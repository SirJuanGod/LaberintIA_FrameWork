import math
import os
import random
import subprocess
import time
from os import path
import threading

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from squaternion import Quaternion
from ros_gz_interfaces.srv import ControlWorld, SetEntityPose
from ros_gz_interfaces.msg import Entity

GOAL_REACHED_DIST = 0.3
COLLISION_DIST = 0.35
TIME_DELTA = 0.1

def check_pos(x, y):
    goal_ok = True
    if -3.8 > x > -6.2 and 6.2 > y > 3.8: goal_ok = False
    if -1.3 > x > -2.7 and 4.7 > y > -0.2: goal_ok = False
    if -0.3 > x > -4.2 and 2.7 > y > 1.3: goal_ok = False
    if -0.8 > x > -4.2 and -2.3 > y > -4.2: goal_ok = False
    if -1.3 > x > -3.7 and -0.8 > y > -2.7: goal_ok = False
    if 4.2 > x > 0.8 and -1.8 > y > -3.2: goal_ok = False
    if 4 > x > 2.5 and 0.7 > y > -3.2: goal_ok = False
    if 6.2 > x > 3.8 and -3.3 > y > -4.2: goal_ok = False
    if 4.2 > x > 1.3 and 3.7 > y > 1.5: goal_ok = False
    if -3.0 > x > -7.2 and 0.5 > y > -1.5: goal_ok = False
    if x > 4.5 or x < -4.5 or y > 4.5 or y < -4.5: goal_ok = False
    return goal_ok


class GazeboEnv(Node):
    """Superclass for all Gazebo environments."""

    def __init__(self, launchfile, environment_dim=3):
        super().__init__('td3_env_node')
        self.environment_dim = environment_dim
        self.odom_x = 0.0
        self.odom_y = 0.0

        self.goal_x = 1.0
        self.goal_y = 0.0

        self.upper = 5.0
        self.lower = -5.0
        
        # 3 distancias: front, left, right
        self.sensor_data = np.ones(self.environment_dim) * 10.0
        self.last_odom = None
        self.world_name = "default"

        # Iniciar rclpy si no está iniciado
        if not rclpy.ok():
            rclpy.init()

        # Lanzar simulacion
        print("Lanzando simulacion ROS 2...")
        self.sim_process = subprocess.Popen(["ros2", "launch", "laberintia_crtll", "laberintia.gazebo.launch.py"])
        time.sleep(10) # Esperar a que Gazebo inicie
        print("Gazebo lanzado!")

        # Publishers y Subscribers
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 1)
        self.publisher = self.create_publisher(MarkerArray, 'goal_point', 3)
        self.publisher2 = self.create_publisher(MarkerArray, 'linear_velocity', 1)
        self.publisher3 = self.create_publisher(MarkerArray, 'angular_velocity', 1)
        
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 1)
        self.front_sub = self.create_subscription(LaserScan, '/sensor/front', self.front_callback, 1)
        self.left_sub = self.create_subscription(LaserScan, '/sensor/left', self.left_callback, 1)
        self.right_sub = self.create_subscription(LaserScan, '/sensor/right', self.right_callback, 1)

        # Servicios Ignition
        self.set_pose_cli = self.create_client(SetEntityPose, f'/world/{self.world_name}/set_pose')
        self.control_cli = self.create_client(ControlWorld, f'/world/{self.world_name}/control')

        # Hilo para spin
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()

    def front_callback(self, msg):
        self.sensor_data[0] = min(msg.ranges) if msg.ranges else 10.0

    def left_callback(self, msg):
        self.sensor_data[1] = min(msg.ranges) if msg.ranges else 10.0

    def right_callback(self, msg):
        self.sensor_data[2] = min(msg.ranges) if msg.ranges else 10.0

    def odom_callback(self, msg):
        self.last_odom = msg

    def pause_sim(self, pause=True):
        if self.control_cli.wait_for_service(timeout_sec=1.0):
            req = ControlWorld.Request()
            req.world_control.pause = pause
            self.control_cli.call_async(req)

    def set_model_state(self, name, x, y, yaw):
        if self.set_pose_cli.wait_for_service(timeout_sec=1.0):
            req = SetEntityPose.Request()
            req.entity = Entity()
            req.entity.name = name
            req.entity.type = Entity.MODEL
            req.pose.position.x = x
            req.pose.position.y = y
            req.pose.position.z = 0.05
            
            q = Quaternion.from_euler(0.0, 0.0, yaw)
            req.pose.orientation.x = q.x
            req.pose.orientation.y = q.y
            req.pose.orientation.z = q.z
            req.pose.orientation.w = q.w
            self.set_pose_cli.call_async(req)

    def step(self, action):
        target = False

        vel_cmd = Twist()
        vel_cmd.linear.x = float(action[0])
        vel_cmd.angular.z = float(action[1])
        self.vel_pub.publish(vel_cmd)
        self.publish_markers(action)

        self.pause_sim(False)
        time.sleep(TIME_DELTA)
        self.pause_sim(True)

        done, collision, min_laser = self.observe_collision(self.sensor_data)
        v_state = self.sensor_data.copy()

        if self.last_odom:
            self.odom_x = self.last_odom.pose.pose.position.x
            self.odom_y = self.last_odom.pose.pose.position.y
            quaternion = Quaternion(
                self.last_odom.pose.pose.orientation.w,
                self.last_odom.pose.pose.orientation.x,
                self.last_odom.pose.pose.orientation.y,
                self.last_odom.pose.pose.orientation.z,
            )
            euler = quaternion.to_euler(degrees=False)
            angle = round(euler[2], 4)
        else:
            angle = 0.0

        distance = np.linalg.norm([self.odom_x - self.goal_x, self.odom_y - self.goal_y])

        skew_x = self.goal_x - self.odom_x
        skew_y = self.goal_y - self.odom_y
        dot = skew_x * 1 + skew_y * 0
        mag1 = math.sqrt(math.pow(skew_x, 2) + math.pow(skew_y, 2))
        mag2 = 1.0
        if mag1 > 0:
            beta = math.acos(dot / (mag1 * mag2))
        else:
            beta = 0
            
        if skew_y < 0:
            beta = -beta if skew_x < 0 else -beta

        theta = beta - angle
        if theta > np.pi:
            theta = np.pi - theta
            theta = -np.pi - theta
        if theta < -np.pi:
            theta = -np.pi - theta
            theta = np.pi - theta

        if distance < GOAL_REACHED_DIST:
            target = True
            done = True

        robot_state = [distance, theta, action[0], action[1]]
        state = np.append(v_state, robot_state)
        reward = self.get_reward(target, collision, action, min_laser)
        return state, reward, done, target

    def reset(self):
        angle = np.random.uniform(-np.pi, np.pi)
        
        x, y = 0, 0
        position_ok = False
        while not position_ok:
            x = np.random.uniform(-4.5, 4.5)
            y = np.random.uniform(-4.5, 4.5)
            position_ok = check_pos(x, y)
            
        self.set_model_state("laberintia", x, y, angle)

        self.odom_x = x
        self.odom_y = y

        self.change_goal()
        self.random_box()
        self.publish_markers([0.0, 0.0])

        self.pause_sim(False)
        time.sleep(TIME_DELTA)
        self.pause_sim(True)

        v_state = self.sensor_data.copy()

        distance = np.linalg.norm([self.odom_x - self.goal_x, self.odom_y - self.goal_y])
        skew_x = self.goal_x - self.odom_x
        skew_y = self.goal_y - self.odom_y
        dot = skew_x * 1 + skew_y * 0
        mag1 = math.sqrt(math.pow(skew_x, 2) + math.pow(skew_y, 2))
        mag2 = 1.0
        if mag1 > 0:
            beta = math.acos(dot / (mag1 * mag2))
        else:
            beta = 0

        if skew_y < 0:
            beta = -beta if skew_x < 0 else -beta
        theta = beta - angle

        if theta > np.pi:
            theta = np.pi - theta
            theta = -np.pi - theta
        if theta < -np.pi:
            theta = -np.pi - theta
            theta = np.pi - theta

        robot_state = [distance, theta, 0.0, 0.0]
        state = np.append(v_state, robot_state)
        return state

    def change_goal(self):
        if self.upper < 10: self.upper += 0.004
        if self.lower > -10: self.lower -= 0.004

        goal_ok = False
        while not goal_ok:
            self.goal_x = self.odom_x + random.uniform(self.upper, self.lower)
            self.goal_y = self.odom_y + random.uniform(self.upper, self.lower)
            goal_ok = check_pos(self.goal_x, self.goal_y)

    def random_box(self):
        # We can also set pose for boxes if they exist in the world, else ignore.
        pass

    def publish_markers(self, action):
        markerArray = MarkerArray()
        marker = Marker()
        marker.header.frame_id = "odom"
        marker.type = marker.CYLINDER
        marker.action = marker.ADD
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.01
        marker.color.a = 1.0
        marker.color.g = 1.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = float(self.goal_x)
        marker.pose.position.y = float(self.goal_y)
        markerArray.markers.append(marker)
        self.publisher.publish(markerArray)

    @staticmethod
    def observe_collision(laser_data):
        min_laser = min(laser_data)
        if min_laser < COLLISION_DIST:
            return True, True, min_laser
        return False, False, min_laser

    @staticmethod
    def get_reward(target, collision, action, min_laser):
        if target:
            return 100.0
        elif collision:
            return -100.0
        else:
            r3 = lambda x: 1 - x if x < 1 else 0.0
            return action[0] / 2 - abs(action[1]) / 2 - r3(min_laser) / 2
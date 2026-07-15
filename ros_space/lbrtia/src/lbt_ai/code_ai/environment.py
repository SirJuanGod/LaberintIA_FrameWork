import math
import random
import subprocess
import time
import threading
import os
import xml.etree.ElementTree as ET

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from squaternion import Quaternion
from ros_gz_interfaces.srv import ControlWorld, SetEntityPose
from ros_gz_interfaces.msg import Entity

# Hiperparámetros del entorno
GOAL_REACHED_DIST = 0.3
COLLISION_DIST = 0.35
TIME_DELTA = 0.1
MAX_LIN_VEL = 0.625   # m/s (Basado en v_max = w * r -> 10 * 0.0625)
MAX_ANG_VEL = 2.0     # rad/s

def parse_maze_walls(world_path):
    """
    Lee el archivo maze.world dinámicamente y extrae los Bounding Boxes (Cajas de colisión)
    de todas las paredes (hwall y vwall).
    """
    walls = []
    if not os.path.exists(world_path):
        print(f"Advertencia: No se encontró el archivo de mundo en {world_path}. No habrá colisiones de spawn.")
        return walls

    tree = ET.parse(world_path)
    root = tree.getroot()
    
    for link in root.findall(".//link"):
        name = link.attrib.get('name', '')
        if 'wall' in name:
            # Extraer Posición: <pose>X Y Z R P Y</pose>
            pose_text = link.find('pose').text
            x, y = map(float, pose_text.split()[:2])
            
            # Extraer Tamaño: <size>X Y Z</size>
            size_text = link.find('.//box/size').text
            w, h = map(float, size_text.split()[:2])
            
            # Guardar límites min/max de la pared
            walls.append({
                'min_x': x - (w / 2.0), 'max_x': x + (w / 2.0),
                'min_y': y - (h / 2.0), 'max_y': y + (h / 2.0)
            })
    return walls

def check_pos(x, y, walls, robot_radius=0.2):
    """
    Verifica si la posición (x,y) colisiona con alguna de las paredes cargadas.
    Se utiliza el 'robot_radius' como un margen de seguridad para que no aparezca rozando la pared.
    """
    # Límites externos del mundo
    if x > 4.5 or x < -4.5 or y > 4.5 or y < -4.5: 
        return False
        
    for wall in walls:
        # Lógica de colisión AABB (Axis-Aligned Bounding Box) con margen
        if (x > wall['min_x'] - robot_radius and x < wall['max_x'] + robot_radius and
            y > wall['min_y'] - robot_radius and y < wall['max_y'] + robot_radius):
            return False # Colisión detectada, posición no válida
            
    return True # Posición segura


class GazeboEnv(Node):
    def __init__(self, launchfile, environment_dim=3):
        if not rclpy.ok(): rclpy.init()
        super().__init__('td3_env_node')
        
        self.environment_dim = environment_dim
        self.odom_x, self.odom_y = 0.0, 0.0
        self.goal_x, self.goal_y = 1.0, 0.0
        self.upper, self.lower = 5.0, -5.0

        world_file_path = "/mnt/disco/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/ros_space/lbrtia/src/lbt_gazebo/worlds/maze.world"
        self.maze_walls = parse_maze_walls(world_file_path)
        print(f"Se cargaron {len(self.maze_walls)} paredes desde el archivo de mundo.")

        self.sensor_data = np.ones(self.environment_dim) * 10.0
        self.last_odom = None
        self.world_name = "default"

        print(f"Lanzando simulacion ROS 2: {launchfile} ...")
        self.sim_process = subprocess.Popen(["ros2", "launch", "lbt_gazebo", launchfile])
        time.sleep(8)
        print("Gazebo lanzado!")

        # Publishers / Subscribers
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 1)
        self.publisher = self.create_publisher(MarkerArray, 'goal_point', 3)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 1)
        self.front_sub = self.create_subscription(LaserScan, '/scan_center', self.front_callback, 1)
        self.left_sub = self.create_subscription(LaserScan, '/scan_left', self.left_callback, 1)
        self.right_sub = self.create_subscription(LaserScan, '/scan_right', self.right_callback, 1)

        self.set_pose_cli = self.create_client(SetEntityPose, f'/world/{self.world_name}/set_pose')
        self.control_cli = self.create_client(ControlWorld, f'/world/{self.world_name}/control')

        self.ros_executor = SingleThreadedExecutor()
        self.ros_executor.add_node(self)
        self.spin_thread = threading.Thread(target=self.ros_executor.spin, daemon=True)
        self.spin_thread.start()

    # --- Callbacks ---
    def front_callback(self, msg): self.sensor_data[0] = min(msg.ranges) if msg.ranges else 10.0
    def left_callback(self, msg):  self.sensor_data[1] = min(msg.ranges) if msg.ranges else 10.0
    def right_callback(self, msg): self.sensor_data[2] = min(msg.ranges) if msg.ranges else 10.0
    def odom_callback(self, msg):  self.last_odom = msg

    # --- Interacción con Gazebo ---
    def pause_sim(self, pause=True):
        if self.control_cli.wait_for_service(timeout_sec=1.0):
            req = ControlWorld.Request()
            req.world_control.pause = pause
            self.control_cli.call_async(req)

    def set_model_state(self, name, x, y, yaw):
        if self.set_pose_cli.wait_for_service(timeout_sec=1.0):
            req = SetEntityPose.Request()
            req.entity.name = name
            req.entity.type = Entity.MODEL
            req.pose.position.x = x
            req.pose.position.y = y
            req.pose.position.z = 0.05
            q = Quaternion.from_euler(0.0, 0.0, yaw)
            req.pose.orientation.x, req.pose.orientation.y = q.x, q.y
            req.pose.orientation.z, req.pose.orientation.w = q.z, q.w
            self.set_pose_cli.call_async(req)

    # --- Lógica de RL ---
    def step(self, action):
        """Action esperada: [linear (-1 a 1), angular (-1 a 1)]"""
        # Escalar la acción al mundo real del robot
        v_real = ((action[0] + 1.0) / 2.0) * MAX_LIN_VEL  # Mapea [-1, 1] a [0, MAX_LIN_VEL]
        w_real = action[1] * MAX_ANG_VEL                  # Mapea [-1, 1] a [-MAX_ANG_VEL, MAX_ANG_VEL]

        vel_cmd = Twist()
        vel_cmd.linear.x = float(v_real)
        vel_cmd.angular.z = float(w_real)
        self.vel_pub.publish(vel_cmd)
        
        self.publish_markers()
        self.pause_sim(False)
        time.sleep(TIME_DELTA)
        self.pause_sim(True)

        min_laser = min(self.sensor_data[:3])
        collision = min_laser < COLLISION_DIST
        v_state = self.sensor_data.copy()

        # Calcular Odometría y Meta
        angle = 0.0
        if self.last_odom:
            self.odom_x = self.last_odom.pose.pose.position.x
            self.odom_y = self.last_odom.pose.pose.position.y
            q = Quaternion(
                self.last_odom.pose.pose.orientation.w,
                self.last_odom.pose.pose.orientation.x,
                self.last_odom.pose.pose.orientation.y,
                self.last_odom.pose.pose.orientation.z,
            )
            angle = round(q.to_euler(degrees=False)[2], 4)

        distance = np.linalg.norm([self.odom_x - self.goal_x, self.odom_y - self.goal_y])
        skew_x, skew_y = self.goal_x - self.odom_x, self.goal_y - self.odom_y
        
        mag1 = math.sqrt(skew_x**2 + skew_y**2)
        beta = math.acos(skew_x / mag1) if mag1 > 0 else 0
        if skew_y < 0: beta = -beta
        
        theta = beta - angle
        while theta > np.pi: theta -= 2 * np.pi
        while theta < -np.pi: theta += 2 * np.pi

        target = distance < GOAL_REACHED_DIST
        done = target or collision

        # Estado: [laser1, laser2, laser3, dist_meta, theta_meta, v_actual, w_actual]
        robot_state = [distance, theta, action[0], action[1]]
        state = np.append(v_state, robot_state)
        reward = self.get_reward(target, collision, action, min_laser)
        
        return state, reward, done, target

    def reset(self):
        angle = np.random.uniform(-np.pi, np.pi)
        
        while True:
            x, y = np.random.uniform(-4.5, 4.5), np.random.uniform(-4.5, 4.5)
            # Ahora usamos la nueva función pasando las paredes cargadas
            if check_pos(x, y, self.maze_walls): 
                break
            
        self.set_model_state("lbt", x, y, angle) # Aquí asumo que tu modelo en Gazebo se llama "lbt" (del URDF)
        self.odom_x, self.odom_y = x, y

        self.change_goal()
        self.publish_markers()
        
        self.pause_sim(False)
        time.sleep(TIME_DELTA)
        self.pause_sim(True)

        v_state = self.sensor_data.copy()
        distance = np.linalg.norm([self.odom_x - self.goal_x, self.odom_y - self.goal_y])
        robot_state = [distance, 0.0, 0.0, 0.0]
        return np.append(v_state, robot_state)

    def change_goal(self):
        if self.upper < 10: self.upper += 0.004
        if self.lower > -10: self.lower -= 0.004
        while True:
            self.goal_x = self.odom_x + random.uniform(self.upper, self.lower)
            self.goal_y = self.odom_y + random.uniform(self.upper, self.lower)
            if check_pos(self.goal_x, self.goal_y, self.maze_walls): 
                break

    def publish_markers(self):
        markerArray = MarkerArray()
        marker = Marker()
        marker.header.frame_id = "odom"
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD
        marker.scale.x, marker.scale.y, marker.scale.z = 0.1, 0.1, 0.01
        marker.color.a, marker.color.g = 1.0, 1.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x, marker.pose.position.y = float(self.goal_x), float(self.goal_y)
        markerArray.markers.append(marker)
        self.publisher.publish(markerArray)

    @staticmethod
    def get_reward(target, collision, action, min_laser):
        if target: return 100.0
        if collision: return -100.0
        r3 = 1 - min_laser if min_laser < 1.0 else 0.0
        return (action[0] / 2.0) - (abs(action[1]) / 2.0) - (r3 / 2.0)
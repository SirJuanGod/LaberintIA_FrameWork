#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from tf2_ros import TransformBroadcaster

class lbt_control(Node):
    def __init__(self):
        super().__init__('lbt_control')

        self.wheel_radius = 0.0625
        self.wheel_separation = 0.16

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()

        self.back_wheel_vel = 0.0
        self.front_wheel_vel = 0.0
        self.back_wheel_pos = 0.0
        self.front_wheel_pos = 0.0

        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)

        self.vel_cmd_pub = self.create_publisher(
            Float64MultiArray, '/velocity_controller/commands', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)

        self.tf_broadcaster = TransformBroadcaster(self)
        self.odom_timer = self.create_timer(0.02, self.publish_odometry)

        self.get_logger().info('LBT Control Started')

    def cmd_vel_callback(self, msg):
        v = msg.linear.x
        omega = msg.angular.z

        v_back = v - (omega * self.wheel_separation / 2.0)
        v_front = v + (omega * self.wheel_separation / 2.0)

        omega_back = v_back / self.wheel_radius
        omega_front = v_front / self.wheel_radius

        self.back_wheel_vel = omega_back
        self.front_wheel_vel = omega_front

        cmd_msg = Float64MultiArray()
        cmd_msg.data = [omega_back, omega_front]
        self.vel_cmd_pub.publish(cmd_msg)

    def joint_state_callback(self, msg):
        try:
            back_idx = msg.name.index('wheel_back')
            front_idx = msg.name.index('wheel_front')
            
            if len(msg.velocity) > max(back_idx, front_idx):
                self.back_wheel_vel = msg.velocity[back_idx]
                self.front_wheel_vel = msg.velocity[front_idx]
        except ValueError:
            pass

    def publish_odometry(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        v_b = self.back_wheel_vel * self.wheel_radius
        v_f = self.front_wheel_vel * self.wheel_radius

        v = (v_f + v_b) / 2.0
        omega = (v_f - v_b) / self.wheel_separation

        delta_theta = omega * dt
        self.theta += delta_theta
        avg_theta = self.theta - delta_theta / 2.0
        
        self.x += v * math.cos(avg_theta) * dt
        self.y += v * math.sin(avg_theta) * dt

        q = self.quaternion_from_euler(0, 0, self.theta)

        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.tf_broadcaster.sendTransform(t)

        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]
        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = omega
        self.odom_pub.publish(odom)

        self.back_wheel_pos += self.back_wheel_vel * dt
        self.front_wheel_pos += self.front_wheel_vel * dt
        
        joint_msg = JointState()
        joint_msg.header.stamp = current_time.to_msg()
        joint_msg.name = ['wheel_back', 'wheel_front']
        joint_msg.position = [self.back_wheel_pos, self.front_wheel_pos]
        joint_msg.velocity = [self.back_wheel_vel, self.front_wheel_vel]
        self.joint_state_pub.publish(joint_msg)

    def quaternion_from_euler(self, roll, pitch, yaw):
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        q = [0] * 4
        q[0] = sr * cp * cy - cr * sp * sy
        q[1] = cr * sp * cy + sr * cp * sy
        q[2] = cr * cp * sy - sr * sp * cy
        q[3] = cr * cp * cy + sr * sp * sy
        return q

def main(args=None):
    rclpy.init(args=args)
    node = lbt_control()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
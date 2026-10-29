#!/usr/bin/env python3
"""Simulador cinemático 2D ligero (sin Gazebo) para ver/entrenar en RViz.

Imita lo que lbt_ai usa de Gazebo: /cmd_vel, /odom, /tf, /scan_*, /joint_states
y los servicios /world/maze_world/control y /world/maze_world/set_pose.
"""
import math
import os
import xml.etree.ElementTree as ET

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState, LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from ros_gz_interfaces.srv import ControlWorld, SetEntityPose
from tf2_ros import TransformBroadcaster

DT = 0.02
WHEEL_RADIUS = 0.033       # medido de la malla part_1__2.stl
WHEEL_SEPARATION = 0.125   # distancia lateral entre ruedas en rbt.urdf.xacro
ROBOT_RADIUS = 0.1         # media anchura de base.stl (~0.093)
WALL_HEIGHT = 0.5
# topic: (frame, x, y, yaw) de cada HC-SR04 en el marco base, igual que rbt.urdf.xacro
SENSORS = {
    'scan_center': ('hc_sr04_center_link', 0.040, 0.0, 0.0),
    'scan_left': ('hc_sr04_left_link', 0.0, -0.049, -math.pi / 2),
    'scan_right': ('hc_sr04_right_link', 0.0, 0.049, math.pi / 2),
}
N_RAYS, HALF_FOV, RANGE_MIN, RANGE_MAX = 32, 0.1309, 0.02, 4.0


def parse_maze_walls(world_path):
    """Bounding boxes (min/max x/y) de las paredes (links con 'wall') de un .world."""
    walls = []
    if not os.path.exists(world_path):
        print(f"Advertencia: No se encontró el archivo de mundo en {world_path}.")
        return walls

    for link in ET.parse(world_path).getroot().findall(".//link"):
        if 'wall' in link.attrib.get('name', ''):
            x, y = map(float, link.find('pose').text.split()[:2])
            w, h = map(float, link.find('.//box/size').text.split()[:2])
            walls.append({
                'min_x': x - (w / 2.0), 'max_x': x + (w / 2.0),
                'min_y': y - (h / 2.0), 'max_y': y + (h / 2.0)
            })
    return walls


def raycast(boxes, ox, oy, angles):
    """Distancia desde (ox, oy) a la primera caja en cada ángulo (inf si no hay o supera RANGE_MAX).

    boxes: array Nx4 [min_x, max_x, min_y, max_y]. Método de slabs vectorizado.
    """
    dx, dy = np.cos(angles)[:, None], np.sin(angles)[:, None]
    with np.errstate(divide='ignore', invalid='ignore'):
        tx1, tx2 = (boxes[:, 0] - ox) / dx, (boxes[:, 1] - ox) / dx
        ty1, ty2 = (boxes[:, 2] - oy) / dy, (boxes[:, 3] - oy) / dy
    # fmin/fmax ignoran el NaN de 0/0 (rayo paralelo justo sobre un borde)
    t_near = np.fmax(np.fmin(tx1, tx2), np.fmin(ty1, ty2))
    t_far = np.fmin(np.fmax(tx1, tx2), np.fmax(ty1, ty2))
    t = np.where(t_far >= np.maximum(t_near, 0.0), np.maximum(t_near, 0.0), np.inf).min(axis=1)
    return np.where(t <= RANGE_MAX, t, np.inf)


class LbtSim(Node):
    def __init__(self):
        super().__init__('lbt_sim')
        world_file = self.declare_parameter('world_file', '').value
        world_name = self.declare_parameter('world_name', 'maze_world').value
        self.x = self.declare_parameter('x', -4.5).value
        self.y = self.declare_parameter('y', -4.5).value
        self.yaw = self.declare_parameter('yaw', 0.0).value

        walls = parse_maze_walls(world_file)
        self.boxes = np.array([[w['min_x'], w['max_x'], w['min_y'], w['max_y']] for w in walls]).reshape(-1, 4)
        self.get_logger().info(f'{len(self.boxes)} paredes cargadas de {world_file}')

        self.cmd = Twist()
        self.paused = False
        self.wheel_pos = [0.0, 0.0]  # [izquierda (-Y), derecha (+Y)]
        self.ticks = 0
        self.ray_offsets = np.linspace(-HALF_FOV, HALF_FOV, N_RAYS)

        self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.walls_pub = self.create_publisher(MarkerArray, '/maze_walls', 1)
        self.scan_pubs = {t: self.create_publisher(LaserScan, '/' + t, 10) for t in SENSORS}
        self.tf_broadcaster = TransformBroadcaster(self)
        self.create_service(ControlWorld, f'/world/{world_name}/control', self.control_callback)
        self.create_service(SetEntityPose, f'/world/{world_name}/set_pose', self.set_pose_callback)
        self.create_timer(DT, self.tick)
        self.get_logger().info('LBT Sim (RViz) iniciado')

    def cmd_callback(self, msg):
        self.cmd = msg

    def control_callback(self, req, res):
        self.paused = req.world_control.pause
        res.success = True
        return res

    def set_pose_callback(self, req, res):
        q = req.pose.orientation
        self.x, self.y = req.pose.position.x, req.pose.position.y
        self.yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        res.success = True
        return res

    def is_free(self, x, y):
        b, r = self.boxes, ROBOT_RADIUS
        return not np.any((x > b[:, 0] - r) & (x < b[:, 1] + r) & (y > b[:, 2] - r) & (y < b[:, 3] + r))

    def tick(self):
        v, w = self.cmd.linear.x, self.cmd.angular.z
        if self.paused:
            v = w = 0.0
        else:
            mid_yaw = self.yaw + w * DT / 2.0
            nx, ny = self.x + v * math.cos(mid_yaw) * DT, self.y + v * math.sin(mid_yaw) * DT
            if self.is_free(nx, ny):  # la pared bloquea el avance, como en Gazebo
                self.x, self.y = nx, ny
            self.yaw = math.atan2(math.sin(self.yaw + w * DT), math.cos(self.yaw + w * DT))
            self.wheel_pos[0] += (v - w * WHEEL_SEPARATION / 2.0) / WHEEL_RADIUS * DT
            self.wheel_pos[1] += (v + w * WHEEL_SEPARATION / 2.0) / WHEEL_RADIUS * DT

        stamp = self.get_clock().now().to_msg()
        qz, qw = math.sin(self.yaw / 2.0), math.cos(self.yaw / 2.0)

        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x, t.transform.translation.y = self.x, self.y
        t.transform.rotation.z, t.transform.rotation.w = qz, qw
        self.tf_broadcaster.sendTransform(t)

        odom = Odometry()
        odom.header = t.header
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x, odom.pose.pose.position.y = self.x, self.y
        odom.pose.pose.orientation.z, odom.pose.pose.orientation.w = qz, qw
        odom.twist.twist.linear.x, odom.twist.twist.angular.z = v, w
        self.odom_pub.publish(odom)

        joints = JointState()
        joints.header.stamp = stamp
        joints.name = ['joint_rueda_izquierda', 'joint_rueda_derecha']
        joints.position = list(self.wheel_pos)
        self.joint_pub.publish(joints)

        c, s = math.cos(self.yaw), math.sin(self.yaw)
        for topic, (frame, sx, sy, syaw) in SENSORS.items():
            ranges = raycast(self.boxes, self.x + c * sx - s * sy, self.y + s * sx + c * sy,
                             self.yaw + syaw + self.ray_offsets)
            scan = LaserScan()
            scan.header.stamp, scan.header.frame_id = stamp, frame
            scan.angle_min, scan.angle_max = -HALF_FOV, HALF_FOV
            scan.angle_increment = 2.0 * HALF_FOV / (N_RAYS - 1)
            scan.range_min, scan.range_max = RANGE_MIN, RANGE_MAX
            scan.ranges = ranges.astype(float).tolist()
            self.scan_pubs[topic].publish(scan)

        if self.ticks % int(1.0 / DT) == 0:  # paredes 1 vez/s para que RViz las reciba aunque arranque después
            self.publish_walls(stamp)
        self.ticks += 1

    def publish_walls(self, stamp):
        markers = MarkerArray()
        for i, (x0, x1, y0, y1) in enumerate(self.boxes):
            m = Marker()
            m.header.stamp, m.header.frame_id = stamp, 'odom'
            m.ns, m.id, m.type, m.action = 'maze', i, Marker.CUBE, Marker.ADD
            m.pose.position.x, m.pose.position.y, m.pose.position.z = (x0 + x1) / 2.0, (y0 + y1) / 2.0, WALL_HEIGHT / 2.0
            m.pose.orientation.w = 1.0
            m.scale.x, m.scale.y, m.scale.z = x1 - x0, y1 - y0, WALL_HEIGHT
            m.color.r, m.color.g, m.color.b, m.color.a = 0.7, 0.2, 0.2, 1.0
            markers.markers.append(m)
        self.walls_pub.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = LbtSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

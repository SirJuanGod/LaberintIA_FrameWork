import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


# Simulación ligera sin Gazebo: lbt_sim (cinemática 2D) + robot_state_publisher + RViz
def generate_launch_description():
    lbt_description_dir = get_package_share_directory('lbt_description')
    lbt_gazebo_dir = get_package_share_directory('lbt_gazebo')
    urdf_xacro_path = os.path.join(lbt_description_dir, 'urdf', 'rbt.urdf.xacro')

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': ParameterValue(Command(['xacro ', urdf_xacro_path]), value_type=str),
            }],
        ),
        Node(
            package='lbt_control',
            executable='lbt_sim',
            output='screen',
            parameters=[{'world_file': os.path.join(lbt_gazebo_dir, 'worlds', 'maze.world')}],
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(lbt_gazebo_dir, 'rviz', 'sim.rviz')],
        ),
    ])

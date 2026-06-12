import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('laberintia_crtll')
    xacro_file = os.path.join(pkg_dir, 'xacro', 'laberintia', 'robot.xacro')
    
    robot_description_content = Command(
        [FindExecutable(name='xacro'), ' ', xacro_file]
    )
    
    robot_description = {'robot_description': robot_description_content}
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description, {'publish_frequency': 30.0}],
        ),
        
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'publish_frequency': 30.0}],
        ),
    ])
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('laberintia_crtll')
    xacro_file = os.path.join(pkg_dir, 'xacro', 'laberintia', 'robot.xacro')
    world_file = os.path.join(pkg_dir, 'worlds', 'TD3.world')
    
    # Procesar xacro a URDF
    robot_description = Command([
        FindExecutable(name='xacro'), ' ', xacro_file
    ])
    
    # Gazebo
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )
    
    return LaunchDescription([
        gz_sim,
        
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),
        
        # Joint state publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'publish_frequency': 30.0}],
        ),
        
        # Spawn robot en Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'laberintia',
                '-topic', 'robot_description',
                '-x', '0.0',
                '-y', '0.0', 
                '-z', '0.01',
            ],
            output='screen',
        ),

        # Bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/sensor/front@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/sensor/left@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/sensor/right@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            ],
            output='screen',
        ),
    ])

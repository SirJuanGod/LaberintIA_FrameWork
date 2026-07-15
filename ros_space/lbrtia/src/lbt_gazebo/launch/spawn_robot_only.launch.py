import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

def generate_launch_description():
    # Rutas a tus paquetes
    lbt_description_dir = get_package_share_directory('lbt_description')
    ros_gz_sim_dir = get_package_share_directory('ros_gz_sim')

    # 1. Cargar el robot (URDF)
    urdf_xacro_path = os.path.join(lbt_description_dir, 'urdf', 'rbt.urdf.xacro')
    robot_description = {"robot_description": ParameterValue(Command(['xacro ', urdf_xacro_path]), value_type=str)}

    # 2. Gazebo con mundo vacío
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items() # Mundo vacío por defecto
    )

    # 3. Publicador de estado del robot
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 4. Spawner del robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'lbt', '-z', '0.2'], # Un poco elevado para evitar colisiones
        output='screen'
    )

    # 5. Bridge básico para poder moverlo
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
        ],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        TimerAction(period=2.0, actions=[spawn_entity]),
        bridge
    ])
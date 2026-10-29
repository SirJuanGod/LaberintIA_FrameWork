import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    urdf_xacro = os.path.join(
        get_package_share_directory('lbt_description'),
        'urdf',
        'rbt.urdf.xacro'
    )

    rbt_desc = ParameterValue(
        Command(['xacro ', urdf_xacro]), value_type=str
    )

    rviz_config_dir = os.path.join(

        get_package_share_directory('lbt_description'),
        'rviz',
        'display.rviz'
    )
    return LaunchDescription(
        [
            Node(
                package = 'lbt_control',
                executable = 'lbt_control',
                name = 'lbt_controller_node',
                output='screen',
                parameters=
                            [
                                {'use_sim_time': False}
                            ] 
            ),

            Node(
                package = 'robot_state_publisher',
                executable = 'robot_state_publisher',
                name = 'robot_state_publisher',
                output = 'screen',
                parameters=
                            [
                                {
                                    'use_sim_time':False,
                                    'robot_description': rbt_desc
                                }
                            ]
            ),

            Node(
                package = 'rviz2',
                executable = 'rviz2',
                name = 'rviz2',
                output ='screen',
                arguments = [
                            '-d',
                            rviz_config_dir
                            ]
            ),
        ]
    )

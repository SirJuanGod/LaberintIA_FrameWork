cmake_minimum_required(VERSION 3.5)
project(velodyne_gazebo_plugins)

# Default to C++14 if not set
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(gazebo REQUIRED)

# Set Gazebo C++ flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")

# Include directories
include_directories(
  include
  ${GAZEBO_INCLUDE_DIRS}
)

# Libraries
add_library(gazebo_ros_velodyne_laser src/GazeboRosVelodyneLaser.cpp)
target_link_libraries(gazebo_ros_velodyne_laser
  ${rclcpp_LIBRARIES}
  ${sensor_msgs_LIBRARIES}
  ${tf2_LIBRARIES}
  ${gazebo_ros_LIBRARIES}
  ${GAZEBO_LIBRARIES}
  RayPlugin
)

add_library(gazebo_ros_velodyne_gpu_laser src/GazeboRosVelodyneLaser.cpp)
target_link_libraries(gazebo_ros_velodyne_gpu_laser
  ${rclcpp_LIBRARIES}
  ${sensor_msgs_LIBRARIES}
  ${tf2_LIBRARIES}
  ${gazebo_ros_LIBRARIES}
  ${GAZEBO_LIBRARIES}
  GpuRayPlugin
)
target_compile_definitions(gazebo_ros_velodyne_gpu_laser PRIVATE GAZEBO_GPU_RAY=1)

# Export
ament_export_include_directories(include)
ament_export_libraries(gazebo_ros_velodyne_laser gazebo_ros_velodyne_gpu_laser)
ament_export_dependencies(rclcpp sensor_msgs gazebo_ros)

# Install
install(TARGETS gazebo_ros_velodyne_laser gazebo_ros_velodyne_gpu_laser
        LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)

install(DIRECTORY include/${PROJECT_NAME}/
        DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
)

ament_package()

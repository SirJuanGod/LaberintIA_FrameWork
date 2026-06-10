cmake_minimum_required(VERSION 3.5)
project(velodyne_description)

# Default to C++14 if not set
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

catkin_package()

install(DIRECTORY launch meshes rviz urdf world
        DESTINATION share/${PROJECT_NAME}
)

ament_package()

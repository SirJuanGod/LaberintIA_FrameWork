cmake_minimum_required(VERSION 3.5)
project(multi_robot_scenario)

# Default to C++14 if not set
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

# Install launch, meshes, xacro directories
install(DIRECTORY launch meshes xacro
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

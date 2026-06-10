cmake_minimum_required(VERSION 3.5)
project(velodyne_simulator)

# Default to C++14 if not set
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

ament_package()

from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'laberintia_crtll'

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
]

# Add xacro files
xacro_dir = os.path.join('xacro')
data_files.append((os.path.join('share', package_name, 'xacro'), glob(os.path.join(xacro_dir, '*.xacro'))))
data_files.append((os.path.join('share', package_name, 'xacro', 'laberintia'), glob(os.path.join(xacro_dir, 'laberintia', '*.xacro'))))

# Add launch files
launch_dir = 'launch'
if os.path.exists(launch_dir):
    data_files.append((os.path.join('share', package_name, 'launch'), glob(os.path.join(launch_dir, '*.py'))))

# Add meshes
meshes_dir = 'meshes'
if os.path.exists(meshes_dir):
    for root, dirs, files in os.walk(meshes_dir):
        for f in files:
            filepath = os.path.join(root, f)
            install_dir = os.path.join('share', package_name, root)
            data_files.append((install_dir, [filepath]))

# Add worlds
worlds_dir = 'worlds'
if os.path.exists(worlds_dir):
    data_files.append((os.path.join('share', package_name, 'worlds'), glob(os.path.join(worlds_dir, '*.world'))))

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools', 'launch', 'launch-ros'],
    zip_safe=True,
    maintainer='sjg',
    maintainer_email='sjg@todo.todo',
    description='LaberintIA ROS2',
    license='MIT',
    entry_points={'console_scripts': []},
)

This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.
The content has been processed where comments have been removed, empty lines have been removed, line numbers have been added, content has been formatted for parsing in markdown style, content has been compressed (code blocks are separated by ⋮---- delimiter), security check has been disabled.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: README.md, mpc_python/mpc_demo_mujoco.py, mpc_python/models/mushr/cars/pusher_car.template, mpc_python/models/mushr/cars/pusher_car/buddy.xml, mpc_python/models/mushr/cars/pusher_car/goose.xml, mpc_python/models/mushr/cars/pusher_car/car3.xml, mpc_python/models/mushr/cars/pusher_car/car4.xml, mpc_python/models/mushr/cars/pusher_car/car5.xml, mpc_python/models/mushr/cars/pusher_car/car1.xml, mpc_python/models/mushr/cars/pusher_car/car2.xml, mpc_python/models/mushr/cars/base_car.template, mpc_python/models/mushr/cars/base_car/buddy.xml, mpc_python/models/mushr/cars/base_car/goose.xml, mpc_python/models/mushr/cars/base_car/car3.xml, mpc_python/models/mushr/cars/base_car/car4.xml, mpc_python/models/mushr/cars/base_car/car5.xml, mpc_python/models/mushr/cars/base_car/car1.xml, mpc_python/models/mushr/cars/base_car/car2.xml, flake.lock, flake.nix, mpc_python/cvxpy_mpc/utils.py, mpc_python/cvxpy_mpc/cvxpy_mpc.py, mpc_python/mpc_demo_nosim.py, LICENSE, mpc_python/models/mushr/mush_nano.xml, pyproject.toml, mpc_python/config/simulation.yaml, mpc_python/config/mpc.yaml, env.yml, mpc_python/models/mushr/cars/make_car_model.py, MUJOCO_LOG.TXT, .gitignore, mpc_python/cvxpy_mpc/__init__.py
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Code comments have been removed from supported file types
- Empty lines have been removed from all files
- Line numbers have been added to the beginning of each line
- Content has been formatted for parsing in markdown style
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
mpc_python/
  config/
    mpc.yaml
    simulation.yaml
  cvxpy_mpc/
    __init__.py
    cvxpy_mpc.py
    utils.py
  models/
    mushr/
      cars/
        base_car/
          buddy.xml
          car1.xml
          car2.xml
          car3.xml
          car4.xml
          car5.xml
          goose.xml
        pusher_car/
          buddy.xml
          car1.xml
          car2.xml
          car3.xml
          car4.xml
          car5.xml
          goose.xml
        base_car.template
        make_car_model.py
        pusher_car.template
      mush_nano.xml
  mpc_demo_mujoco.py
  mpc_demo_nosim.py
.gitignore
env.yml
flake.lock
flake.nix
LICENSE
MUJOCO_LOG.TXT
pyproject.toml
README.md
```

# Files

## File: mpc_python/config/mpc.yaml
````yaml
model:
  vehicle:
    wheelbase: 0.2965
    width: 0.16
    max_speed: 1.5
    max_acc: 1.0
    max_d_acc: 1.0
    max_steer: 0.38
    max_d_steer: 0.52
controller:
  prediction:
    horizon_time: 5.0
    timestep: 0.2
  weights:
    state_cost: [10, 50, 30, 30]
    final_state_cost: [10, 50, 30, 30]
    input_cost: [10, 10]
    input_rate_cost: [10, 10]
  obstacle:
    safety_margin: 0.15
    slack_penalty: 100000
````

## File: mpc_python/config/simulation.yaml
````yaml
target_speed: 1.0
sensor:
  max_range: 4.0
  fov_deg: 90.0
path:
  waypoints_x: [0, 3, 4, 6, 10, 11, 12, 6, 1, 0]
  waypoints_y: [0, 0, 2, 4, 3, 3, -1, -6, -2, -2]
  interpolation_step: 0.05
obstacles:
  - distance: 3.0
    speed: 0.1
    radius: 0.4
    lateral_offset: 0.3
  - distance: 5.5
    speed: 0.25
    radius: 0.3
    lateral_offset: -0.25
  - distance: 8.5
    speed: 0.20
    radius: 0.5
    lateral_offset: 0.35
start:
  x: 0.0
  y: 0.3
  heading: 0.0
  velocity: 0.0
goal_threshold: 0.2
````

## File: mpc_python/cvxpy_mpc/__init__.py
````python

````

## File: mpc_python/cvxpy_mpc/cvxpy_mpc.py
````python
class MPC
⋮----
path = pathlib.Path(config)
⋮----
path = pathlib.Path(__file__).parent.parent / config
⋮----
config_data = yaml.safe_load(f)
⋮----
config_data = config
⋮----
vehicle_config = config_data["model"]["vehicle"]
obstacle_config = config_data["controller"]["obstacle"]
prediction_config = config_data["controller"]["prediction"]
weights_config = config_data["controller"]["weights"]
⋮----
horizon = (
⋮----
state_cost_weights = (
terminal_cost_weights = (
input_cost_weights = (
input_rate_cost_weights = (
⋮----
# Reference params (DPP-compliant placeholders)
# see https://www.cvxpy.org/tutorial/dpp/index.html
⋮----
# Obstacle params (half-plane linearization)
⋮----
v = x_bar[2]
theta = x_bar[3]
⋮----
a = u_bar[0]
delta = u_bar[1]
⋮----
ct = np.cos(theta)
st = np.sin(theta)
cd = np.cos(delta)
td = np.tan(delta)
⋮----
A = np.zeros((self._state_dim, self._state_dim))
⋮----
A_lin = np.eye(self._state_dim) + self.dt * A
⋮----
B = np.zeros((self._state_dim, self._control_dim))
⋮----
B_lin = self.dt * B
⋮----
f_xu = np.array([v * ct, v * st, a, v * td / self.wheelbase]).reshape(
C_lin = (
⋮----
def _make_mpc_problem(self) -> opt.Problem
⋮----
cost = 0
constraints = []
⋮----
along_track_error = (
cross_track_error = (
error = opt.vstack(
⋮----
terminal_along_track_error = (
terminal_cross_track_error = (
terminal_error = opt.vstack(
⋮----
problem = opt.Problem(opt.Minimize(cost), constraints)
⋮----
cos_values = np.cos(theta_ref)
sin_values = np.sin(theta_ref)
along_projections = cos_values * x_ref + sin_values * y_ref
cross_projections = -sin_values * x_ref + cos_values * y_ref
⋮----
x_guess = np.roll(self._previous_trajectory, -1, axis=1)
⋮----
u_guess = np.roll(self._previous_command, -1, axis=1)
⋮----
x_guess = target
u_guess = np.zeros((self._control_dim, self.control_horizon))
⋮----
x_bar = x_guess[:, k]
u_bar = u_guess[:, k]
⋮----
obstacle_normals_x = np.zeros(self.control_horizon)
obstacle_normals_y = np.zeros(self.control_horizon)
obstacle_distances = np.zeros(self.control_horizon)
⋮----
dx = x_ref[k + 1] - obstacle_x - obstacle_velocity_x * k * self.dt
dy = y_ref[k + 1] - obstacle_y - obstacle_velocity_y * k * self.dt
⋮----
dist = np.hypot(dx, dy)
dist = dist if dist > 1e-5 else 1e-5
⋮----
normal_x = dx / dist
normal_y = dy / dist
⋮----
emergency_controls = np.zeros((self._control_dim, self.control_horizon))
v = initial_state[2]
⋮----
a = -self.max_acc if v > 0 else 0.0
⋮----
v = max(0.0, v + a * self.dt)
⋮----
new_x = np.array(self._states.value)
new_u = np.array(self._controls.value)
⋮----
x_guess = new_x
u_guess = new_u
````

## File: mpc_python/cvxpy_mpc/utils.py
````python
u_fine = np.linspace(0, 1, 2000)
⋮----
arc_lengths = np.zeros(len(u_fine))
⋮----
total_len = arc_lengths[-1]
⋮----
num_points = int(total_len / step)
u_uniform = np.interp(np.linspace(0, total_len, num_points), arc_lengths, u_fine)
⋮----
dx = np.gradient(final_xp)
dy = np.gradient(final_yp)
theta = np.arctan2(dy, dx)
⋮----
def get_nn_idx(state: npt.NDArray[np.float64], path: npt.NDArray[np.float64]) -> int
⋮----
dx = state[0] - path[0, :]
dy = state[1] - path[1, :]
dist = np.hypot(dx, dy)
nn_idx = np.argmin(dist)
⋮----
v = np.array(
⋮----
d = [path[0, nn_idx] - state[0], path[1, nn_idx] - state[1]]
⋮----
target_idx = nn_idx
⋮----
target_idx = nn_idx + 1
⋮----
K = int(T / DT)
⋮----
xref = np.zeros((4, K + 1))
ind = get_nn_idx(state, path)
⋮----
cdist = np.append(
cdist = np.clip(cdist, cdist[0], cdist[-1])
⋮----
start_dist = cdist[ind]
⋮----
interp_points = [d * DT * target_v + start_dist for d in range(0, K + 1)]
⋮----
xref_cdist = np.interp(interp_points, cdist, cdist)
stop_idx = np.where(xref_cdist == cdist[-1])
⋮----
dx = xref[0, :] - state[0]
dy = xref[1, :] - state[1]
⋮----
def fix_angle_reference(angle_ref, angle_init)
⋮----
diff_angle = angle_ref - angle_init
diff_angle = np.unwrap(diff_angle)
⋮----
traj = x_mpc[:2, :].copy()
⋮----
R = np.array([[ct, -st], [st, ct]])
traj = R @ traj
⋮----
cdist = np.zeros(path.shape[1])
⋮----
result = []
⋮----
x = np.interp(obs["distance"], cdist, path[0])
y = np.interp(obs["distance"], cdist, path[1])
⋮----
idx = max(
seg_dx = path[0, idx + 1] - path[0, idx]
seg_dy = path[1, idx + 1] - path[1, idx]
seg_len = np.hypot(seg_dx, seg_dy)
⋮----
tx = seg_dx / seg_len
ty = seg_dy / seg_len
vx = tx * obs["speed"]
vy = ty * obs["speed"]
lateral = obs.get("lateral_offset", 0.0)
⋮----
dx = current_state[0] - path[0, :]
dy = current_state[1] - path[1, :]
distances = np.hypot(dx, dy)
idx = np.argmin(distances)
⋮----
idx_start = idx - 1
idx_end = idx
⋮----
idx_start = idx
idx_end = idx + 1
⋮----
tx = path[0, idx_end] - path[0, idx_start]
ty = path[1, idx_end] - path[1, idx_start]
seg_len = np.hypot(tx, ty)
⋮----
vx = current_state[0] - path[0, idx]
vy = current_state[1] - path[1, idx]
⋮----
cte = (vy * tx) - (vx * ty)
⋮----
cte = distances[idx]
⋮----
target_heading = path[2, idx_start]
heading_err = (current_state[3] - target_heading + np.pi) % (2.0 * np.pi) - np.pi
⋮----
closest = None
closest_dist = float("inf")
fov_rad = np.radians(fov_degrees)
⋮----
dx = obs_x - robot_x
dy = obs_y - robot_y
d = np.hypot(dx, dy)
⋮----
dist_to_edge = max(0.0, d - obs_r)
⋮----
rel_angle = (np.arctan2(dy, dx) - robot_heading + np.pi) % (2.0 * np.pi) - np.pi
angle_to_obs_center = abs(rel_angle)
angular_radius = np.arcsin(obs_r / d)
⋮----
closest_dist = dist_to_edge
closest = obs
````

## File: mpc_python/models/mushr/cars/base_car/buddy.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="buddy_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="buddy_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="buddy_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="buddy_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="buddy_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="buddy_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="buddy_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="buddy" pos="0.0 2.0 0.0" euler="0 0 0.0">
      <camera name="buddy_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="buddy_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="buddy_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="buddy_mushr_base_nano"/>
      <geom name="buddy_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="buddy_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="buddy_mushr_ydlidar"/>
      <body name="buddy_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="buddy_steering" name="buddy_steering_wheel"/>
        <geom class="buddy_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="buddy_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="buddy_steering" name="buddy_wheel_fl_steering"/>
        <joint class="buddy_throttle" name="buddy_wheel_fl_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="buddy_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="buddy_steering" name="buddy_wheel_fr_steering"/>
        <joint class="buddy_throttle" name="buddy_wheel_fr_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="buddy_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="buddy_throttle" name="buddy_wheel_bl_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="buddy_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="buddy_throttle" name="buddy_wheel_br_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="buddy_steering" kp="25.0" name="buddy_steering_pos" joint="buddy_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="buddy_throttle_velocity" tendon="buddy_throttle"/>
  </actuator>
  <equality>
    <joint joint1="buddy_wheel_fl_steering" joint2="buddy_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="buddy_wheel_fr_steering" joint2="buddy_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="buddy_throttle">
      <joint joint="buddy_wheel_fl_throttle" coef="0.25"/>
      <joint joint="buddy_wheel_fr_throttle" coef="0.25"/>
      <joint joint="buddy_wheel_bl_throttle" coef="0.25"/>
      <joint joint="buddy_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="buddy_accelerometer" site="buddy_imu" />
    <gyro name="buddy_gyro" site="buddy_imu" />
    <velocimeter name="buddy_velocimeter" site="buddy_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car/car1.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car1_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car1_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car1_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car1_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car1_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car1_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car1_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car1" pos="0.0 1.0 0.0" euler="0 0 0.0">
      <camera name="car1_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car1_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car1_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car1_mushr_base_nano"/>
      <geom name="car1_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car1_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car1_mushr_ydlidar"/>
      <body name="car1_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car1_steering" name="car1_steering_wheel"/>
        <geom class="car1_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car1_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car1_steering" name="car1_wheel_fl_steering"/>
        <joint class="car1_throttle" name="car1_wheel_fl_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car1_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car1_steering" name="car1_wheel_fr_steering"/>
        <joint class="car1_throttle" name="car1_wheel_fr_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car1_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car1_throttle" name="car1_wheel_bl_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car1_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car1_throttle" name="car1_wheel_br_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car1_steering" kp="25.0" name="car1_steering_pos" joint="car1_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car1_throttle_velocity" tendon="car1_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car1_wheel_fl_steering" joint2="car1_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car1_wheel_fr_steering" joint2="car1_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car1_throttle">
      <joint joint="car1_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car1_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car1_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car1_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car1_accelerometer" site="car1_imu" />
    <gyro name="car1_gyro" site="car1_imu" />
    <velocimeter name="car1_velocimeter" site="car1_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car/car2.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car2_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car2_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car2_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car2_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car2_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car2_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car2_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car2" pos="0.0 0.0 0.0" euler="0 0 0.0">
      <camera name="car2_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car2_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car2_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car2_mushr_base_nano"/>
      <geom name="car2_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car2_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car2_mushr_ydlidar"/>
      <body name="car2_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car2_steering" name="car2_steering_wheel"/>
        <geom class="car2_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car2_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car2_steering" name="car2_wheel_fl_steering"/>
        <joint class="car2_throttle" name="car2_wheel_fl_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car2_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car2_steering" name="car2_wheel_fr_steering"/>
        <joint class="car2_throttle" name="car2_wheel_fr_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car2_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car2_throttle" name="car2_wheel_bl_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car2_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car2_throttle" name="car2_wheel_br_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car2_steering" kp="25.0" name="car2_steering_pos" joint="car2_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car2_throttle_velocity" tendon="car2_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car2_wheel_fl_steering" joint2="car2_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car2_wheel_fr_steering" joint2="car2_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car2_throttle">
      <joint joint="car2_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car2_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car2_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car2_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car2_accelerometer" site="car2_imu" />
    <gyro name="car2_gyro" site="car2_imu" />
    <velocimeter name="car2_velocimeter" site="car2_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car/car3.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car3_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car3_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car3_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car3_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car3_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car3_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car3_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car3" pos="0.0 -1.0 0.0" euler="0 0 0.0">
      <camera name="car3_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car3_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car3_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car3_mushr_base_nano"/>
      <geom name="car3_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car3_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car3_mushr_ydlidar"/>
      <body name="car3_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car3_steering" name="car3_steering_wheel"/>
        <geom class="car3_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car3_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car3_steering" name="car3_wheel_fl_steering"/>
        <joint class="car3_throttle" name="car3_wheel_fl_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car3_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car3_steering" name="car3_wheel_fr_steering"/>
        <joint class="car3_throttle" name="car3_wheel_fr_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car3_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car3_throttle" name="car3_wheel_bl_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car3_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car3_throttle" name="car3_wheel_br_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car3_steering" kp="25.0" name="car3_steering_pos" joint="car3_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car3_throttle_velocity" tendon="car3_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car3_wheel_fl_steering" joint2="car3_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car3_wheel_fr_steering" joint2="car3_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car3_throttle">
      <joint joint="car3_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car3_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car3_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car3_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car3_accelerometer" site="car3_imu" />
    <gyro name="car3_gyro" site="car3_imu" />
    <velocimeter name="car3_velocimeter" site="car3_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car/car4.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car4_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car4_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car4_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car4_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car4_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car4_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car4_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car4" pos="0.0 -2.0 0.0" euler="0 0 0.0">
      <camera name="car4_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car4_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car4_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car4_mushr_base_nano"/>
      <geom name="car4_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car4_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car4_mushr_ydlidar"/>
      <body name="car4_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car4_steering" name="car4_steering_wheel"/>
        <geom class="car4_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car4_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car4_steering" name="car4_wheel_fl_steering"/>
        <joint class="car4_throttle" name="car4_wheel_fl_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car4_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car4_steering" name="car4_wheel_fr_steering"/>
        <joint class="car4_throttle" name="car4_wheel_fr_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car4_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car4_throttle" name="car4_wheel_bl_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car4_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car4_throttle" name="car4_wheel_br_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car4_steering" kp="25.0" name="car4_steering_pos" joint="car4_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car4_throttle_velocity" tendon="car4_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car4_wheel_fl_steering" joint2="car4_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car4_wheel_fr_steering" joint2="car4_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car4_throttle">
      <joint joint="car4_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car4_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car4_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car4_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car4_accelerometer" site="car4_imu" />
    <gyro name="car4_gyro" site="car4_imu" />
    <velocimeter name="car4_velocimeter" site="car4_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car/car5.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car5_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car5_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car5_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car5_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car5_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car5_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car5_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car5" pos="0.0 -3.0 0.0" euler="0 0 0.0">
      <camera name="car5_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car5_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car5_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car5_mushr_base_nano"/>
      <geom name="car5_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car5_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car5_mushr_ydlidar"/>
      <body name="car5_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car5_steering" name="car5_steering_wheel"/>
        <geom class="car5_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car5_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car5_steering" name="car5_wheel_fl_steering"/>
        <joint class="car5_throttle" name="car5_wheel_fl_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car5_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car5_steering" name="car5_wheel_fr_steering"/>
        <joint class="car5_throttle" name="car5_wheel_fr_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car5_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car5_throttle" name="car5_wheel_bl_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car5_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car5_throttle" name="car5_wheel_br_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car5_steering" kp="25.0" name="car5_steering_pos" joint="car5_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car5_throttle_velocity" tendon="car5_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car5_wheel_fl_steering" joint2="car5_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car5_wheel_fr_steering" joint2="car5_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car5_throttle">
      <joint joint="car5_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car5_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car5_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car5_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car5_accelerometer" site="car5_imu" />
    <gyro name="car5_gyro" site="car5_imu" />
    <velocimeter name="car5_velocimeter" site="car5_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car/goose.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="goose_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="goose_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="goose_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="goose_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="goose_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="goose_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="goose_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="goose" pos="0.0 3.0 0.0" euler="0 0 0.0">
      <camera name="goose_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="goose_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="goose_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="goose_mushr_base_nano"/>
      <geom name="goose_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="goose_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="goose_mushr_ydlidar"/>
      <body name="goose_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="goose_steering" name="goose_steering_wheel"/>
        <geom class="goose_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="goose_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="goose_steering" name="goose_wheel_fl_steering"/>
        <joint class="goose_throttle" name="goose_wheel_fl_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="goose_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="goose_steering" name="goose_wheel_fr_steering"/>
        <joint class="goose_throttle" name="goose_wheel_fr_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="goose_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="goose_throttle" name="goose_wheel_bl_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="goose_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="goose_throttle" name="goose_wheel_br_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="goose_steering" kp="25.0" name="goose_steering_pos" joint="goose_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="goose_throttle_velocity" tendon="goose_throttle"/>
  </actuator>
  <equality>
    <joint joint1="goose_wheel_fl_steering" joint2="goose_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="goose_wheel_fr_steering" joint2="goose_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="goose_throttle">
      <joint joint="goose_wheel_fl_throttle" coef="0.25"/>
      <joint joint="goose_wheel_fr_throttle" coef="0.25"/>
      <joint joint="goose_wheel_bl_throttle" coef="0.25"/>
      <joint joint="goose_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="goose_accelerometer" site="goose_imu" />
    <gyro name="goose_gyro" site="goose_imu" />
    <velocimeter name="goose_velocimeter" site="goose_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/buddy.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="buddy_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="buddy_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="buddy_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="buddy_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="buddy_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="buddy_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="buddy_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="buddy" pos="0.0 2.0 0.0" euler="0 0 0.0">
      <camera name="buddy_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="buddy_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="buddy_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="buddy_mushr_base_nano"/>
      <geom name="buddy_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="buddy_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="buddy_mushr_ydlidar"/>
      <geom name="buddy_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="buddy_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="buddy_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="buddy_steering" name="buddy_steering_wheel"/>
        <geom class="buddy_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="buddy_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="buddy_steering" name="buddy_wheel_fl_steering"/>
        <joint class="buddy_throttle" name="buddy_wheel_fl_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="buddy_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="buddy_steering" name="buddy_wheel_fr_steering"/>
        <joint class="buddy_throttle" name="buddy_wheel_fr_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="buddy_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="buddy_throttle" name="buddy_wheel_bl_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="buddy_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="buddy_throttle" name="buddy_wheel_br_throttle"/>
        <geom class="buddy_wheel"/>
        <geom class="buddy_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="buddy_steering" kp="25.0" name="buddy_steering_pos" joint="buddy_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="buddy_throttle_velocity" tendon="buddy_throttle"/>
  </actuator>
  <equality>
    <joint joint1="buddy_wheel_fl_steering" joint2="buddy_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="buddy_wheel_fr_steering" joint2="buddy_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="buddy_throttle">
      <joint joint="buddy_wheel_fl_throttle" coef="0.25"/>
      <joint joint="buddy_wheel_fr_throttle" coef="0.25"/>
      <joint joint="buddy_wheel_bl_throttle" coef="0.25"/>
      <joint joint="buddy_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="buddy_accelerometer" site="buddy_imu" />
    <gyro name="buddy_gyro" site="buddy_imu" />
    <velocimeter name="buddy_velocimeter" site="buddy_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/car1.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car1_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car1_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car1_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car1_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car1_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car1_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car1_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car1" pos="0.0 1.0 0.0" euler="0 0 0.0">
      <camera name="car1_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car1_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car1_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car1_mushr_base_nano"/>
      <geom name="car1_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car1_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car1_mushr_ydlidar"/>
      <geom name="car1_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="car1_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="car1_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car1_steering" name="car1_steering_wheel"/>
        <geom class="car1_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car1_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car1_steering" name="car1_wheel_fl_steering"/>
        <joint class="car1_throttle" name="car1_wheel_fl_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car1_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car1_steering" name="car1_wheel_fr_steering"/>
        <joint class="car1_throttle" name="car1_wheel_fr_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car1_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car1_throttle" name="car1_wheel_bl_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car1_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car1_throttle" name="car1_wheel_br_throttle"/>
        <geom class="car1_wheel"/>
        <geom class="car1_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car1_steering" kp="25.0" name="car1_steering_pos" joint="car1_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car1_throttle_velocity" tendon="car1_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car1_wheel_fl_steering" joint2="car1_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car1_wheel_fr_steering" joint2="car1_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car1_throttle">
      <joint joint="car1_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car1_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car1_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car1_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car1_accelerometer" site="car1_imu" />
    <gyro name="car1_gyro" site="car1_imu" />
    <velocimeter name="car1_velocimeter" site="car1_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/car2.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car2_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car2_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car2_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car2_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car2_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car2_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car2_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car2" pos="0.0 0.0 0.0" euler="0 0 0.0">
      <camera name="car2_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car2_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car2_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car2_mushr_base_nano"/>
      <geom name="car2_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car2_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car2_mushr_ydlidar"/>
      <geom name="car2_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="car2_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="car2_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car2_steering" name="car2_steering_wheel"/>
        <geom class="car2_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car2_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car2_steering" name="car2_wheel_fl_steering"/>
        <joint class="car2_throttle" name="car2_wheel_fl_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car2_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car2_steering" name="car2_wheel_fr_steering"/>
        <joint class="car2_throttle" name="car2_wheel_fr_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car2_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car2_throttle" name="car2_wheel_bl_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car2_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car2_throttle" name="car2_wheel_br_throttle"/>
        <geom class="car2_wheel"/>
        <geom class="car2_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car2_steering" kp="25.0" name="car2_steering_pos" joint="car2_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car2_throttle_velocity" tendon="car2_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car2_wheel_fl_steering" joint2="car2_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car2_wheel_fr_steering" joint2="car2_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car2_throttle">
      <joint joint="car2_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car2_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car2_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car2_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car2_accelerometer" site="car2_imu" />
    <gyro name="car2_gyro" site="car2_imu" />
    <velocimeter name="car2_velocimeter" site="car2_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/car3.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car3_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car3_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car3_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car3_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car3_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car3_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car3_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car3" pos="0.0 -1.0 0.0" euler="0 0 0.0">
      <camera name="car3_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car3_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car3_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car3_mushr_base_nano"/>
      <geom name="car3_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car3_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car3_mushr_ydlidar"/>
      <geom name="car3_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="car3_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="car3_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car3_steering" name="car3_steering_wheel"/>
        <geom class="car3_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car3_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car3_steering" name="car3_wheel_fl_steering"/>
        <joint class="car3_throttle" name="car3_wheel_fl_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car3_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car3_steering" name="car3_wheel_fr_steering"/>
        <joint class="car3_throttle" name="car3_wheel_fr_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car3_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car3_throttle" name="car3_wheel_bl_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car3_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car3_throttle" name="car3_wheel_br_throttle"/>
        <geom class="car3_wheel"/>
        <geom class="car3_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car3_steering" kp="25.0" name="car3_steering_pos" joint="car3_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car3_throttle_velocity" tendon="car3_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car3_wheel_fl_steering" joint2="car3_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car3_wheel_fr_steering" joint2="car3_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car3_throttle">
      <joint joint="car3_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car3_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car3_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car3_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car3_accelerometer" site="car3_imu" />
    <gyro name="car3_gyro" site="car3_imu" />
    <velocimeter name="car3_velocimeter" site="car3_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/car4.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car4_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car4_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car4_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car4_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car4_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car4_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car4_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car4" pos="0.0 -2.0 0.0" euler="0 0 0.0">
      <camera name="car4_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car4_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car4_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car4_mushr_base_nano"/>
      <geom name="car4_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car4_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car4_mushr_ydlidar"/>
      <geom name="car4_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="car4_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="car4_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car4_steering" name="car4_steering_wheel"/>
        <geom class="car4_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car4_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car4_steering" name="car4_wheel_fl_steering"/>
        <joint class="car4_throttle" name="car4_wheel_fl_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car4_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car4_steering" name="car4_wheel_fr_steering"/>
        <joint class="car4_throttle" name="car4_wheel_fr_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car4_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car4_throttle" name="car4_wheel_bl_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car4_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car4_throttle" name="car4_wheel_br_throttle"/>
        <geom class="car4_wheel"/>
        <geom class="car4_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car4_steering" kp="25.0" name="car4_steering_pos" joint="car4_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car4_throttle_velocity" tendon="car4_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car4_wheel_fl_steering" joint2="car4_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car4_wheel_fr_steering" joint2="car4_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car4_throttle">
      <joint joint="car4_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car4_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car4_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car4_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car4_accelerometer" site="car4_imu" />
    <gyro name="car4_gyro" site="car4_imu" />
    <velocimeter name="car4_velocimeter" site="car4_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/car5.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="car5_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="car5_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="car5_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="car5_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="car5_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="car5_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="car5_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="car5" pos="0.0 -3.0 0.0" euler="0 0 0.0">
      <camera name="car5_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="car5_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="car5_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="car5_mushr_base_nano"/>
      <geom name="car5_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="car5_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="car5_mushr_ydlidar"/>
      <geom name="car5_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="car5_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="car5_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="car5_steering" name="car5_steering_wheel"/>
        <geom class="car5_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="car5_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="car5_steering" name="car5_wheel_fl_steering"/>
        <joint class="car5_throttle" name="car5_wheel_fl_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car5_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="car5_steering" name="car5_wheel_fr_steering"/>
        <joint class="car5_throttle" name="car5_wheel_fr_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car5_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="car5_throttle" name="car5_wheel_bl_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="car5_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="car5_throttle" name="car5_wheel_br_throttle"/>
        <geom class="car5_wheel"/>
        <geom class="car5_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="car5_steering" kp="25.0" name="car5_steering_pos" joint="car5_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="car5_throttle_velocity" tendon="car5_throttle"/>
  </actuator>
  <equality>
    <joint joint1="car5_wheel_fl_steering" joint2="car5_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="car5_wheel_fr_steering" joint2="car5_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="car5_throttle">
      <joint joint="car5_wheel_fl_throttle" coef="0.25"/>
      <joint joint="car5_wheel_fr_throttle" coef="0.25"/>
      <joint joint="car5_wheel_bl_throttle" coef="0.25"/>
      <joint joint="car5_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="car5_accelerometer" site="car5_imu" />
    <gyro name="car5_gyro" site="car5_imu" />
    <velocimeter name="car5_velocimeter" site="car5_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/pusher_car/goose.xml
````xml
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="goose_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="goose_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="goose_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="goose_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="goose_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="goose_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="goose_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="goose" pos="0.0 3.0 0.0" euler="0 0 0.0">
      <camera name="goose_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>
      <camera name="goose_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="goose_imu" pos="-0.005 0 .165"/>
      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="goose_mushr_base_nano"/>
      <geom name="goose_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="goose_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="goose_mushr_ydlidar"/>
      <geom name="goose_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <geom name="goose_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>
      <body name="goose_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="goose_steering" name="goose_steering_wheel"/>
        <geom class="goose_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>
      <body name="goose_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="goose_steering" name="goose_wheel_fl_steering"/>
        <joint class="goose_throttle" name="goose_wheel_fl_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="goose_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="goose_steering" name="goose_wheel_fr_steering"/>
        <joint class="goose_throttle" name="goose_wheel_fr_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="goose_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="goose_throttle" name="goose_wheel_bl_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="goose_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="goose_throttle" name="goose_wheel_br_throttle"/>
        <geom class="goose_wheel"/>
        <geom class="goose_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="goose_steering" kp="25.0" name="goose_steering_pos" joint="goose_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="goose_throttle_velocity" tendon="goose_throttle"/>
  </actuator>
  <equality>
    <joint joint1="goose_wheel_fl_steering" joint2="goose_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>
    <joint joint1="goose_wheel_fr_steering" joint2="goose_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="goose_throttle">
      <joint joint="goose_wheel_fl_throttle" coef="0.25"/>
      <joint joint="goose_wheel_fr_throttle" coef="0.25"/>
      <joint joint="goose_wheel_bl_throttle" coef="0.25"/>
      <joint joint="goose_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="goose_accelerometer" site="goose_imu" />
    <gyro name="goose_gyro" site="goose_imu" />
    <velocimeter name="goose_velocimeter" site="goose_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/base_car.template
````
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="{C}_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="{C}_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="{C}_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="{C}_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="{C}_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="{C}_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="{C}_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="{C}" pos="{InitX} {InitY} 0.0" euler="0 0 {InitT}">
      <camera name="{C}_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>

      <camera name="{C}_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="{C}_imu" pos="-0.005 0 .165"/>

      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="{C}_mushr_base_nano"/>
      <geom name="{C}_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="{C}_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="{C}_mushr_ydlidar"/>

      <body name="{C}_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="{C}_steering" name="{C}_steering_wheel"/>
        <geom class="{C}_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>

      <body name="{C}_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="{C}_steering" name="{C}_wheel_fl_steering"/>
        <joint class="{C}_throttle" name="{C}_wheel_fl_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="{C}_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="{C}_steering" name="{C}_wheel_fr_steering"/>
        <joint class="{C}_throttle" name="{C}_wheel_fr_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="{C}_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="{C}_throttle" name="{C}_wheel_bl_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="{C}_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="{C}_throttle" name="{C}_wheel_br_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="{C}_steering" kp="25.0" name="{C}_steering_pos" joint="{C}_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="{C}_throttle_velocity" tendon="{C}_throttle"/>
  </actuator>
  <equality>
    <!-- taylor expansion of delta_l = arctan(L/(L/tan(delta) - W/2)) with L,W in reference to kinematic car model -->
    <joint joint1="{C}_wheel_fl_steering" joint2="{C}_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>

    <!-- taylor expansion of delta_r = arctan(L/(L/tan(delta) + W/2)) with L,W in reference to kinematic car model -->
    <joint joint1="{C}_wheel_fr_steering" joint2="{C}_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="{C}_throttle">
      <joint joint="{C}_wheel_fl_throttle" coef="0.25"/>
      <joint joint="{C}_wheel_fr_throttle" coef="0.25"/>
      <joint joint="{C}_wheel_bl_throttle" coef="0.25"/>
      <joint joint="{C}_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="{C}_accelerometer" site="{C}_imu" />
    <gyro name="{C}_gyro" site="{C}_imu" />
    <velocimeter name="{C}_velocimeter" site="{C}_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/cars/make_car_model.py
````python
MODELS = ["base_car", "pusher_car"]
⋮----
MAPPING = ["{C}", "{InitX}", "{InitY}", "{InitT}"]
ENTRIES = [
⋮----
car_data = f.readlines()
⋮----
name = e[MAPPING.index("{C}")]
⋮----
line = line.replace(k, str(v))
````

## File: mpc_python/models/mushr/cars/pusher_car.template
````
<mujoco>
  <compiler meshdir="cars/meshes" />
  <asset>
    <mesh name="{C}_mushr_base_nano" file="mushr_base_nano.stl"/>
    <mesh name="{C}_mushr_wheel" file="mushr_wheel.stl"/>
    <mesh name="{C}_mushr_ydlidar" file="mushr_ydlidar.stl"/>
  </asset>
  <default>
      <default class="{C}_wheel">
      <geom fitscale="1.2" type="ellipsoid" friction="2 0.005 0.0001" contype="1" conaffinity="0" mesh="{C}_mushr_wheel" mass="0.498952"/>
    </default>
    <default class="{C}_steering">
      <joint type="hinge" axis="0 0 1" limited="true" frictionloss="0.01" damping="0.001" armature="0.0002" range="-0.38 0.38"/>
    </default>
    <default class="{C}_throttle">
      <joint type="hinge" axis="0 1 0" frictionloss="0.001" damping="0.01" armature="0.01" limited="false"/>
    </default>
  </default>
  <worldbody>
    <body name="{C}" pos="{InitX} {InitY} 0.0" euler="0 0 {InitT}">
      <camera name="{C}_third_person" mode="fixed" pos="-1 0 1" xyaxes="0 -1 0 0.707 0 0.707"/>
      <joint type="free"/>

      <camera name="{C}_realsense_d435i" mode="fixed" pos="-0.005 0 .165" euler="0 4.712 4.712"/>
      <site name="{C}_imu" pos="-0.005 0 .165"/>

      <geom pos="0 0 0.094655" type="mesh" mass="3.542137" mesh="{C}_mushr_base_nano"/>
      <geom name="{C}_realsense_d435i" size="0.012525 0.045 0.0125" pos="0.0123949 0 0.162178" mass="0.072" type="box"/>
      <geom name="{C}_ydlidar" pos="-0.035325 0 0.202405" type="mesh" mass="0.180" mesh="{C}_mushr_ydlidar"/>

      <geom name="{C}_pusher_connector" pos="0.2073 0 0.063" type="box" size="0.0025 0.025 0.02" mass="0.01" />
      <!-- x=1cm, y=22cm, z=7cm -->
      <geom name="{C}_pusher" pos="0.215 0 0.048" type="box" size=".005 .11 .035" mass="0.05"/>

      <body name="{C}_steering_wheel" pos="0.1385 0 0.0488">
        <joint class="{C}_steering" name="{C}_steering_wheel"/>
        <geom class="{C}_wheel" contype="0" conaffinity="0" mass="0.01" rgba="0 0 0 0.01"/>
      </body>

      <body name="{C}_wheel_fl" pos="0.1385 0.115 0.0488">
        <joint class="{C}_steering" name="{C}_wheel_fl_steering"/>
        <joint class="{C}_throttle" name="{C}_wheel_fl_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="{C}_wheel_fr" pos="0.1385 -0.115 0.0488">
        <joint class="{C}_steering" name="{C}_wheel_fr_steering"/>
        <joint class="{C}_throttle" name="{C}_wheel_fr_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="{C}_wheel_bl" pos="-0.158 0.115 0.0488">
        <joint class="{C}_throttle" name="{C}_wheel_bl_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
      <body name="{C}_wheel_br" pos="-0.158 -0.115 0.0488">
        <joint class="{C}_throttle" name="{C}_wheel_br_throttle"/>
        <geom class="{C}_wheel"/>
        <geom class="{C}_wheel" type="mesh" contype="0" conaffinity="0" group="1" rgba="1 1 1 0.3"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <position class="{C}_steering" kp="25.0" name="{C}_steering_pos" joint="{C}_steering_wheel"/>
    <velocity kv="100" gear="0.04" forcelimited="true" forcerange="-500 500" name="{C}_throttle_velocity" tendon="{C}_throttle"/>
  </actuator>
  <equality>
    <!-- taylor expansion of delta_l = arctan(L/(L/tan(delta) - W/2)) with L,W in reference to kinematic car model -->
    <joint joint1="{C}_wheel_fl_steering" joint2="{C}_steering_wheel" polycoef="0 1 0.375 0.140625 -0.0722656"/>

    <!-- taylor expansion of delta_r = arctan(L/(L/tan(delta) + W/2)) with L,W in reference to kinematic car model -->
    <joint joint1="{C}_wheel_fr_steering" joint2="{C}_steering_wheel" polycoef="0 1 -0.375 0.140625 0.0722656"/>
  </equality>
  <tendon>
    <fixed name="{C}_throttle">
      <joint joint="{C}_wheel_fl_throttle" coef="0.25"/>
      <joint joint="{C}_wheel_fr_throttle" coef="0.25"/>
      <joint joint="{C}_wheel_bl_throttle" coef="0.25"/>
      <joint joint="{C}_wheel_br_throttle" coef="0.25"/>
    </fixed>
  </tendon>
  <sensor>
    <accelerometer name="{C}_accelerometer" site="{C}_imu" />
    <gyro name="{C}_gyro" site="{C}_imu" />
    <velocimeter name="{C}_velocimeter" site="{C}_imu" />
  </sensor>
</mujoco>
````

## File: mpc_python/models/mushr/mush_nano.xml
````xml
<mujoco model="mushr_nano">
  <compiler angle="radian" />
  <size njmax="500" nconmax="100"/>
  <option timestep="0.01"/>
  <include file="cars/base_car/buddy.xml"/>
  <asset>
    <texture name="texplane" type="2d" builtin="checker" rgb1="0.26 0.12 0.36" rgb2="0.23 0.09 0.33" width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>
    <texture name="texgeom" type="cube" builtin="flat" mark="cross" width="127" height="1278" rgb1="0.8 0.6 0.4" rgb2="0.8 0.6 0.4" markrgb="1 1 1" random="0.01"/>
    <material name="matplane" reflectance="0.3" texture="texplane" texrepeat="1 1" texuniform="true"/>
    <material name="matgeom" texture="texgeom" texuniform="true" rgba="0.8 0.6 .4 1"/>
  </asset>
  <visual>
    <headlight ambient="0.6 0.6 0.6" diffuse="0.5 0.5 0.5" specular="0.2 0.2 0.2"/>
    <map znear="0.001" />
  </visual>
  <worldbody>
    <geom contype="1" friction=".5 0.005 0.0001" name="floor" pos="0 0 0" size="0 0 .25" type="plane" material="matplane" condim="3"/> -->
  </worldbody>
</mujoco>
````

## File: mpc_python/mpc_demo_mujoco.py
````python
class SharedData
⋮----
def __init__(self) -> None
⋮----
start_time = time.time()
⋮----
current_state = shared.state.copy()
global_obs = (
last_control = (shared.mpc_accel, shared.mpc_steer)
elapsed = shared.mpc_elapsed
⋮----
goal_dist = np.sqrt(
⋮----
pred_state = current_state.copy()
v = pred_state[2]
theta = pred_state[3]
a = last_control[0]
delta = last_control[1]
L = mpc.wheelbase
⋮----
target = get_ref_trajectory(
pred_ego_state = [0.0, 0.0, pred_state[2], 0.0]
⋮----
dx = gx - pred_state[0]
dy = gy - pred_state[1]
⋮----
pred_obstacle = (
⋮----
pred_obstacle = None
⋮----
control = (u_mpc[0, 0], u_mpc[1, 0])
elapsed = time.time() - start_time
⋮----
elapsed_total = time.time() - start_time
sleep_time = max(0.0, mpc.dt - elapsed_total)
⋮----
def body_id(model: mujoco.MjModel, name: str) -> int
⋮----
i = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
⋮----
def get_state(data: mujoco.MjData, bid: int) -> npt.NDArray[np.float64]
⋮----
rot = data.xmat[bid].reshape(3, 3)
yaw = np.arctan2(rot[1, 0], rot[0, 0])
speed = np.linalg.norm(data.qvel[0:2])
⋮----
def draw_path(viewer: mujoco.viewer.MjViewer, path: npt.NDArray[np.float64]) -> None
⋮----
g = viewer.user_scn.geoms[viewer.user_scn.ngeom]
⋮----
p1 = np.array([path[0, i], path[1, i], 0.03], dtype=np.float64)
p2 = np.array([path[0, i + 1], path[1, i + 1], 0.03], dtype=np.float64)
⋮----
alpha = (i + 1) / len(x_hist) * 0.8
⋮----
p1 = np.array([x_hist[i], y_hist[i], 0.005], dtype=np.float64)
p2 = np.array([x_hist[i + 1], y_hist[i + 1], 0.005], dtype=np.float64)
⋮----
def draw_obstacle(viewer: mujoco.viewer.MjViewer, obstacles) -> None
⋮----
fov_rad = np.radians(fov_deg)
right_angle = heading - fov_rad / 2.0
left_angle = heading + fov_rad / 2.0
⋮----
right_end = np.array(
left_end = np.array(
origin = np.array([x, y, 0.0])
⋮----
rgba = np.array([0.8, 0.8, 0, 0.2], dtype=np.float32)
⋮----
num_arc_pts = 20
prev = None
⋮----
t = i / num_arc_pts
angle = right_angle + t * fov_rad
p = np.array(
⋮----
prev = p
⋮----
def main() -> None
⋮----
model_path = pathlib.Path(__file__).parent / "models" / "mushr" / "mush_nano.xml"
m = mujoco.MjModel.from_xml_path(str(model_path))
d = mujoco.MjData(m)
bid = body_id(m, "buddy")
⋮----
sim_config = yaml.safe_load(
start = sim_config["start"]
target_speed = sim_config["target_speed"]
sensor_max_range = sim_config["sensor"]["max_range"]
sensor_fov_deg = sim_config["sensor"]["fov_deg"]
goal_threshold = sim_config["goal_threshold"]
⋮----
path = compute_path_from_wp(
⋮----
path_obstacles = list(sim_config["obstacles"])
⋮----
dynamic_obstacle_list = update_path_obstacles(path_obstacles, path, 0.0)
mpc = MPC(
⋮----
steer_jnt = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, "buddy_steering_wheel")
steer_qaddr = m.jnt_qposadr[steer_jnt]
⋮----
shared = SharedData()
mpc_thread = threading.Thread(
⋮----
shutdown_flag = threading.Event()
⋮----
def handle_shutdown(signum, frame)
⋮----
fps = 60.0
render_dt = 1.0 / fps
⋮----
x_hist = []
y_hist = []
cte_hist = []
heading_error_hist = []
cte_rmse = -1
heading_rmse = -1
⋮----
sim_start_time = time.perf_counter()
⋮----
# Idle until the user closes the window or forces a KeyboardInterrupt
⋮----
elapsed_real_time = time.perf_counter() - sim_start_time
⋮----
current_state = get_state(d, bid)
⋮----
# External obstacle detection pipeline (global frame)
⋮----
detected_obs = detect_obstacle_camera(
⋮----
detected_obs = None
⋮----
# Sync with MPC Thread
⋮----
mpc_elapsed = shared.mpc_elapsed
mpc_accel = shared.mpc_accel
mpc_steer = shared.mpc_steer
x_mpc_world = shared.x_mpc_world
⋮----
# Log position etc...
⋮----
cte_rmse = np.sqrt(np.mean(np.square(cte_hist)))
heading_rmse = np.sqrt(np.mean(np.square(heading_error_hist)))
⋮----
# Step physics
⋮----
# ZERO-ORDER HOLD (ZOH)
# The MPC outputs a target steering angle.
# Since the low-level actuator (aka steering wheel PID) usually
# tracks position directly, we treat this command as a constant step.
# We hold it flat (Zero-Order Hold) across the entire window.
⋮----
# FIRST-ORDER HOLD (FOH)
# MuJoCo's wheel actuators expect a velocity command,
# but the MPC outputs an acceleration.
#
# If we applied a raw step jump to velocity (speed+=mpc_acc*DT), it would imply infinite acceleration.
# Instead, we integrate the acceleration command over every microscopic physics step. This smoothly ramps the
# velocity command over time, creating a First-Order Hold that perfectly mimics
# a real motor.
⋮----
# Update camera position to follow the car
⋮----
# re-draw markers
⋮----
# Update the HUD
actual_steer = np.degrees(d.qpos[steer_qaddr])
goal_dist = np.hypot(
⋮----
# Frame limiting (sleep just enough to hit 60 FPS)
time_until_next_frame = render_dt - (
````

## File: mpc_python/mpc_demo_nosim.py
````python
class MPCSim
⋮----
def __init__(self) -> None
⋮----
sim_config = yaml.safe_load(
start = sim_config["start"]
⋮----
gs = plt.GridSpec(3, 3)
⋮----
initial_obs = update_path_obstacles(self.path_obstacles, self.path, 0.0)
⋮----
c = plt.Circle(
⋮----
max_steer_deg = np.degrees(self.mpc.max_steer)
⋮----
def run(self) -> None
⋮----
dynamic_obs = update_path_obstacles(
⋮----
target = get_ref_trajectory(
⋮----
curr_state = np.array([0, 0, self.state[2], 0])
⋮----
dx = gx - self.state[0]
dy = gy - self.state[1]
⋮----
obs_ego = (
⋮----
obs_ego = None
⋮----
t0 = time.perf_counter()
⋮----
L = self.mpc.wheelbase
⋮----
def kinematics_model(x, t, u)
⋮----
dxdt = x[2] * np.cos(x[3])
dydt = x[2] * np.sin(x[3])
dvdt = u[0]
dthetadt = x[2] * np.tan(u[1]) / L
dqdt = [dxdt, dydt, dvdt, dthetadt]
⋮----
tspan = [0, dt]
new_state = odeint(kinematics_model, state, tspan, args=(u[:],))[1]
⋮----
def plot_sim(self) -> None
⋮----
current_obs = update_path_obstacles(self.path_obstacles, self.path, 0.0)
⋮----
half_fov = self.sensor_fov_deg / 2
theta1 = np.degrees(self.h_history[-1]) - half_fov
theta2 = np.degrees(self.h_history[-1]) + half_fov
⋮----
goal_dist = np.sqrt(
avoiding = (
⋮----
t = np.arange(len(self.a_history)) * self.mpc.dt
⋮----
def plot_car(ax: plt.Axes, x: float, y: float, yaw: float) -> plt.Line2D
⋮----
CAR_LENGTH = 0.5
CAR_WIDTH = 0.25
CAR_OFFSET = CAR_LENGTH
⋮----
outline = np.array(
⋮----
Rotm = np.array([[np.cos(yaw), np.sin(yaw)], [-np.sin(yaw), np.cos(yaw)]])
outline = (outline.T @ Rotm).T
⋮----
def do_sim() -> None
⋮----
sim = MPCSim()
````

## File: .gitignore
````
*.pyc
*.DS_Store
*.ipynb_checkpoints
````

## File: env.yml
````yaml
name: simulation
channels:
  - conda-forge
  - defaults
dependencies:
  - ipython
  - ipywidgets
  - jupyterlab
  - jupyterlab_server
  - nb_conda_kernels
  - nbconvert
  - nbformat
  - pip
  - python>=3.11
  - numpy
  - sympy
  - cvxpy
  - matplotlib
  - scipy
  - osqp
  - pyyaml
  - pip:
    - black>=24
````

## File: flake.lock
````
{
  "nodes": {
    "flake-utils": {
      "inputs": {
        "systems": "systems"
      },
      "locked": {
        "lastModified": 1731533236,
        "narHash": "sha256-l0KFg5HjrsfsO/JpG+r7fRrqm12kzFHyUHqHCVpMMbI=",
        "owner": "numtide",
        "repo": "flake-utils",
        "rev": "11707dc2f618dd54ca8739b309ec4fc024de578b",
        "type": "github"
      },
      "original": {
        "owner": "numtide",
        "repo": "flake-utils",
        "type": "github"
      }
    },
    "flake-utils_2": {
      "inputs": {
        "systems": "systems_2"
      },
      "locked": {
        "lastModified": 1731533236,
        "narHash": "sha256-l0KFg5HjrsfsO/JpG+r7fRrqm12kzFHyUHqHCVpMMbI=",
        "owner": "numtide",
        "repo": "flake-utils",
        "rev": "11707dc2f618dd54ca8739b309ec4fc024de578b",
        "type": "github"
      },
      "original": {
        "owner": "numtide",
        "repo": "flake-utils",
        "type": "github"
      }
    },
    "nixgl": {
      "inputs": {
        "flake-utils": "flake-utils_2",
        "nixpkgs": "nixpkgs"
      },
      "locked": {
        "lastModified": 1762090880,
        "narHash": "sha256-fbRQzIGPkjZa83MowjbD2ALaJf9y6KMDdJBQMKFeY/8=",
        "owner": "nix-community",
        "repo": "nixGL",
        "rev": "b6105297e6f0cd041670c3e8628394d4ee247ed5",
        "type": "github"
      },
      "original": {
        "owner": "nix-community",
        "repo": "nixGL",
        "type": "github"
      }
    },
    "nixpkgs": {
      "locked": {
        "lastModified": 1746378225,
        "narHash": "sha256-OeRSuL8PUjIfL3Q0fTbNJD/fmv1R+K2JAOqWJd3Oceg=",
        "owner": "nixos",
        "repo": "nixpkgs",
        "rev": "93e8cdce7afc64297cfec447c311470788131cd9",
        "type": "github"
      },
      "original": {
        "owner": "nixos",
        "repo": "nixpkgs",
        "type": "github"
      }
    },
    "nixpkgs_2": {
      "locked": {
        "lastModified": 1778443072,
        "narHash": "sha256-zi7/fsqM/kFdNuED//4WOCUtezGtKKqRNORjMvfwjnA=",
        "owner": "NixOS",
        "repo": "nixpkgs",
        "rev": "da5ad661ba4e5ef59ba743f0d112cbc30e474f32",
        "type": "github"
      },
      "original": {
        "owner": "NixOS",
        "ref": "nixos-unstable",
        "repo": "nixpkgs",
        "type": "github"
      }
    },
    "root": {
      "inputs": {
        "flake-utils": "flake-utils",
        "nixgl": "nixgl",
        "nixpkgs": "nixpkgs_2"
      }
    },
    "systems": {
      "locked": {
        "lastModified": 1681028828,
        "narHash": "sha256-Vy1rq5AaRuLzOxct8nz4T6wlgyUR7zLU309k9mBC768=",
        "owner": "nix-systems",
        "repo": "default",
        "rev": "da67096a3b9bf56a91d16901293e51ba5b49a27e",
        "type": "github"
      },
      "original": {
        "owner": "nix-systems",
        "repo": "default",
        "type": "github"
      }
    },
    "systems_2": {
      "locked": {
        "lastModified": 1681028828,
        "narHash": "sha256-Vy1rq5AaRuLzOxct8nz4T6wlgyUR7zLU309k9mBC768=",
        "owner": "nix-systems",
        "repo": "default",
        "rev": "da67096a3b9bf56a91d16901293e51ba5b49a27e",
        "type": "github"
      },
      "original": {
        "owner": "nix-systems",
        "repo": "default",
        "type": "github"
      }
    }
  },
  "root": "root",
  "version": 7
}
````

## File: flake.nix
````nix
{
  description = "MPC Python Demo - Model Predictive Control";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    nixgl.url = "github:nix-community/nixGL";  # GPU support
  };

  outputs = { self, nixpkgs, flake-utils, nixgl }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        nixgl-pkg = nixgl.packages.${system};

        # --- Python packages ---
        # core ones for running the demo, don't touch these
        core-python-pkgs = ps: with ps; [
          numpy
          matplotlib
          mujoco
          cvxpy
          scipy
          pyyaml
        ];

        # dev packages, add extra stuff here
        dev-python-pkgs = ps: with ps; [
            osqp
            sympy
            jupyterlab
            ipython
            ipywidgets
            nbformat
            nbconvert
            black
            ruff
          ];

        python-demo = pkgs.python3.withPackages core-python-pkgs;

        python-dev = pkgs.python3.withPackages (ps:
          (core-python-pkgs ps) ++ (dev-python-pkgs ps)
        );

        # --- System binaries ---
        dev-bin-pkgs = with pkgs; [
          # add here extra CLI tools for the dev shell
          # cmake, gdb, htop, just, ...
        ];

      in
      {
        devShells = {
          demo = pkgs.mkShell {
            buildInputs = [
              python-demo
              nixgl-pkg.nixGLDefault
            ];

            shellHook = ''
              echo "demo shell — bare deps to run the sim"
              echo ""
              echo "Run with GUI (MuJoCo):"
              echo "  nixGL python mpc_python/mpc_demo_mujoco.py"
              echo ""
              echo "Run without GUI:"
              echo "  python mpc_python/mpc_demo_nosim.py"
            '';
          };

          default = pkgs.mkShell {
            buildInputs = [
              python-dev
              nixgl-pkg.nixGLDefault
            ] ++ dev-bin-pkgs;

            shellHook = ''
              echo "full dev shell — deps + jupyter + dev tools"
              echo ""
              echo "Run with GUI (MuJoCo):"
              echo "  nixGL python mpc_python/mpc_demo_mujoco.py"
              echo ""
              echo "Run without GUI:"
              echo "  python mpc_python/mpc_demo_nosim.py"
              echo ""
              echo "Notebooks: jupyter lab"
              echo "Lint: ruff check ."
              echo "Format: black ."
            '';
          };
        };
        apps = {
          mujoco-demo = flake-utils.lib.mkApp {
            drv = pkgs.writeShellApplication {
              name = "mpc-mujoco-demo";
              runtimeInputs = [ python-demo nixgl-pkg.nixGLDefault ];
              text = "cd ${./.} && nixGL python mpc_python/mpc_demo_mujoco.py";
            };
          };
          nosim-demo = flake-utils.lib.mkApp {
            drv = pkgs.writeShellApplication {
              name = "mpc-nosim-demo";
              runtimeInputs = [ python-demo ];
              text = "cd ${./.} && python mpc_python/mpc_demo_nosim.py";
            };
          };
        };
      });
}
````

## File: LICENSE
````
MIT License

Copyright (c) 2022 mcarfagno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

## File: MUJOCO_LOG.TXT
````
Thu May 14 19:46:40 2026
ERROR: could not create window

Thu May 14 19:51:16 2026
ERROR: could not create window
````

## File: pyproject.toml
````toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "mpc-python"
version = "0.1.0"
description = "Model Predictive Control for path-following problems"
requires-python = ">=3.11"
dependencies = [
    "numpy<2",
    "matplotlib",
    "mujoco",
    "cvxpy",
    "scipy",
    "osqp",
    "sympy",
    "pyyaml",
]

[project.optional-dependencies]
notebook = [
    "jupyterlab>=4",
    "ipython",
    "ipywidgets",
    "nbformat",
    "nbconvert",
]
dev = [
    "black>=24",
    "ruff",
]

[tool.setuptools.packages.find]
where = ["."]
````

## File: README.md
````markdown
# mpc_python

A (hopefully) easy-to-follow Iterative MPC tracking controller built with CVXPY and paired with MuJoCo. Designed to help anyone looking to transition from basic control to real-time convex optimization.

<figure>
  <img src="img/banner.png" width="500" />
  <figcaption>MuJoCo simulation with the mushr car model</figcaption>
</figure>

This mainly uses **[CVXPY](https://www.cvxpy.org/)** to maintain a strict quadratic programming framework rather than relying on a non-linear solver like CasADi (which I love btw!). But, implementing an iMPC, we can still bridge the gap between convex optimization and real-world vehicle physics, allowing you to handle non-linear kinematics through iterative linearization.

Note: I've also preserved my original notebooks on Model Predictive Control for path-following problems here for historical context, a bit outdated.

This repo builds upon code and ideas from other open-source projects; please check them out in the Special Thanks section!

## Showcase

You can run the demo with MuJoCo and the mushr car or just python with no physics simulation:

<table>
  <tr>
    <td><figure><img src="img/demo-mujoco.gif" width="500" /><figcaption>MuJoCo simulation with the mushr car model (without obstacles)</figcaption></figure></td>
    <td><figure><img src="img/demo.gif" width="500" /><figcaption>Headless toy demo with dummy car (without obstacles)</figcaption></figure></td>
  </tr>
  <tr>
    <td><figure><img src="img/demo-mujoco_with_obs.gif" width="500" /><figcaption>MuJoCo simulation with static obstacle avoidance</figcaption></figure></td>
    <td><figure><img src="img/demo_with_obs.gif" width="500" /><figcaption>Headless toy demo with static obstacle avoidance</figcaption></figure></td>
  </tr>
  <tr>
    <td><figure><img src="img/demo-mujoco_with_moving_obs.gif" width="500" /><figcaption>MuJoCo simulation with moving obstacle avoidance</figcaption></figure></td>
    <td><figure><img src="img/demo_with_moving_obs.gif" width="500" /><figcaption>Headless toy demo with moving obstacle avoidance</figcaption></figure></td>
  </tr>
</table>

## Getting started

Here is a brief overview of the codebase:

```
mpc_python
├── config/
│   ├── mpc.yaml           # the configuration of the MPC. Start here!
│   └── simulation.yaml    # common configuration of the demos
└── mpc_python/
    ├── cvxpy_mpc/
    │   ├── cvxpy_mpc.py   # main mpc implementation
    │   └── utils.py
    ├── models/
    │   └── mushr/         # model from prl-mushr/mushr_mujoco_ros
    ├── mpc_demo_mujoco.py # mujoco demo entry point
    └── mpc_demo_nosim.py  # no physics demo entry point
```

There are a few ways to run this:

### Nix Flake ❄️

A [Nix flake](flake.nix) is provided for a reproducible development shell.

Just run the 2 examples below:
```bash
nix run --impure .#mujoco-demo
nix run .#nosim-demo
```

Otherwise, enter the development shell: this is heavier but also includes `jupyter lab` to experiment with the notebooks.
```bash
nix develop --impure
```

GUI demos require `nixGL` (auto-detects Intel/AMD/NVIDIA GPU):

```bash
nixGL python mpc_python/mpc_demo_mujoco.py
```

Headless demos run without it:

```bash
python mpc_python/mpc_demo_nosim.py
```

### Conda

```bash
conda env create -f env.yml
conda activate simulation
```

Then run the scripts:

```bash
python3 mpc_demo_mujoco.py
python3 mpc_demo_nosim.py
```

## Notebooks

1. **Model derivation** — analytical and numerical derivation ([1.0](notebooks/1.0-linearised-system-modelling.ipynb), [parametrized curves](notebooks/1.1-parametrized-path-curves.ipynb), [differential](notebooks/models/differential_model.ipynb), [motion model](notebooks/models/motion_model.ipynb))

2. **MPC** — implementation and testing of various tweaks ([2.0](notebooks/2.0-MPC-base.ipynb), [2.1](notebooks/2.1-MPC-with-iterative-linearization.ipynb), [2.2](notebooks/2.2-MPC-v2-car-reference-frame.ipynb), [2.3](notebooks/2.3-MPC-simplified.ipynb))

3. **Obstacle Avoidance** — halfplane constraints to avoid track collisions ([3.0](notebooks/3.0-MPC-v3-track-constrains.ipynb), [3.1](notebooks/3.1-better-track.ipynb)) — Still **work in progress**!

## References & Special Thanks :star: :
* [Prof. Borrelli - mpc papers and material](https://borrelli.me.berkeley.edu/pdfpub/IV_KinematicMPC_jason.pdf)
* [AtsushiSakai - pythonrobotics](https://github.com/AtsushiSakai/PythonRobotics/)
* [alexliniger - mpcc](https://github.com/alexliniger/MPCC) and his [paper](https://onlinelibrary.wiley.com/doi/abs/10.1002/oca.2123)
* [arex18 - rocket-lander](https://github.com/arex18/rocket-lander)
* [prl-mushr - mushr](https://github.com/prl-mushr/mushr_mujoco_ros) for the vehicle used
````

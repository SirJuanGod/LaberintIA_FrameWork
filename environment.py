import torch
import numpy as np
import genesis as gs
import pathlib

from genesis_forge import ManagedEnvironment
from genesis_forge.managers import (
    RewardManager,
    TerminationManager,
    EntityManager,
    ObservationManager,
    ActuatorManager,
    ContactManager,
)

from genesis_forge.mdp import rewards, terminations, observations, reset

# ------------------------------------------------------------
# 1. Action Manager para tracción diferencial (2 ruedas)
# ------------------------------------------------------------
from genesis_forge.managers.action.base import BaseActionManager

class DifferentialDriveActionManager(BaseActionManager):
    """
    Convierte [linear_vel, angular_vel] en velocidades de dos ruedas.
    Asume que las ruedas están separadas por 'wheel_base' y tienen radio 'wheel_radius'.
    """
    def __init__(self, env, motors, max_speed=1.5, max_turn=2.0,
                 wheel_base=0.205, wheel_radius=0.035):
        super().__init__(env)
        self.motors = motors
        self.max_speed = max_speed
        self.max_turn = max_turn
        self.wheel_base = wheel_base
        self.wheel_radius = wheel_radius

    @property
    def num_actions(self) -> int:
        return 2

    def step(self, action):
        super().step(action)
        action = self._actions
        
        # action: (num_envs, 2) -> [linear_vel, angular_vel]
        linear = torch.clamp(action[:, 0], -self.max_speed, self.max_speed)
        angular = torch.clamp(action[:, 1], -self.max_turn, self.max_turn)

        # Velocidades lineales de cada rueda (m/s)
        v_back = linear - (self.wheel_base / 2) * angular
        v_front = linear + (self.wheel_base / 2) * angular

        # Convertir a velocidad angular de los joints (rad/s)
        omega_back = v_back / self.wheel_radius
        omega_front = v_front / self.wheel_radius

        # Aplicar a los actuadores
        velocities = torch.stack([omega_back, omega_front], dim=-1)
        self.motors.set_dofs_velocity(velocities)

        return velocities


# ------------------------------------------------------------
# 2. Sensor de distancia simulado (cámaras de profundidad)
# ------------------------------------------------------------
class DepthDistanceSensor:
    """
    Simula N sensores HC‑SR04 usando cámaras de profundidad.
    Cada sensor apunta en una dirección fija relativa al robot.
    """
    def __init__(self, scene, robot, num_sensors=5, max_range=4.0,
                 sensor_fov_deg=30, sensor_res=(16, 16), link_name="base"):
        self.scene = scene
        self.robot = robot
        self.num_sensors = num_sensors
        self.max_range = max_range
        self.sensor_fov_deg = sensor_fov_deg
        self.sensor_res = sensor_res
        self.link_name = link_name

        # Direcciones (ángulos en radianes, 0 = frente)
        # 5 sensores: front, front-left, front-right, left, right
        angles_deg = [0, -45, 45, -90, 90]
        self.angles = torch.tensor(np.radians(angles_deg[:num_sensors]))

        # Crear las cámaras (aún no montadas)
        self.cameras = []
        for i in range(num_sensors):
            cam = scene.add_camera(
                res=sensor_res,
                fov=sensor_fov_deg,
                GUI=False,
            )
            self.cameras.append(cam)

    def attach_to_robot(self):
        """Monta las cámaras al robot. Llamar después de scene.build()"""
        parent = self.robot.get_link(self.link_name) if self.link_name else self.robot
        for i, cam in enumerate(self.cameras):
            angle = self.angles[i].item()
            # Posición local: 0.12 m delante, 0.08 m lateral, 0.06 m arriba
            local_pos = [0.12 * np.cos(angle), 0.12 * np.sin(angle), 0.06]
            # Orientación: mirar en la dirección del sensor
            quat = gs.xyz_to_quat(np.array([0.0, 0.0, angle]))
            T = gs.trans_quat_to_T(np.array(local_pos), quat)
            cam.attach(parent, offset_T=T)

    def get_distances(self):
        """
        Retorna tensor (num_envs, num_sensors) con distancias normalizadas [0,1].
        1.0 = sin obstáculo dentro de max_range.
        """
        dist_list = []
        for cam in self.cameras:
            _, depth, _, _ = cam.render(rgb=False, depth=True, segmentation=False, normal=False)
            positive = depth[depth > 0.01]          # ignorar fondo/cero
            if positive.size == 0:
                min_dist = self.max_range
            else:
                min_dist = positive.min().item()
            min_dist = min(min_dist, self.max_range)
            norm = min_dist / self.max_range
            dist_list.append(norm)

        dist_tensor = torch.tensor(dist_list, device=gs.device).unsqueeze(0)
        # Expandir a batch si hay múltiples entornos
        if self.scene.n_envs > 1:
            dist_tensor = dist_tensor.expand(self.scene.n_envs, -1).clone()
        return dist_tensor


# ------------------------------------------------------------
# 3. Entorno principal
# ------------------------------------------------------------
class LaberintIA(ManagedEnvironment):
    def __init__(
        self,
        num_envs: int = 1,
        dt: float = 1 / 50,
        max_episode_length_s: int | None = 20,
        headless: bool = True,
    ):
        super().__init__(
            num_envs=num_envs,
            dt=dt,
            max_episode_length_sec=max_episode_length_s,
            max_episode_random_scaling=0.1,
        )

        # Crear escena
        self.scene = gs.Scene(
            show_viewer=not headless,
            sim_options=gs.options.SimOptions(dt=self.dt, substeps=2),
            viewer_options=gs.options.ViewerOptions(
                max_FPS=int(0.5 / self.dt),
                camera_pos=(1.0, 0.0, 1.8),
                camera_lookat=(0.0, 0.0, 0.5),
                camera_fov=40,
            ),
            vis_options=gs.options.VisOptions(rendered_envs_idx=list(range(num_envs))),
            rigid_options=gs.options.RigidOptions(
                dt=self.dt,
                constraint_solver=gs.constraint_solver.Newton,
                enable_collision=True,
            ),
        )

        # Suelo y robot
        self.terrain = self.scene.add_entity(gs.morphs.Plane())
        self.robot = self.scene.add_entity(
            gs.morphs.MJCF(file="./model/HexaBot.xml", pos=[0.0, 0.0, 0.055], quat=[1, 0, 0, 0]),
        )

        # Cámara de debug (estática)
        self.camera = self.scene.add_camera(
            pos=(1.0, 0.0, 1.8),
            lookat=(0.0, 0.0, 0.5),
            fov=40,
            res=(1280, 720),
            env_idx=0,
            debug=True,
        )

        # Construir laberinto
        self._build_maze()

        # Inicializar sensores de distancia (después de que la escena esté construida)
        self.depth_sensor = DepthDistanceSensor(
            scene=self.scene,
            robot=self.robot,
            num_sensors=5,
            max_range=4.0,
            sensor_fov_deg=30,
            sensor_res=(16, 16),
            link_name="base",          # el body principal de tu robot se llama "base"
        )
        self.depth_sensor.attach_to_robot()

    # --------------------------------------------------------
    # Laberinto (paredes como cajas estáticas)
    # --------------------------------------------------------
    def _build_maze(self):
        walls = [
            ( 0.0,  3.0, 0.25,   6.0, 0.2, 0.5),   # norte
            ( 0.0, -3.0, 0.25,   6.0, 0.2, 0.5),   # sur
            ( 3.0,  0.0, 0.25,   0.2, 6.0, 0.5),   # este
            (-3.0,  0.0, 0.25,   0.2, 6.0, 0.5),   # oeste
            ( 0.5,  1.0, 0.25,   0.2, 2.0, 0.5),   # muro interior
        ]
        for (px, py, pz, sx, sy, sz) in walls:
            self.scene.add_entity(
                gs.morphs.Box(size=(sx, sy, sz), pos=(px, py, pz), fixed=True)
            )

    # --------------------------------------------------------
    # Configuración de managers
    # --------------------------------------------------------
    def config(self):
        # 1. EntityManager: reset de posición
        self.car_manager = EntityManager(
            self,
            entity_attr="robot",
            on_reset={
                "position": {
                    "fn": reset.position,
                    "params": {
                        "position": [0.0, 0.0, 0.055],
                        "quat": [1.0, 0.0, 0.0, 0.0],
                        "zero_velocity": True,
                    },
                },
            },
        )

        # 2. Actuadores para las dos ruedas (joints según tu XML)
        self.motors = ActuatorManager(
            self,
            joint_names=["whell_back", "whell_front"],
            kv=80.0,
            max_force=300.0,
        )

        # 3. Action Manager diferencial
        self.action_manager = DifferentialDriveActionManager(
            self,
            self.motors,
            max_speed=1.5,      # m/s
            max_turn=2.0,       # rad/s
            wheel_base=0.205,   # distancia entre ruedas (ajústala si es necesario)
            wheel_radius=0.035,
        )
        self.action_managers = [self.action_manager]

        # 4. ContactManager (detecta colisiones con paredes)
        self.contact_manager = ContactManager(
            self,
            entity_attr="robot",
            link_names=["base"],   # solo detectar colisiones en el chasis
        )

        # 5. RewardManager
        RewardManager(
            self,
            cfg={
                # Velocidad hacia adelante
                "forward_progress": {
                    "weight": 1.5,
                    "fn": lambda env: self._get_forward_velocity(),
                },
                # Penalizar cambio brusco de acción
                "action_smoothness": {
                    "weight": -0.2,
                    "fn": lambda env: (env.actions - env.last_actions).abs().mean(dim=-1),
                },
                # Evitar giros excesivos (diferencia de velocidades entre ruedas)
                "diff_drive_balance": {
                    "weight": -0.1,
                    "fn": lambda env: (self.motors.get_dofs_velocity()[..., 0] - self.motors.get_dofs_velocity()[..., 1]).abs(),
                },
                # Penalizar colisiones fuertes
                "collision_penalty": {
                    "weight": -10.0,
                    "fn": lambda env: (self.contact_manager.contacts.norm(dim=-1) > 1.0).any(dim=-1).float(),
                },
                # Penalizar proximidad a paredes (suave)
                "wall_proximity": {
                    "weight": -0.5,
                    "fn": lambda env: torch.clamp(1.0 - self.depth_sensor.get_distances().min(dim=-1)[0], 0, 1),
                },
            },
        )

        # 6. TerminationManager
        self.termination_manager = TerminationManager(
            self,
            logging_enabled=True,
            term_cfg={
                "timeout": {"fn": terminations.timeout, "time_out": True},
                "wall_collision": {"fn": lambda env: (self.contact_manager.contacts.norm(dim=-1) > 1.0).any(dim=-1)},
            },
        )

        # 7. ObservationManager
        ObservationManager(
            self,
            cfg={
                "linear_velocity": {
                    "fn": lambda env: self.car_manager.get_linear_velocity(),
                    "noise": 0.05,
                },
                "angular_velocity": {
                    "fn": lambda env: self.car_manager.get_angular_velocity(),
                    "noise": 0.02,
                },
                "projected_gravity": {
                    "fn": lambda env: self.car_manager.get_projected_gravity(),
                    "noise": 0.01,
                },
                "wheel_vel": {
                    "fn": lambda env: self.motors.get_dofs_velocity(),
                    "noise": 0.05,
                    "scale": 0.1,
                },
                "last_action": {
                    "fn": lambda env: env.last_actions if env.last_actions is not None else torch.zeros((env.num_envs, 2), device=gs.device),
                },
                "distance_sensors": {
                    "fn": lambda env: self.depth_sensor.get_distances(),
                    "noise": 0.02,
                    "scale": 1.0,
                },
            },
        )

    # --------------------------------------------------------
    # Helper: velocidad lineal proyectada hacia adelante
    # --------------------------------------------------------
    def _get_forward_velocity(self) -> torch.Tensor:
        lin_vel = self.car_manager.get_linear_velocity()   # (n_envs, 3)
        heading = self.car_manager.get_heading()           # (n_envs,)
        forward = torch.stack([torch.cos(heading), torch.sin(heading)], dim=-1)
        return (lin_vel[:, :2] * forward).sum(dim=-1)
import torch
import numpy as np
import genesis as gs


class DepthDistanceSensor:
    """
    Simula sensores ultrasónicos HC-SR04 usando cámaras de profundidad montadas en el robot.
    Cada sensor renderiza un depth map pequeño y retorna la distancia mínima en su FOV.
    """
    
    def __init__(
        self,
        scene: gs.Scene,
        robot,
        num_sensors: int = 5,
        max_range: float = 4.0,
        sensor_fov_deg: float = 30.0,
        sensor_res: tuple = (16, 16),
        sensor_height: float = 0.1,
        sensor_forward_offset: float = 0.1,
    ):
        """
        Args:
            scene: Escena de Genesis
            robot: Entidad del robot
            num_sensors: Número de sensores HC-SR04 simulados
            max_range: Alcance máximo en metros
            sensor_fov_deg: Ángulo del cono de detección por sensor (grados)
            sensor_res: Resolución de cada mini-cámara (H, W)
            sensor_height: Altura de los sensores sobre el suelo
            sensor_forward_offset: Offset hacia adelante desde el centro del robot
        """
        self.scene = scene
        self.robot = robot
        self._num_sensors = num_sensors
        self.max_range = max_range
        self.sensor_fov_deg = sensor_fov_deg
        self.sensor_res = sensor_res
        self.sensor_height = sensor_height
        self.sensor_forward_offset = sensor_forward_offset
        
        self.cameras = []
        self._sensor_angles = self._compute_sensor_angles()
        
    def _compute_sensor_angles(self):
        """Calcula los ángulos de cada sensor (en radianes) respecto al forward del robot."""
        if self._num_sensors == 5:
            # Front, Front-Left, Left, Front-Right, Right
            angles_deg = [0, -45, -90, 45, 90]
        elif self._num_sensors == 7:
            # Agrega Left-90 y Right-90 (ya incluido en 5), y traseros
            angles_deg = [0, -30, -60, -90, -120, 30, 60, 90, 120]
            angles_deg = angles_deg[:7]
        elif self._num_sensors == 8:
            # 360 grados cada 45°
            angles_deg = [i * 45 for i in range(8)]
        else:
            # Distribución uniforme
            angles_deg = np.linspace(-90, 90, self._num_sensors)
        
        return np.deg2rad(angles_deg).astype(np.float32)
    
    def attach_to_robot(self, link_name: str = "buddy"):
        """
        Monta las cámaras al robot. Debe llamarse DESPUÉS de scene.build().
        """
        robot_link = self.robot.get_link(link_name)
        
        for i, angle in enumerate(self._sensor_angles):
            # Crear matriz de transformación para cada sensor
            # Posición: offset forward + altura
            # Rotación: yaw = angle, pitch = 0, roll = 0
            
            # En Genesis, attach usa una matriz de transformación 4x4
            T = self._create_transform_matrix(angle)
            
            cam = self.scene.add_camera(
                res=self.sensor_res,
                fov=self.sensor_fov_deg,
                near=0.01,
                far=self.max_range,
                GUI=False,
            )
            cam.attach(robot_link, T=T)
            self.cameras.append(cam)
        
        print(f"[DepthDistanceSensor] {len(self.cameras)} sensores montados en link '{link_name}'")
    
    def _create_transform_matrix(self, yaw: float) -> np.ndarray:
        """
        Crea matriz de transformación 4x4 para el sensor.
        Convención: X forward, Y left, Z up (coordenadas del robot)
        """
        # Posición relativa al link del robot
        pos = np.array([
            self.sensor_forward_offset,
            0.0,
            self.sensor_height
        ], dtype=np.float32)
        
        # Rotación solo en yaw (eje Z)
        cy, sy = np.cos(yaw), np.sin(yaw)
        rot = np.array([
            [cy, -sy, 0],
            [sy,  cy, 0],
            [0,   0,  1]
        ], dtype=np.float32)
        
        # Aplicar rotación a la posición
        pos_rotated = rot @ pos
        
        T = np.eye(4, dtype=np.float32)
        T[:3, :3] = rot
        T[:3, 3] = pos_rotated
        
        return T
    
    def get_distances(self) -> torch.Tensor:
        """
        Renderiza depth de cada cámara y retorna distancias normalizadas [0, 1].
        
        Returns:
            Tensor de shape (num_envs, num_sensors) con distancias normalizadas
        """
        if not self.cameras:
            raise RuntimeError("Sensores no montados. Llama attach_to_robot() primero.")
        
        distances = []
        
        for cam in self.cameras:
            # Renderizar depth map
            # render() retorna (rgb, depth, segmentation) si depth=True
            _, depth = cam.render(depth=True)
            
            # depth shape: (H, W) o (num_envs, H, W)
            # Tomar mínimo de toda la imagen (simula cono del HC-SR04)
            if depth.ndim == 3:
                # Múltiples entornos
                min_depth = depth.amin(dim=(-1, -2))  # (num_envs,)
            else:
                # Single env
                min_depth = depth.amin()
                min_depth = min_depth.unsqueeze(0)
            
            # Clamp a max_range y normalizar
            min_depth = torch.clamp(min_depth, 0.0, self.max_range)
            normalized = min_depth / self.max_range
            
            distances.append(normalized)
        
        # Stack: (num_sensors, num_envs) -> (num_envs, num_sensors)
        distances_tensor = torch.stack(distances, dim=-1)
        
        return distances_tensor
    
    def get_raw_distances(self) -> torch.Tensor:
        """Retorna distancias en metros (sin normalizar)."""
        if not self.cameras:
            raise RuntimeError("Sensores no montados. Llama attach_to_robot() primero.")
        
        distances = []
        
        for cam in self.cameras:
            _, depth = cam.render(depth=True)
            
            if depth.ndim == 3:
                min_depth = depth.amin(dim=(-1, -2))
            else:
                min_depth = depth.amin().unsqueeze(0)
            
            min_depth = torch.clamp(min_depth, 0.0, self.max_range)
            distances.append(min_depth)
        
        return torch.stack(distances, dim=-1)
    
    @property
    def sensor_angles(self) -> np.ndarray:
        """Retorna los ángulos de los sensores en radianes."""
        return self._sensor_angles.copy()
    
    @property
    def num_sensors(self) -> int:
        return self._num_sensors
    
    @num_sensors.setter
    def num_sensors(self, value: int):
        self._num_sensors = value
        self._sensor_angles = self._compute_sensor_angles()
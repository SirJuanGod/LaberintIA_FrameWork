# tools.py
import torch

class DifferentialDriveActionManager:
    def __init__(self, actuator_back, actuator_front, max_speed=1.5, max_turn=2.0, wheel_base=0.205):
        self.act_back = actuator_back   # rueda trasera
        self.act_front = actuator_front # rueda delantera
        self.max_speed = max_speed
        self.max_turn = max_turn
        self.wheel_base = wheel_base
        # Suponemos radio de rueda (debes medirlo o estimarlo)
        self.wheel_radius = 0.035  # ajusta según tu modelo

    def process_action(self, action):
        # action: (num_envs, 2) -> [linear_vel, angular_vel]
        linear = torch.clamp(action[:, 0], -self.max_speed, self.max_speed)
        angular = torch.clamp(action[:, 1], -self.max_turn, self.max_turn)

        # Velocidades lineales de cada rueda (en m/s)
        v_back = linear - (self.wheel_base / 2) * angular
        v_front = linear + (self.wheel_base / 2) * angular

        # Convertir a velocidad angular de los joints (rad/s)
        omega_back = v_back / self.wheel_radius
        omega_front = v_front / self.wheel_radius

        # Aplicar a los actuadores
        self.act_back.set_dofs_velocity(omega_back.unsqueeze(-1))
        self.act_front.set_dofs_velocity(omega_front.unsqueeze(-1))

        return torch.stack([omega_back, omega_front], dim=-1)
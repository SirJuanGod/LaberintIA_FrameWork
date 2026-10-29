import time
import numpy as np
import torch

from environment import GazeboEnv
from td3 import TD3

if __name__ == "__main__":
    ENV_NAME = "rviz_sim.launch.py"  # simulación ligera en RViz; "spawn_maze.launch.py" para Gazebo
    MODEL_NAME = "TD3_laberinto"
    MAX_EP_STEPS = 500

    env = GazeboEnv(ENV_NAME, environment_dim=3)
    time.sleep(5)

    state_dim = 7
    action_dim = 2
    max_action = 1.0

    policy = TD3(state_dim, action_dim, max_action)
    
    try:
        print(f"Cargando modelo desde ./pytorch_models/{MODEL_NAME}...")
        policy.load(MODEL_NAME, "./pytorch_models")
        print("¡Modelo cargado con éxito!")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        exit()

    state = env.reset()
    episode_timesteps = 0

    print("Iniciando evaluación...")
    while True:
        action = policy.select_action(np.array(state))
        
        # En evaluación no agregamos ruido, usamos la acción pura
        next_state, reward, done, _ = env.step(action)
        
        episode_timesteps += 1
        if done or episode_timesteps >= MAX_EP_STEPS:
            print("Episodio terminado. Reiniciando...")
            state = env.reset()
            episode_timesteps = 0
        else:
            state = next_state
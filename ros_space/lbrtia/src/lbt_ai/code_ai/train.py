import os
import time
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from environment import GazeboEnv
from td3 import TD3
from replay_buffer import ReplayBuffer

def evaluate_policy(env, policy, eval_episodes=10):
    avg_reward = 0.
    for _ in range(eval_episodes):
        state = env.reset()
        done = False
        count = 0
        while not done and count < 500:
            action = policy.select_action(np.array(state))
            state, reward, done, _ = env.step(action)
            avg_reward += reward
            count += 1
    avg_reward /= eval_episodes
    print(f"---------------------------------------")
    print(f"Evaluación en {eval_episodes} episodios: Reward Promedio: {avg_reward:.2f}")
    print(f"---------------------------------------")
    return avg_reward

if __name__ == "__main__":
    # Configuraciones
    ENV_NAME = "spawn_maze.launch.py"
    SEED = 0
    MAX_TIMESTEPS = 5e6
    START_TIMESTEPS = 1e4    # Acciones aleatorias antes de usar la red
    EVAL_FREQ = 5e3
    MAX_EPISODE_STEPS = 500
    
    EXPL_NOISE = 1.0
    EXPL_DECAY_STEPS = 500000
    EXPL_MIN = 0.1
    
    # Crear carpetas
    if not os.path.exists("./results"): os.makedirs("./results")
    if not os.path.exists("./pytorch_models"): os.makedirs("./pytorch_models")

    env = GazeboEnv(ENV_NAME, environment_dim=3)
    
    state_dim = 7  # 3 lasers + 4 robot info
    action_dim = 2
    max_action = 1.0

    # Inicializar IA
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    policy = TD3(state_dim, action_dim, max_action)
    replay_buffer = ReplayBuffer(max_size=1e6, state_dim=state_dim, action_dim=action_dim)
    writer = SummaryWriter()

    evaluations = [evaluate_policy(env, policy)]
    
    state = env.reset()
    done = False
    episode_reward = 0
    episode_timesteps = 0
    episode_num = 0
    
    count_rand_actions = 0
    random_action = []

    print("Comenzando el entrenamiento...")
    for t in range(int(MAX_TIMESTEPS)):
        episode_timesteps += 1

        # Decaimiento del ruido
        if EXPL_NOISE > EXPL_MIN:
            EXPL_NOISE -= ((1.0 - EXPL_MIN) / EXPL_DECAY_STEPS)

        # Seleccionar acción
        if t < START_TIMESTEPS:
            action = np.random.uniform(-max_action, max_action, action_dim)
        else:
            action = policy.select_action(np.array(state))
            action = (action + np.random.normal(0, EXPL_NOISE, size=action_dim)).clip(-max_action, max_action)

        # Maniobra evasiva aleatoria frente a obstáculos cercanos
        if np.random.uniform(0, 1) > 0.85 and min(state[:3]) < 0.6 and count_rand_actions < 1:
            count_rand_actions = np.random.randint(8, 15)
            random_action = np.random.uniform(-1, 1, 2)

        if count_rand_actions > 0:
            count_rand_actions -= 1
            action = random_action
            action[0] = -1.0  # Forzar retroceso

        # Ejecutar acción
        next_state, reward, done, target = env.step(action)
        done_bool = 0 if episode_timesteps == MAX_EPISODE_STEPS else int(done)

        # Guardar en memoria
        replay_buffer.add(state, action, reward, next_state, done_bool)

        state = next_state
        episode_reward += reward

        if done or episode_timesteps >= MAX_EPISODE_STEPS:
            if t >= START_TIMESTEPS:
                policy.train(replay_buffer, episode_timesteps)

            writer.add_scalar("Recompensa por Episodio", episode_reward, episode_num)
            print(f"Total T: {t+1} Episodio: {episode_num+1} Pasos: {episode_timesteps} Recompensa: {episode_reward:.3f}")
            
            state = env.reset()
            done = False
            episode_reward = 0
            episode_timesteps = 0
            episode_num += 1 

        if (t + 1) % EVAL_FREQ == 0:
            evaluations.append(evaluate_policy(env, policy))
            policy.save("TD3_laberinto", directory="./pytorch_models")
            np.save("./results/TD3_laberinto", evaluations)
import numpy as np

class ReplayBuffer:
    def __init__(self, max_size=1000000, state_dim=7, action_dim=2, random_seed=123):
        self.max_size = int(max_size)
        self.ptr = 0
        self.size = 0
        np.random.seed(random_seed)

        self.state = np.zeros((self.max_size, state_dim))
        self.action = np.zeros((self.max_size, action_dim))
        self.next_state = np.zeros((self.max_size, state_dim))
        self.reward = np.zeros((self.max_size, 1))
        self.done = np.zeros((self.max_size, 1))

    def add(self, state, action, reward, next_state, done):
        self.state[self.ptr] = state
        self.action[self.ptr] = action
        self.next_state[self.ptr] = next_state
        self.reward[self.ptr] = reward
        self.done[self.ptr] = done

        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(self.size + 1, self.max_size)

    def sample(self, batch_size):
        ind = np.random.randint(0, self.size, size=batch_size)
        return (
            self.state[ind],
            self.action[ind],
            self.next_state[ind],
            self.reward[ind],
            self.done[ind]
        )
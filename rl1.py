import numpy as np
import gymnasium as gym


def train_q_learning(env, episodes, alpha, gamma, epsilon_start, epsilon_end, epsilon_decay):
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q = np.zeros((n_states, n_actions), dtype=np.float64)

    returns = np.zeros(episodes, dtype=np.float64)
    eps = float(epsilon_start)

    for ep in range(episodes):
        obs, _ = env.reset(seed=ep)
        done = False
        total_reward = 0.0

        while not done:
            if np.random.random() < eps:
                action = env.action_space.sample()
            else:
                action = int(np.argmax(q[obs]))

            next_obs, reward, terminated, truncated, _ = env.step(action)
            done = bool(terminated or truncated)

            target = reward
            if not done:
                target = reward + gamma * float(np.max(q[next_obs]))

            q[obs, action] = q[obs, action] + alpha * (target - q[obs, action])

            obs = next_obs
            total_reward += float(reward)

        returns[ep] = total_reward
        eps = max(float(epsilon_end), eps * float(epsilon_decay))

    return q, returns


def evaluate_greedy(env, q, episodes):
    rewards = np.zeros(episodes, dtype=np.float64)
    for ep in range(episodes):
        obs, _ = env.reset(seed=10_000 + ep)
        done = False
        total_reward = 0.0
        while not done:
            action = int(np.argmax(q[obs]))
            obs, reward, terminated, truncated, _ = env.step(action)
            done = bool(terminated or truncated)
            total_reward += float(reward)
        rewards[ep] = total_reward
    return rewards


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False)

    q, returns = train_q_learning(
        env=env,
        episodes=5000,
        alpha=0.1,
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_end=0.05,
        epsilon_decay=0.999,
    )

    eval_rewards = evaluate_greedy(env, q, episodes=200)

    print(f"train_avg_last_500={returns[-500:].mean():.3f}")
    print(f"eval_avg={eval_rewards.mean():.3f}")

    env.close()


if __name__ == "__main__":
    main()


import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import gymnasium as gym
import numpy as np
import tensorflow as tf
from keras import layers

# Create the CartPole Environment
env = gym.make('CartPole-v1')
obs_space = int(env.observation_space.shape[0])
act_space = int(env.action_space.n)

# Define the actor and critic networks
actor = tf.keras.Sequential([
    layers.Input(shape=(obs_space,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(act_space, activation='softmax')
])

critic = tf.keras.Sequential([
    layers.Input(shape=(obs_space,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

# Define optimizer and loss functions
actor_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
critic_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

# Main training loop
num_episodes = int(os.getenv("AC_EPISODES", "110"))
gamma = 0.99

for episode in range(num_episodes):
    # Fix 1: Unpack state and info
    state, _ = env.reset()
    state = np.array(state, dtype=np.float32)
    episode_reward = 0

    for t in range(1, 10000):
        with tf.GradientTape(persistent=True) as tape:
            # Predict action probabilities
            state_tensor = tf.convert_to_tensor([state])
            action_probs = actor(state_tensor)
            
            # Choose action
            action = np.random.choice(env.action_space.n, p=action_probs.numpy()[0])

            # Fix 2: Unpack 5 values from step
            next_state, reward, terminated, truncated, _ = env.step(action)
            next_state = np.array(next_state, dtype=np.float32)
            done = terminated or truncated

            # Compute Values and Advantage
            state_value = critic(state_tensor)
            next_state_value = critic(tf.convert_to_tensor([next_state]))
            
            # TD Error / Advantage
            # If done, next_state_value should be 0
            target = reward + (gamma * next_state_value * (1 - int(done)))
            advantage = target - state_value

            # Losses
            actor_loss = -tf.math.log(action_probs[0, action]) * tf.stop_gradient(advantage)
            critic_loss = tf.square(advantage)

        # Update
        actor_grads = tape.gradient(actor_loss, actor.trainable_variables)
        critic_grads = tape.gradient(critic_loss, critic.trainable_variables)
        
        actor_optimizer.apply_gradients(zip(actor_grads, actor.trainable_variables))
        critic_optimizer.apply_gradients(zip(critic_grads, critic.trainable_variables))

        state = next_state
        episode_reward += reward

        if done:
            break

    if episode % 10 == 0:
        print(f'Episode {episode}, Reward: {episode_reward}', flush=True)

env.close()

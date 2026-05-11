import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

#The maze is represented as a 2D NumPy array.
#Zero values are safe paths; ones are obstacles the agent must avoid.
#Start and goal define the positions where the agent begins and where it aims to reach.
maze = np.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0]
])

start = (0, 0)#The agent starts at the top-left corner of the maze.
goal = (9, 9)#The agent's goal is to reach the bottom-right corner of the maze.

num_episodes = 5000 #The number of episodes determines how many times the agent will attempt to navigate the maze, allowing it to learn from its experiences and improve its policy over time.
alpha = 0.1 #The learning rate (alpha) controls how much the agent updates its Q-values based on new experiences. A value of 0.1 means that the agent will update its Q-values by 10% of the new information it receives, allowing it to learn gradually while still retaining some of its previous knowledge.
gamma = 0.9 #The discount factor (gamma) determines the importance of future rewards. A value of 0.9 means that the agent values future rewards at 90% of their immediate value.
epsilon = 0.5 #The exploration rate (epsilon) controls the balance between exploration and exploitation. A value of 0.5 means that the agent will explore randomly 50% of the time.

reward_fire = -10 #The reward for encountering a fire obstacle.
reward_goal = 50 #The reward for reaching the goal.
reward_step = -1 #The reward for each step taken.

actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]#The possible actions the agent can take: left, right, up, and down.

Q = np.zeros(maze.shape + (len(actions),))#The Q-table is initialized to zeros, with dimensions corresponding to the maze's shape and the number of possible actions. This table will be updated as the agent learns from its interactions with the environment.

#Step 3: Helper Function for Maze Validity and Action Selection
def is_valid(pos):
    r, c = pos
    if r < 0 or r >= maze.shape[0]:
        return False
    if c < 0 or c >= maze.shape[1]:
        return False
    if maze[r, c] == 1:
        return False
    return True


def choose_action(state):
    if np.random.random() < epsilon:
        return np.random.randint(len(actions))
    else:
        return np.argmax(Q[state])

#Step 4: Train the Agent with Q-Learning Algorithm
rewards_all_episodes = []

for episode in range(num_episodes):
    state = start
    total_rewards = 0
    done = False

    while not done:
        action_index = choose_action(state)
        action = actions[action_index]

        next_state = (state[0] + action[0], state[1] + action[1])

        if not is_valid(next_state):
            reward = reward_fire
            done = True
        elif next_state == goal:
            reward = reward_goal
            done = True
        else:
            reward = reward_step

        old_value = Q[state][action_index]
        next_max = np.max(Q[next_state]) if is_valid(next_state) else 0

        Q[state][action_index] = old_value + alpha * \
            (reward + gamma * next_max - old_value)

        state = next_state
        total_rewards += reward

    epsilon = max(0.01, epsilon * 0.995)
    rewards_all_episodes.append(total_rewards)

#Step 5: Extract the Optimal Path after Training
def get_optimal_path(Q, start, goal, actions, maze, max_steps=200):
    path = [start]
    state = start
    visited = set()

    for _ in range(max_steps):
        if state == goal:
            break
        visited.add(state)

        best_action = None
        best_value = -float('inf')

        for idx, move in enumerate(actions):
            next_state = (state[0] + move[0], state[1] + move[1])

            if (0 <= next_state[0] < maze.shape[0] and
                0 <= next_state[1] < maze.shape[1] and
                maze[next_state] == 0 and
                    next_state not in visited):

                if Q[state][idx] > best_value:
                    best_value = Q[state][idx]
                    best_action = idx

        if best_action is None:
            break

        move = actions[best_action]
        state = (state[0] + move[0], state[1] + move[1])
        path.append(state)

    return path


optimal_path = get_optimal_path(Q, start, goal, actions, maze)

#Step 6: Visualize the Maze, Robot Path, Start and Goal
def plot_maze_with_path(path):
    cmap = ListedColormap(['#eef8ea', '#a8c79c'])

    plt.figure(figsize=(8, 8))
    plt.imshow(maze, cmap=cmap)

    plt.scatter(start[1], start[0], marker='o', color='#81c784', edgecolors='black',
                s=200, label='Start (Robot)', zorder=5)
    plt.scatter(goal[1], goal[0], marker='*', color='#388e3c', edgecolors='black',
                s=300, label='Goal (Diamond)', zorder=5)

    rows, cols = zip(*path)
    plt.plot(cols, rows, color='#60b37a', linewidth=4,
             label='Learned Path', zorder=4)

    plt.title('Reinforcement Learning: Robot Maze Navigation')
    plt.gca().invert_yaxis()
    plt.xticks(range(maze.shape[1]))
    plt.yticks(range(maze.shape[0]))
    plt.grid(True, alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

#Step 7: Plot Rewards per Training
plot_maze_with_path(optimal_path)

def plot_rewards(rewards):
    plt.figure(figsize=(10, 5))
    plt.plot(rewards)
    plt.title('Total Rewards per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True)
    plt.show()


plot_rewards(rewards_all_episodes)
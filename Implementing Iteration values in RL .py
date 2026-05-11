import numpy as np

states = [0, 1, 2]  
actions = [0, 1]     

def transition_model(s, a, s_next):
    if (s == 0 and a == 0 and s_next == 1):
        return 1
    elif (s == 0 and a == 1 and s_next == 2):
        return 1
    elif (s == 1 and a == 0 and s_next == 0):
        return 1
    elif (s == 1 and a == 1 and s_next == 2):
        return 1
    elif (s == 2 and a == 0 and s_next == 0):
        return 1
    elif (s == 2 and a == 1 and s_next == 1):
        return 1
    return 0

def reward_function(s, a, s_next):
    if s == 0 and a == 0 and s_next == 1:
        return 10
    elif s == 0 and a == 1 and s_next == 2:
        return 5
    elif s == 1 and a == 0 and s_next == 0:
        return 7
    elif s == 1 and a == 1 and s_next == 2:
        return 3
    elif s == 2 and a == 0 and s_next == 0:
        return 4
    elif s == 2 and a == 1 and s_next == 1:
        return 8
    return 0
gamma = 0.9  
epsilon = 0.01

def value_iteration(states, actions, transition_model, reward_function, gamma, epsilon):
    V = {s: 0 for s in states}
    
    while True:
        delta = 0
        for s in states:
            v = V[s]
            V[s] = max(sum(transition_model(s, a, s_next) * 
                           (reward_function(s, a, s_next) + gamma * V[s_next])
                           for s_next in states) for a in actions)
            delta = max(delta, abs(v - V[s]))
        if delta < epsilon:
            break
    policy = {}
    for s in states:
        policy[s] = max(actions, 
                        key=lambda a: sum(
                          transition_model(s, a, s_next) *
                                                   (reward_function(
                                                     s, a, s_next) + gamma * V[s_next])
                                                   for s_next in states))
    return policy, V

policy, value_function = value_iteration(states, actions, transition_model, reward_function, gamma, epsilon)

print("Optimal Policy:", policy)
print("Value Function:", value_function)
import numpy as np
import matplotlib.pyplot as pyplot
import math


'''System size L'''
L = 8
'''Total number of mc steps'''
nsteps = 100000


'''Function to generate initial configuration'''


def init_state(L):
    inistate = [1 for i in range(L * L)]
    return inistate


def energy(state):
    E = 0
    for i in range(len(state)):
        for j in range(len(state)):
            E -= 0.0001 * state[i] * state[j]

    return E


def equilibrate(state, beta):
    endstate = state
    for i in range(1000):
        endstate = mcstep(endstate, beta)

    return endstate


def mcstep(state, beta):

    newstate = state
    i = np.random.choice(64)
    newstate[i] = -state[i]

    p = math.exp(int(-beta * energy(newstate))) / \
        math.exp(int(-beta * energy(state)))
    # evaluate p with integrand
    if p >= 1:
        state = newstate
        # accept
    else:
        if random.random() < p:
            state = newstate
            # accept with probability p
        else:
            state = state
            # reject :(

    return state


conf = init_state(L)
Tsample = 25

Tn = [(1 + 12 * i) for i in range(Tsample)]

for T in Tn:
    print(energy(conf) / T)

print(conf, len(conf), energy(conf), energy(estate))

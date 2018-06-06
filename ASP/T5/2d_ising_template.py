import numpy as np
import matplotlib.pyplot as pyplot
import math

'''System size L'''
L = 15
'''Total number of mc steps'''
nsteps = 100000


'''Function to generate initial configuration'''


def init_state(L):
    inistate = [np.random.choice([-1, 1])for i in range((L + 1) * (L + 1))]
    inistate = np.mat(np.reshape(inistate, (L + 1, L + 1)))
    for i in range(L + 1):
        inistate[i, L] = inistate[i, 0]

        inistate[L, i] = inistate[0, i]

    return inistate


print(init_state(L))
'''Function which calculates the magnetization'''


def magnetization(state):
    m = 0
    for i in range(L):
        for j in range(L):
            m += state[i, j]
    return m / (L * L)


'''Function which calculates the total energy in the system'''


def energy(state):
    E = 0
    for i in range(L):
        for j in range(L):
            E += -state[i, j] * state[i + 1, j] - state[i, j] * state[i, j + 1]

    return E


'''Function Monte-Carlo Step (Metropolis Algorithm)'''


def mcstep(state, beta):

    newstate = state
    i = np.random.choice(L, 2)
    newstate[i] = -state[i]
    if i[0] == 0:
        newstate[L, i[1]] = -state[0, i[1]]
    if i[1] == 0:
        newstate[i[0], L] = -state[i[1], L]

    p = math.exp(-beta * energy(newstate)) / \
        math.exp(-beta * energy(state))
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


def equilibrate(state, beta):
    endstate = state
    for i in range(10000):
        endstate = mcstep(endstate, beta)

    return endstate


def mc(steps, state, beta):
    endstate = state
    measure_m = []
    measure_E = []
    states = []
    for i in range(steps):
        endstate = mcstep(endstate, beta)

        if i % 100 == 0:
            measure_m.append(magnetization(endstate))
            measure_E.append(energy(endstate))
            # print(magnetization(endstate), energy(endstate))
            # if i % 1000 == 0:
            # states.append(np.reshape(endstate, (8, 8)))

    return (endstate, measure_m, measure_E, states)\



def chi(measure_m, beta):
    return beta * np.var(measure_m)


def cv(measure_E, beta):
    return beta * beta * np.var(measure_E)


'''Main part of the program'''

if __name__ == '__main__':
    '''set up initial configuration'''
    conf = init_state(L)
    '''number of steps to equilibrate the initial configuration'''

    '''measure every 100 mc steps'''

    '''Temperature points - don't make this number too large'''
    Tsample = 25
    '''Sample temperature between 4 and 1'''
    Tn = [(1.0 + 0.12 * i) for i in range(Tsample)]
    '''define lists to sample thermodynamic quantities for different temperatures'''

    '''Lopp over different Temperatures'''
    chilist = []
    cvlist = []
    elist = []
    mlist = []
    for T in Tn:
        beta = 1 / T

        estate = equilibrate(conf, beta)

        ends = ()
        ends = mc(nsteps, conf, beta)
        print(T, chi(ends[1], beta), cv(ends[2], beta))
        chilist.append(chi(ends[1], beta))
        cvlist.append(cv(ends[2], beta))
        elist.append(np.mean(ends[2]) / (L * L))
        mlist.append(np.mean(ends[1]))

    fig, axes = pyplot.subplots(2, 2)
    axes[0, 0].plot(elist)
    axes[0, 1].plot(mlist)
    axes[1, 0].plot(cvlist)
    axes[1, 1].plot(chilist)
    pyplot.show()
# pyplot.plot(ends[1])
# pyplot.plot(ends[2])

# fig, axes = pyplot.subplots(1, 8)

# for i in range(8):
# axes[i].imshow(ends[3][i], origin='lower', interpolation='nearest')

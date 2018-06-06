import math
import random
import numpy as np
import matplotlib.pyplot as plt


def mc(n, a, b):
    s = 0
    for i in n:
        s += math.exp(-pow(i, 2))
    return (b - a) * s / len(n)


def ips(n, a, b):
    s = 0
    for i in n:
        s += math.exp(-pow(i, 2)) / ((1 / math.sqrt(2 * math.pi))
                                     * math.exp(-pow(i, 2) / (2 * math.pi)))
    return s / len(n)
# define integration using importance sampling method


def markov(walker, t):
    for i in range(t):
        # repeat t times
        newwalker = np.random.normal(0, 1)
        # generate new sample with probability distribution omega
        p = math.exp(-pow(newwalker, 2)) / math.exp(-pow(walker, 2))
        # evaluate p with integrand
        if p >= 1:
            walker = newwalker
        # accept
        else:
            if random.random() < p:
                walker = newwalker
                # accept with probability p
            else:
                walker = walker
                # reject :(
    return walker

# define markov process for one sample


def mmc(w, t):
    a = w
    b = []
    for i in a:
        i = markov(i, t)
        b.append(i)
    return b


for i in range(2, 13, 2):
    points = []
    for p in range(1000):
        points.append(random.uniform(-20, 20))
    opoints = points

    print(1000, mc(points, -20, 20), ips(mmc(opoints, i * 100), -20, 20))
pts = []
for p in range(1000):
    pts.append(random.uniform(-20, 20))
mak = []
mak.append(pts)
colors = []
colors.append((0.2, 0.5, 0.8, 0.9))
for i in range(1, 101, 20):
    mak.append(mmc(pts, i * 5))
    colors.append((0.3 + i / 500, 0.6 + i / 300, 0.9 - i / 300, 0.9))

plt.hist(mak, 500, color=colors, histtype='barstacked')
plt.show()

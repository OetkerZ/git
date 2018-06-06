# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:29:17 2018

@author: Chao Wan
"""
import numpy as np
import matplotlib.pyplot as plt

neq = pow(10,4)
nsteps = pow(10,5)
L = 3

def init_state(L):
    psi0 = np.zeros((L+1)*(L+1))
    psi0 = psi0.reshape(L+1,L+1)
    psi0 = np.mat(psi0) 
    for i in range(L):
        for j in range(L):
            list = [-1,1]
            psi0[i,j] = np.random.choice(list)
    for i in range(L+1):
        psi0[L,i] = psi0[0,i]
        psi0[i,L] = psi0[i,0]
    return psi0

def magnetization(state):
    sum = 0.
    m = 0.
    for i in range(L):
        for j in range(L):
            sum += state[i,j]
    m = sum/pow(L,2)
    return m

def energy(state):
    E = 0.
    for i in range(L):
        for j in range(L):
            E += (-1)*state[i,j]*state[i+1,j]+(-1)*state[i,j]*state[i,j+1]
    return E/pow(L,2)

def mcstep(state, temp):
    newstate = state
    list = range(L)
    rand = 0.
    i = np.random.choice(list)
    j = np.random.choice(list)
    newstate[i,j] *= -1
    for i in range(L):
        newstate[L,i] = newstate[0,i]
        newstate[i,L] = newstate[i,0]
    deltaE = energy(newstate)-energy(state)
    if deltaE < 0:
        state = newstate
    else:
        rand = random.uniform(0,1)
        if rand < np.exp(-deltaE/temp):
            state = newstate
    return state


if __name__=='__main__':
    '''set up initial configuration'''
    conf = init_state(L)
    '''number of steps to equilibrate the initial configuration'''

    '''Sample temperature between 4 and 1'''
    
    '''define lists to sample thermodynamic quantities for different temperatures'''
    Tn = []
    for i in range(25):
        Tn.append(1+0.12*i)
    print(Tn)
    
    j = 0
    ener = []
    magn = []
    for i in range(nsteps):
        conf = mcstep(conf, 2)
        if i == neq:
            print(conf)
        if i > neq:
            if np.mod(i,100) == 0:
                ener.append(energy(conf))
                magn.append(magnetization(conf))
    print(ener)
    print(magn)
    
    plt.subplot(211)
    plt.plot(range(len(magn)),magn,'b',label = 'magnetization')
    plt.plot(range(len(ener)),ener,'r', label = 'energy')
    plt.show()
    
    meanm = []
    meane = []
    cv = []
    chi = []
    for T in Tn:
         ener = []
         magn = []
         for i in range(nsteps):
             conf = mcstep(conf,T)
             if i > neq:
                 if np.mod(i,100) == 0:
                     ener.append(energy(conf))
                     magn.append(magnetization(conf))
         cv.append(np.var(ener))
         meanm.append(np.mean(magn))
         meane.append(np.mean(ener))
         chi.append(np.var(magn))
    
    print(meane)
    print(meanm)
    print(chi)
    print(cv)
    
    plt.plot(Tn,meane,'b',Tn,meanm,'r',Tn,cv,'g',Tn,chi,'pink')
    plt.show()
                 


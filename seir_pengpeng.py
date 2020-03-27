# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:52:29 2020
SEIR model based on
"SEIR Transmission dynamics model of 2019 nCoV coronavirus
with considering the weak infectious ability and changes in latency duration"
by Shi Pengpeng, Cao Shengli, and Feng Peihua
doi: https://doi.org/10.1101/2020.02.16.20023655

@author: Brian
"""

import numpy as np
import matplotlib.pyplot as plt

c = 3.6 #contact rate
beta = 6.93e-11 #probability of transmission
delta_I = 0.13 # quarantine rate of the infected
delta_q = 0.13 # transformation rate from the exposed to the isolated infected
gama_I = 0.003 # recovery rate of the infected
gama_H = 0.009 # recovery rate of the isolated infected
q = 9e-7  #quarantine ratio
alpha = 0.0001 # diseaseinduced death rate
theta = 0.6 # ratio of the transmission ability of the exposed to the infected.
lam = 1/14 # rate of isolation release (1/days)
T = 40 # days
t = 0.1 # period in days (time step)
NN = int(T/t) # set time steps

#Initial values
S = 8.3e6  # Susceptible population
E = 4007     # Exposed population
I = 7770     # Infected population
Sq = 8420    # Isolated susceptible
Eq = 3000    # Isolated Exposed
H = I + Eq     # Hospitalized
R = 34       # Recovered
De = 25      # Died

# initialize lists to store time steps
SS = [S]
EE = [E]
II = [I]
HH = [H]
DD = [De]
x_range = []

for ii in range (1,NN):
# Modified SEIR Transmission dynamics model
    sigma = (1/7 - 1/3)/(1+ np.exp((ii * t - 4)/ ii * t/0.2)) + 1/3
    dS = -(beta*c+c*q*(1-beta))*S*(I+theta*E)+lam*Sq
    dE = beta*c*(1-q)*S*(I+theta*E)-sigma*E
    dI = sigma*E-(delta_I+alpha+gama_I)*I
    dSq = (1-beta)*c*q*S*(I+theta*E)-lam*Sq
    dEq = beta*c*q*S*(I+theta*E)-delta_q*Eq
    dH = delta_I*I+delta_q*Eq-(alpha+gama_H)*H
    dR = gama_I*I+gama_H*H
    dDe = alpha*(I+H)

    #Euler integration algorithm
    S = round(S+dS*t,0)
    E = round(E+dE*t,0)
    I = round(I+dI*t,)
    Sq = round(Sq+dSq*t,0)
    Eq = round(Eq+dEq*t,0)
    H = round(H+dH*t,0)
    R = round(R+dR*t,0)
    De = round(De + dDe*t,0)

    #update lists
    SS.append(S)
    EE.append(E)
    II.append(I)
    HH.append(H)
    DD.append(De)
    x_range.append(ii)

# plot specified list
x = np.asarray(x_range)
y = np.asarray(HH)

plt.plot(y)
ticks = np.arange(x.min(), x.max(), 50)
labels = np.round(ticks/10,0).astype(int)
plt.xticks(ticks, labels)
plt.xlabel('Days')
plt.show()
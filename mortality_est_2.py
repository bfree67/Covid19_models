# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:48:35 2020

@author: Brian
"""

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import copy

def rand_uniform_v( min_x, max_x, n):
    return (np.random.rand(n) * (max_x-min_x)) + min_x

def prob(dist,p):
    ### p is probability threshold
    ### dist is an array of probability distributions results
    ### returns binary array where 1 is> p and 0 is less
    a = (dist <= p) + 0.
    return a

def makeprob(Vin, n, p):

    ## Vin is cell vector
    ## n is the matrix and vector indices
    ## p is the binomial probability after the element prob is created in rand_uniform
    ## uses functions justone and rand_uniform_v

    av = prob((rand_uniform_v(0,1,n)), p)
    bv = 1 - av ## make complement

    return np.asmatrix((av)).T, np.asmatrix((bv)).T

def deepcopy(a):
    # make deep copy of array a and get array length
    new_a = copy.deepcopy(a)
    n,m = np.shape(a)
    return new_a, n

def makeone(a):
    ### make all non-zero counts 1
    return (a>0) + 0

def justone(a,x):
    ### a = matrix/vector and x = elements to focus on
    ### returns binary array filter with 1 as element space & 0 is not the element of interest
    return np.asarray((a == x) + 0)

def greaterone(a,x):
    ### returns vector mask that identifies positions where the value is >= x
    return np.asarray((a >= x) + 0)

def and_filter(a,p):
    ### uses logical AND to identify existing (1) and new (1) = 1, all others 0
    ### a = conditional population
    ### p = binomial probability
    new_a, n = deepcopy(a)
    new_rate = np.asmatrix(rnd.binomial(1, p, size = n)).T
    return np.logical_and(new_a, new_rate) + 0

def or_filter(a,p):
    ### uses logical AND to identify existing (1) and new (1) = 1, or any 1 becomes 1
    ### a = conditional population
    ### p = binomial probability
    new_a, n = deepcopy(a)
    new_rate = np.asmatrix(rnd.binomial(1, p, size = n)).T
    return np.logical_or(new_a, new_rate) + 0

def reset(a, mask, value):
    # reset values in array a to 0 based on index of mask
    # value is 0 or 1
    new_a, n = deepcopy(a)
    nonz = np.flatnonzero(mask) #get indices of nonzero elements in a
    if len(mask)!=0:
        for i in range(len(nonz)):
            new_a[nonz[i]] = value
        return new_a

rnd.seed(1)
size = 100
p_exp = 0.1 # chance of coming inc contact with virus
p_inf = 0.5 # chance of getting infected after exposure
p_hospital = 0.9
p_icu = 0.1 #
p_recover = 0.2
p_death = 0.1
p_isolate = 0.01 # impact of isolation/quarantine from spreading

# baseline population before initial exposure
a = []
P = np.zeros((size,1)) # array to track population condition (no exp = 0)
te = np.zeros((size,1)) #array to track time from exposure (no exp = 0)
ti = np.zeros((size,1)) #array to track time from infection (no infection = 0)
th = np.zeros((size,1)) #array to track time from hospitalization (no hospital = 0)

I = np.zeros((size,1))
H = np.zeros((size,1))
ICU = np.zeros((size,1))
D = np.zeros((size,1))

# initial exposure
E, S = makeprob(P, size, p_exp)
te += makeone(E) # start the clock for exposed individuals

for i in range (5):
    # exposure chance - either get exposed or not
    E1, E1c = makeprob(E, size, p_exp)
    E = makeone(np.logical_or(E1,E)) # chance non-exposed individuals get exposed
    S -= (np.logical_and(S,E) + 0) # remove from S population
    te += makeone(E)               # update exposure time


    # once exposed, you either stay exposed or get infected (show symptoms)
    EIa, EIc = makeprob(E, size, p_inf) # get infection rate (EIa) and complement
    I = makeone((np.logical_and(E,EIa) + 0) + I)     # merge with exposed population
    ti += I                                        # update infection time

    # if infected for more than a day, stay infected, recover, goto hospital, or die
    InfTime = greaterone(ti,2)

    # find patients that recover
    Ri,Rc = makeprob(I, size, p_recover)
    I_recover = np.logical_and(Ri, InfTime) + 0
    S = reset(S, I_recover, 1)  # update S population
    E = reset(E, I_recover, 0)  # update E population
    ii = I - I_recover # remaining infected

    # find patients that die before going to hospital
    Di, Dc = makeprob(ii, size, p_death)
    I_died = np.logical_and(Di, ii) + 0
    iii = ii - I_died
    S = reset(S,I_died,-1)     #if negative number then dead
    E = reset(E,I_died,-1)

    # find how many infected go to hospital
    IH, IHc = makeprob(iii, size, p_hospital)
    I_hospital = np.logical_and(IH, iii) + 0
    H = makeone(I_hospital + H)
    Iq = iii - I_hospital    # infected patients quarantined outside hospital
    th += H

    # in hospital you can stay, recover, die, or goto ICU
    HTime = greaterone(th,3)
    # find how many in hospitals recover
    Hi,Hc = makeprob(H, size, p_recover)
    H_recover = np.logical_and(Hi, InfTime) + 0
    S = reset(S, H_recover, 1)  # update S population
    E = reset(E, H_recover, 0)  # update E population
    hh = H - H_recover # remaining in hospital





#plt.plot(a)

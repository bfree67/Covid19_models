# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 01:28:43 2020
Expanded SEIR model to account for missing links to different state conditions
@author: Brian
"""

import numpy as np
import matplotlib.pyplot as plt

# initial values
S0 = 100000
S = S0  #susceptible population
Sq = 0    # Isolated susceptible
E = 0    # Exposed population
Eq = 0   # Isolated Exposed
I = 0     # Infected population (showing symptoms)
Iq = 0    # infected population in isolation
H = 0   # Hospitalized
Icu = 0  # in ICU beds
D = 0      # Died
R = 0   # Recovered

#initialize lists
aS = [S]; aSQ = [Sq]; aE = [E]; aEQ = [Eq]; aI = [I]; aIQ = [Iq]
aH = [H]; aICU = [Icu]; aD = [D]; aR = [R]
model_period = 4 # days

for i in range (model_period):
    ### set output values
    ps_sq = 0.4
    StoSQ = S * ps_sq
    ps_e = 0.04
    StoE = S * ps_e

    psq_exp = 0.001
    psq_e = psq_exp * .1 # prob isolation S pop gets exposed to virus and goes into the open
    psq_eq = psq_exp * 0.9 # prob isolation S pop stays in isolation
    SQtoE = Sq * psq_e
    SQtoEQ = Sq * psq_eq

    pe_eq = 0.4
    EtoEQ = E*pe_eq
    pe_i = 0.1 # prob exposed pop shows symptoms (infected)
    EtoI = E * pe_i

    peq_i = 0.1 # prob exposed pop shows symptoms (infected)
    EQtoI = Eq * peq_i
    peq_iq = 0.1 # prob exposed pop shows symptoms (infected)
    EQtoIQ = Eq * peq_iq
    peq_r = .01 # prob exposed person in isolation recovers
    EQtoR = Eq * peq_r

    pi_h = 0.9 # prob infected population goes to hospital
    ItoH = I * pi_h
    pi_iq = 0.6 # prob infected population goes into isolation
    ItoIQ = I * pi_iq
    pi_r = 0.05 # prob infected person recovers
    ItoR = I * pi_r
    pi_d = 0.001 # prob infected pop dies
    ItoD = I * pi_d

    piq_h = 0.9 # prob infected pop in isolation goes to hospital
    IQtoH = Iq * piq_h
    piq_r = 0.05 # prob infected pop in isolation recovers
    IQtoR = Iq * piq_r
    piq_d = 0.001 # prob infected pop dies
    IQtoD = Iq * piq_d

    ph_icu = 0.2 # prob pop in hospital needs ICU/ventilator
    HtoICU = H * ph_icu
    ph_r = 0.4 # prob pop in hospital recovers
    HtoR = H * ph_r
    ph_d = 0.01 # pob pop in hospital dies
    HtoD = H * ph_d

    picu_h = 0.2 # prob pop in icu returns to normal ward
    ICUtoH = Icu * picu_h
    picu_d = 0.3 # prob pop in ICU dies
    ICUtoD = Icu * picu_d

    pr_s = 1  # prob recovered patients returns to susceptible population
    RtoS = R * pr_s

    ### begin calculations
    Dnew = round(HtoD + ICUtoD + ItoD + IQtoD,0)
    D += round(Dnew,0); aD.append(Dnew)
    R += round(ItoR + IQtoR + HtoR,0); aR.append(ItoR + IQtoR + HtoR)
    Sq += round(StoSQ - SQtoE - SQtoEQ,0); aSQ.append(Sq)
    E += round(StoE + SQtoE - EtoEQ - EtoI,0); aE.append(E)
    Eq += round(EtoEQ + SQtoEQ - EQtoI - EQtoIQ,0); aEQ.append(Eq)
    I += round(EtoI + EQtoI - ItoR - ItoIQ - ItoH - ItoD,0); aI.append(I)
    Iq += round(ItoIQ + EQtoIQ - IQtoR - IQtoH - IQtoD,0); aIQ.append(Iq)
    H += round(ItoH + IQtoH + ICUtoH - HtoR - HtoICU - HtoD,0); aH.append(H)
    Icu += round(HtoICU - ICUtoH - ICUtoD,0); aICU.append(Icu)
    S += round(-StoSQ - StoE,0); aS.append(S)

    TotPop = S + Sq + E + Eq +I + Iq + H + Icu + R - Dnew

    print(int(S), int(Sq), int(E), int(Eq), int(I), int(Iq),  int(H), int(Icu),
           int(R), int(HtoD + ICUtoD + ItoD + IQtoD), int(TotPop), S0 - int(Dnew))
tot_infected = np.asarray(aI) + np.asarray(aIQ)
#plt.plot(aI)

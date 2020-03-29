# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 01:28:43 2020

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

'''
S = S*ps_s + R*pr_s - S*ps_e - S*ps_sq
SQ = SQ*psq_sq + S*ps_sq - SQ*psq_s - SQ*psq_e - SQ*psq_eq
E = E*pe_e + S*ps_e + SQ*psq_e - E*pe_i - E*pe_eq - E*pe_s
EQ = EQ*peq_eq + SQ*psq_eq + E*pe_eq - EQ*peq_s - EQ*peq_iq - EQ*peq_i
I = I*pi_i + E*pe_i + EQ*peq_i - I*pi_s - I*pi_iq - I*pi_h - I*pi_d
IQ = IQ*piq_iq + EQ*peq_iq + I*pi_iq - IQ*piq_h - IQ*piq_s - IQ*piq_d
H = H*ph_h + I*pi_h + IQ*piq_h + ICU*picu_h - H*ph_s - H*ph_icu - H*ph_d
ICU = ICU*picu_icu + H*ph_icu - ICU*picu_h - ICU*picu_d
D = ICU*picu_d + H*ph_d + IQ*piq_d + I*pi_d
R = R*pr_r + E*pe_s + + EQ*peq_s + I*pi_s + IQ*piq_s + H*ph_s - R*pr_s
'''
for i in range (60):
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
    D += (HtoD + ICUtoD + ItoD + IQtoD); aD.append((HtoD + ICUtoD + ItoD + IQtoD))
    R += (ItoR + IQtoR + HtoR ); aR.append(ItoR + IQtoR + HtoR)
    Sq += (StoSQ - SQtoE - SQtoEQ); aSQ.append(Sq)
    E += (StoE + SQtoE - EtoEQ - EtoI); aE.append(E)
    Eq += (EtoEQ + SQtoEQ - EQtoI - EQtoI); aEQ.append(Eq)
    I += (EtoI + EQtoI - ItoR - ItoIQ - ItoH - ItoD); aI.append(I)
    Iq += (ItoIQ + EQtoIQ - IQtoR - IQtoH - IQtoD); aIQ.append(Iq)
    H += (ItoH + IQtoH + ICUtoH - HtoR - HtoICU - HtoD); aH.append(H)
    Icu += (HtoICU - ICUtoH - ICUtoD); aICU.append(Icu)
    S += ( -StoSQ - StoE); aS.append(S)
    TotPop = S + Sq + E + Eq +I + Iq + H + Icu + R - D


    print(round(S,0), round(Sq,0), round(E,0), round(Eq,0), round(I,0), round(Iq,0),  round(H,0), round(Icu,0),
           int(ItoR + IQtoR + HtoR), int(HtoD + ICUtoD + ItoD + IQtoD), int(TotPop), S0 - int(D))
tot_infected = np.asarray(aI) + np.asarray(aIQ)
#plt.plot(aI)

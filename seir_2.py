# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import numpy.random as rand
import random
import math

def init_group(init):
   if init > population:
       init = population
       
   g_init = np.array([1] * init + [0] * (population - init)) 
   rand.shuffle(g_init)
   return g_init

def make_one(pop):
    return (pop>0) + 0

rand.seed(0)
random.seed(0)

population = int(1e3)

pop = np.zeros(population)
t_exp = np.zeros(population)   ### time exposed
t_infected = np.zeros(population)   ### time infected
t_hosp = np.zeros(population)  ### time hospitalized

p_contact = 1  # chance of coming into contact with someone
p_inf = 0.5    # probability of showing symptoms if infected
incubation = 4 #days
serious_symptoms = 4 # days
expose_end = 8 # days
p_hospital = 0.15 # 

# initial exposure group
init_exp = 1

exp_pop = init_group(init_exp) # set initial exposure group
t_exp += exp_pop

R0 = 1.1  # set R0

for i in range (20):
    
    # reduce probability of contact over time
    p_contact -= i*.001
    contact =(rand.uniform(low = 0.0, high = 1.0, size = population) < p_contact) + 0
    
    ## spreading it around if you do come into contact
    r0 = rand.uniform(low = 1.1, high = 2.1, size = population) 
    r0_1 = r0 - r0.astype(int)
    
    ## convert to contacts
    r_p = rand.uniform(low = 0.0, high = 1.0, size = population)
    r_add = ((r0_1 > r_p) + 0) * contact
    
    # sum total of new exposed and make random array of new exposed people
    r0_int = ((r0.astype(int) * r_add) * exp_pop).sum() # filter out non players 
    add = init_group(r0_int)
    
    ## add new exposed to population
    exp_pop += add
    exp_pop = make_one(exp_pop)
    t_exp += exp_pop  # update time exposed
    
    # calculate eposed population that contract virus after 4 days
    incubated_pop = (t_exp > incubation) + 0  ### population completed incubation
    r_incubated = (rand.uniform(low = 0.0, high = 1.0, size = population) < p_inf) + 0
    infected_pop = incubated_pop * r_incubated  # update infected population
    t_infected += infected_pop  # update time of infection
    
    ### calculate population that completed exposure
    end_exposed_pop = (t_exp > expose_end) + 0  
    end_exposed = ((infected_pop - end_exposed_pop) < 0) + 0
    
    ### remove exposed population that did not get infected - count infected people as exposed
    exp_pop = make_one(exp_pop - end_exposed)  
    
    # reset exposed timer by 0ing out non-exposed and infected
    t_exp_reset = ((incubated_pop + end_exposed) == 0) + 0  
    t_exp *= t_exp_reset
    
    ### infected population with serious symptoms
    serious_symptoms_pop = (t_infected > serious_symptoms) + 0  
    r_hospital = (rand.uniform(low = 0.0, high = 1.0, size = population) < p_hospital) + 0
    hospital_pop = r_hospital * serious_symptoms_pop
    t_hosp += hospital_pop
    

    
    print(exp_pop.sum(), infected_pop.sum(), hospital_pop.sum())



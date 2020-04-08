# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 10:40:33 2020

@author: Brian
"""


import numpy as np
import numpy.random as rand

### age demographics (https://en.wikipedia.org/wiki/Demographics_of_the_United_States)
p0_10 = .1862
p10_20 = .1312
p20_30 = 0
p30_40 = 0
p40_50 = .3929
p50_60 = .1294
p60_70 = 0
p_gt70 = .1603

p_tot = p0_10 + p10_20 + p20_30 + p30_40 + p40_50 + p50_60 + p60_70 + p_gt70

# covi-19 death rates based on age and pre-existing condition
# https://www.disabled-world.com/health/influenza/coronavirus/coronavirus-mortality.php
pd_lt65 = 0.002
pd_gt65 = 0.08
pd_precon = 0.06

# percent of Americans with pre-existing conditions
p_precon = 0.6 # https://www.statnews.com/2020/03/03/who-is-getting-sick-and-how-sick-a-breakdown-of-coronavirus-risk-by-demographic-factors/

population = 100

### make age distribution
dem_age = np.array([5] * int(round(p0_10*population,0)) + 
                   [15] * int(round(p10_20*population,0)) +
                   [25] * int(round(p20_30*population,0)) +
                   [35] * int(round(p30_40*population,0)) +
                   [45] * int(round(p40_50*population,0)) +
                   [55] * int(round(p50_60*population,0)) +
                   [65] * int(round(p60_70*population,0)) +
                   [75] * int(round(p_gt70*population,0))
                   )
rand.shuffle(dem_age)

#### make pre-existing condition distribution
init = int(round(p_precon*population,0))
dem_precon = np.array([1] * init + [0] * (population - init))
rand.shuffle(dem_precon)
dr_precon = dem_precon * pd_precon

### apply death rates and make an array based on age
lt65_dr = ((dem_age <= 65) + 0) * pd_lt65
gt65_dr = ((dem_age > 65) + 0) * pd_gt65
dr_age = lt65_dr + gt65_dr

### consolidated death rate
dr = dr_age + dr_precon

### make random array of incubation (exposure to infection days) (8-14 days)
incubation = rand.randint(8, high = 15, size = population)
hosp_time = rand.randint(8, high = 15, size = population)
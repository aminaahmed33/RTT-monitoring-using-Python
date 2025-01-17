import numpy as np
from math import sqrt
import time
from datetime import timedelta, datetime
import statsmodels.api as sm
def wilson(distrib , n, alpha =  0.05):
    wilsonCi_low, wilsonCi_upp = sm.stats.proportion_confint(n/2, n, alpha, "wilson")
    #print("fwilson is:",wilsonCi_low, wilsonCi_upp)
    wilsonCi_low = np.array(wilsonCi_low)*len(distrib)
    wilsonCi_upp = np.array(wilsonCi_upp)*len(distrib)
    distrib.sort()
    #print("wilson is:",wilsonCi_low, wilsonCi_upp,"list is:",distrib)
    lower_b = distrib[int(wilsonCi_low)]
    #print("lower b as an index of disturb", lower_b)
    upper_b = distrib[int(wilsonCi_upp)]
    #print("upper b as an index of disturb", upper_b)
    return (lower_b , upper_b)
"""
def wilson(p, n, alpha = 0.5):
    denominator = 1 + alpha**2/n
    centre_adjusted_probability = p + alpha*alpha / (2*n)
    adjusted_standard_deviation = sqrt((p*(1 - p) + alpha*alpha / (4*n)) / n)
    lower_bound = (centre_adjusted_probability - alpha*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + alpha*adjusted_standard_deviation) / denominator
    return (round(lower_bound*n), round(upper_bound*n))
"""
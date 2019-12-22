#param_finder.py
"""A program for finding parameters of statistical functions with given power for 
hypothesis testing. Supports binomial and Poisson hypothesis testing currently."""

import numpy as np
from math import factorial
import scipy.stats as stats
from scipy.special import binom
from matplotlib import pyplot as plt

def x_finder(n, p=0.5, alpha=0.05):
    """For a given number n of Bernoulli trials with probability p of success, find the 
    smallest x such that x successes would indicate that we should REJECT the null 
    hypothesis that the true probability of success is less than or equal to p. Uses a 
    brute-force approach."""
    for x in np.arange(0,n+1):
        p_val = np.sum([binom(n,k) * p**k * (1-p)**(n-k) for k in np.arange(x,n+1)])
        if p_val < alpha:
            return x
    return None

def n_finder(power, p_true, p_null=0.5, alpha=0.05, n_bound=100):
    """For a given statistical power, find the smallest number n of Bernoulli trials 
    such that the probability of correctly rejecting the null hypothesis (that the 
    probability of success for the Bernoulli trials is p_null) in favor of the 
    alternative hypothesis (that the probability of success for the Bernoulli trials is 
    equal to p_true) is at least the given power. Uses a brute-force approach with a 
    maximum considered n given by n_bound."""
    for n in np.arange(0, n_bound+1):
        x = x_finder(n, p_null, alpha)
        if x is None:
            continue
        current_power = np.sum([binom(n,k) * p_true**k * (1-p_true)**(n-k) for k in 
                                np.arange(x,n+1)])
        if current_power >= power:
            return n
    return None

def poisson_n_finder(lambd, alpha=0.05):
    """For a Poisson trial of hypothesized rate lambd, find the smallest n such that 
    n observations would indicate that we should RETAIN the null hypothesis that the 
    true rate is greater than or equal to lambd. Uses a brute-force approach."""
    print(np.exp(-lambd)*np.sum([(lambd**x)/np.math.factorial(x) for x in np.arange(0,lambd+1)]))
    for n in np.arange(0,lambd+1):
        p_val = np.sum([np.exp(-lambd)*(lambd**x)/factorial(x) for x in range(n+1)])
        print(p_val)
        if p_val >= alpha:
            return n
    return None


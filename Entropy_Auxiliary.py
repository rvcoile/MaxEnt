# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-20"

import numpy as np
import pandas as pd
import scipy as scipy
from numpy import inf
from scipy.stats import *


#########################################
### CALCULATION FUNCTION DEFINITIONS  ### 
#########################################

def Z_final(l0, Lambda, alpha, X, W):  # recalculate with more precise l0
    M = [fraction_moment(i, X, W) for i in alpha]
    return l0 + np.sum(np.multiply(Lambda, M))


######################################
### AUXILIARY FUNCTION DEFINITIONS ### 
######################################

def fraction_moment(alpha, X, W):
    sim_numbers = X.index.tolist()
    Power = X.pow(alpha)
    if isinstance(W, int):
        N = max(sim_numbers)
        FractionalMoment = Power.sum() / N
        return FractionalMoment.loc['X']
    else:
        central = Power.loc['CENTRAL', 'CENTRAL']
        Power = Power.drop('CENTRAL', 0).drop('CENTRAL', 1)
        n = len(Power.columns)
        constituent = Power.multiply(W)
        FractionalMoment = central ** (1 - n)
        for variables in list(constituent.columns):
            FractionalMoment = FractionalMoment * constituent[variables].sum()
        return FractionalMoment


def lambda_0(Lambda, alpha, xmax, limit=10000, method='quad'):
    if method == 'quad':
        # with lambda and alpha vectors
        integraal = scipy.integrate.quad(integrand, 0, xmax, args=(Lambda, alpha), limit=limit)
        return np.log(integraal[0])
    elif method == 'numerical':
        integraal = lambda_0_numerical_preLN(Lambda, alpha, xmax)
        return np.log(integraal)


def lambda_0_numerical_preLN(Lambda, alpha, xmax):
    resultaat = []
    xlimlist = np.linspace(0., xmax, num=500)
    for n, xlim in enumerate(xlimlist):
        if xlim == 0:
            resultaat.append(0)
        else:
            delta = xlim - xlimlist[n - 1]
            divisions = 10
            size = delta / divisions
            int_points = np.arange(xlimlist[n - 1] + size / 2, xlim, size)
            int_values = []
            for x in int_points:
                fx = integrand(x, Lambda, alpha)
                int_values.append(fx)
            integraal = np.sum(int_values) * size
            resultaat.append(integraal)
    return sum(resultaat)


def integrand(x, Lambda, alpha):
    return np.exp(-np.sum(np.multiply(Lambda, np.power(x, alpha))))


def Entropy(mean, cov, xmax):
    # entropy calculation for known Lognormal distribution -- hardcoded lognormal for testing !!!
    sln = np.sqrt(np.log(1 + cov ** 2))
    mln = np.log(mean) - 1. / 2 * sln ** 2

    H = scipy.integrate.quad(LN_entropy_integrand, 0, xmax, args=(mln, sln), limit=10000)
    return -H[0]


def LN_entropy_integrand(x, mln, sln):
    return LN_pdf(x, mln, sln) * np.log(LN_pdf(x, mln, sln))


def LN_pdf(x, mln, sln):
    return lognorm.pdf(x, sln, scale=np.exp(mln))

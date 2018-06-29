# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-12"

import numpy as np
import pandas as pd
from scipy.integrate import quad
from numpy import inf
from PrintAuxiliary import *


#########################
### SUPPORT FUNCTIONS ###
#########################

def integrand(x, Lambda_Alpha):
    lambdalist = [];
    alphalist = []
    m = len(Lambda_Alpha.columns) / 2 - 1
    n = 0
    integrand = 1
    while n <= m:
        # integrand=integrand*np.exp(-Lambda_Alpha['l'+str(n)]*x**Lambda_Alpha['a'+str(n)])
        integrand = integrand * np.exp(
            -Lambda_Alpha.loc['min', 'l' + str(n)] * x ** Lambda_Alpha.loc['min', 'a' + str(n)])
        n = n + 1
    return integrand


def FxCalc(xlimlist, Lambda_Alpha, xmax, method='single_quad'):
    if method == 'single_quad':
        resultaat = FxCalc_quad_single(xlimlist, Lambda_Alpha, xmax)
    elif method == 'stepwise_quad':
        resultaat = FxCalc_quad_stepwise(xlimlist, Lambda_Alpha, xmax)
    elif method == 'numerical':
        resultaat = FxCalc_numerical(xlimlist, Lambda_Alpha, xmax)
    return resultaat


def FxCalc_numerical(xlimlist, Lambda_Alpha, xmax):
    resultaat = []
    for n, xlim in enumerate(xlimlist):
        if n == 0:
            if xlim == 0:  # hardcoded
                resultaat.append(0)
            else:
                print("assumed to start from 0 !!! -- hardcoded for now!!!")
        else:
            delta = xlim - xlimlist[n - 1]
            divisions = 100;
            size = delta / divisions
            int_points = np.arange(xlimlist[n - 1] + size / 2, xlim, size)
            int_values = fxCalc(int_points, Lambda_Alpha)
            integraal = np.sum(int_values.values) * size
            resultaat.append(integraal + resultaat[n - 1])
    return resultaat


def FxCalc_quad_stepwise(xlimlist, Lambda_Alpha, xmax):
    resultaat = []
    for n, xlim in enumerate(xlimlist):
        if n == 0:
            integraal = quad(integrand, 0, xlim, args=(Lambda_Alpha), limit=1000)
            resultaat.append(integraal[0])
        else:
            integraal = quad(integrand, xlimlist[n - 1], xlim, args=(Lambda_Alpha), limit=1000)
            resultaat.append(integraal[0] + resultaat[n - 1])
    return resultaat


def FxCalc_quad_single(xlimlist, Lambda_Alpha, xmax):
    resultaat = []
    for xlim in xlimlist:
        integraal = quad(integrand, 0, xlim, args=(Lambda_Alpha), limit=1000)
        resultaat.append(integraal[0])
    return resultaat


def fxCalc(xlimlist, Lambda_Alpha):
    m = len(Lambda_Alpha.columns) / 2 - 1
    number = len(xlimlist)
    fx = np.ones(number)

    fx = pd.DataFrame(0, index=xlimlist, columns=['PDF_m' + str(m)])
    x = pd.DataFrame(xlimlist, index=xlimlist, columns=['PDF_m' + str(m)])

    n = 0
    while n <= m:
        Lambda = Lambda_Alpha.loc['min', 'l' + str(n)]
        Alpha = Lambda_Alpha.loc['min', 'a' + str(n)]
        power = x.pow(Alpha)
        multi = power.multiply(Lambda)
        fx = fx.subtract(multi)
        # Print_DataFrame([multi,constituent,fx],'stap'+str(n),['multi','constituent','fx'])
        n = n + 1
    fx = np.exp(fx)
    return fx

#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2017-11-24"

import pandas as pd
import sympy as sy
import numpy as np

import statFunc
from PrintAuxiliary import Print_DataFrame


########################
## USE AND BACKGROUND ##
########################
#
# snippet from ProbabCalc2018
#

###############################
## (TEMPORARY LOCAL SUPPORT) ##
###############################

def ParameterRealization_r(varDict,rArray):

	DistType=varDict['Dist']

	if DistType=='N':
		return statFunc.Finv_Normal(rArray,varDict['m'],varDict['s'])
	if DistType=='LN':
		return statFunc.Finv_Lognormal(rArray,varDict['m'],varDict['s'])
	if DistType=='G':
		return statFunc.Finv_Gumbel(rArray,varDict['m'],varDict['s'])
	if DistType=='DET':
		return np.ones(np.shape(rArray))*varDict['m']


##########
## TEST ##
##########

# # limit state
# r,e1,e2=sy.symbols("r e1 e2")
# g=r-e1*e2

# # number of Monte Carlo
# nsim=10

# # ParameterDict
# mr=20; sr=3
# me1=3; se1=2
# me2=5; se2=3

# R={
# 'name':'r',
# 'Dist':'N',
# 'DIM':"[N]",
# 'm':mr,
# 's':sr,
# 'info':''
# }

# E1={
# 'name':'e1',
# 'Dist':'LN',
# 'DIM':"[N]",
# 'm':me1,
# 's':se1,
# 'info':''
# }

# E2={
# 'name':'e2',
# 'Dist':'G',
# 'DIM':"[N]",
# 'm':me2,
# 's':se2,
# 'info':''
# }

# Dict={
# 	'01':R,
# 	'02':E1,
# 	'03':E2
# 	}

# # Z,dfX,dfr=MonteCarlo(g,Dict,nsim)
# # Print_DataFrame([dfr,dfX],'TestOutput/test3var',['r','X'])
# # print(dfr)

# [m,s]=Taylor(g,Dict)


# print(m,s)
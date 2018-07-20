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

##############
## FUNCTION ##
##############

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

def SamplePointCalc(local_StochVar,r):

    # data
    info1=local_StochVar['info1']
    info2=local_StochVar['info2']

    # determine mean value for variable
    if info1=='mean':
        m=local_StochVar['p1']
    elif info1=='char':
        if info2=='std':
            m=local_StochVar['p1']+2*local_StochVar['p2'] # 2x std as hardcoded default
        elif info2=='cov':
            m=local_StochVar['p1']/(1-2*local_StochVar['p2'])

    # determine std for variable
    if info2=='std':
        s=local_StochVar['p2']
    elif info2=='cov':
        s=m*local_StochVar['p2']

    # apply in standardized stochastic variable Dict
    parDict={
    'name':local_StochVar['X'],
    'Dist':local_StochVar['type'],
    'DIM':"",
    'm':m,
    's':s,
    'info':''
    }

    return ParameterRealization_r(parDict,r)

def MeanEval(local_StochVar):

    # data
    info1=local_StochVar['info1']
    info2=local_StochVar['info2']

    # determine mean value for variable
    if info1=='mean':
        return local_StochVar['p1']
    elif info1=='char':
        if info2=='std':
            return local_StochVar['p1']+2*local_StochVar['p2'] # 2x std as hardcoded default
        elif info2=='cov':
            return local_StochVar['p1']/(1-2*local_StochVar['p2'])

def GaussSampleScheme(L,n,nSim):

    # initialize
    scheme=pd.DataFrame(index=np.arange(1,nSim+1),columns=['j','l'])    

    for l in np.arange(n+1):

        if l==0:
            scheme.loc[1,:]=[0,0] # starting entry as median value realization
        else:
            scheme.loc[2+4*(l-1):2+4*l-1,:]=[[1,l],[2,l],[4,l],[5,l]]    

    return scheme

def CalculationPoints(samplingScheme,GaussPoint_df,nSim):

    modelInput=pd.DataFrame(index=np.arange(1,nSim+1),columns=GaussPoint_df.columns)

    # initialize median values for all parameter realizations
    for var in modelInput.columns:
        modelInput[var]=GaussPoint_df.loc[3,var]

    # correct on every line the single modified Gauss point
    for i in modelInput.index:

        # j,l realization
        [j,l]=samplingScheme.loc[i,:]

        # assignment
        if l!=0: # 0-value corresponds with median point
            modelInput.loc[i,l]=GaussPoint_df.loc[j,l]

    return modelInput
#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2015-07-09"

import numpy as np
import pandas as pd
import scipy as scipy
from scipy.stats import *
from LatinHypercube import LHS_rand
from PrintAuxiliary import *

###########################
### Variable Definition ###
###########################

stochastic_variables=['X'] # name of stochastic variab

v1_name='X'

v1_mean = 60
v1_COV = 0.4
v1_sig=v1_COV*v1_mean

v1_sln=np.sqrt(np.log(1+v1_COV**2))
v1_mln=np.log(v1_mean)-1./2*v1_sln**2

#######################################
### Functions for Sample generation ###
#######################################

def LHS_data():

	number_simLHS=1*10**2

	indexlist=np.arange(1,number_simLHS+1,1)
	RandomField_Eval=pd.DataFrame(index=indexlist,columns=stochastic_variables)

	tmp=LHS_rand(number_simLHS,2)

	RandomField_Raw=pd.DataFrame()
	RandomField_Raw[v1_name]=tmp[0]

	tmp=norm.ppf(RandomField_Raw[v1_name],loc=v1_mln,scale=v1_sln)
	RandomField_Eval[v1_name]=np.exp(tmp)

	Print_DataFrame([RandomField_Eval,RandomField_Raw],'Samples\Test_LN_LHS',['DATA','aselect'])

def MC_data():

	number_MC=10**4 # number of Monte Carlo simulations

	indexlist=np.arange(1,number_MC+1,1)
	RandomField_Eval=pd.DataFrame(index=indexlist,columns=stochastic_variables)

	RandomField_Raw=pd.DataFrame(np.random.rand(number_MC,len(stochastic_variables)),index=indexlist,columns=stochastic_variables)

	tmp=norm.ppf(RandomField_Raw[v1_name],loc=v1_mln,scale=v1_sln)
	RandomField_Eval[v1_name]=np.exp(tmp)

	Print_DataFrame([RandomField_Eval,RandomField_Raw],'Samples\Test_LN_MC',['DATA','aselect'])

######################
### COMMAND CENTER ###
######################

LHS_data()
MC_data()
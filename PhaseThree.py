#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2015-07-21"

import numpy as np
import pandas as pd
import scipy as scipy
from scipy.optimize import *
from scipy.stats import *
from numpy import inf
from LatinHypercube import LHS_rand
from PrintAuxiliary import *
from LocalAuxiliary2 import *
from Entropy_Auxiliary import *

def PhaseThree(m,xmax,RandomField_Eval,number_best_phase3,W,targetfolder):

	Best=pd.read_excel(targetfolder+'\\PhaseResults\\m'+str(m)+'_PhaseTwo.xlsx','results')

	N=len(RandomField_Eval.index)

	AlphaList=Alpha_List(m); LambdaList=Lambda_List(m); tmp=AlphaList+['Z','simnumber']
	columnlist=LambdaList+tmp

	Final_df=pd.DataFrame(columns=columnlist+['l0','a0','Znew','Znew_PLUS'])

	for results in list(Best.index.values):
		localset=Best.loc[results,LambdaList+AlphaList].values
		l0=lambda_0(localset[:m],localset[m:],xmax=xmax,limit=100000,method='numerical')
		Znew=Z_final(l0,localset[:m],localset[m:],RandomField_Eval,W)
		Znew_PLUS=Znew+m/N

		Final_df.loc[results,:]=Best.loc[results,:].values.tolist()+[l0,0,Znew,Znew_PLUS]

	Results=Final_df

	Print_DataFrame([Results],targetfolder+'\\PhaseResults\\m'+str(m)+'_PhaseThree_prior',['result'])

	### Reduce set based on new Z-value ###
	#######################################

	value=Results[['Znew']]
	Lambda=Results[LambdaList]
	Alpha=Results[AlphaList]
	simnumbers=Results[['simnumber']]


	Redux=ReduceSet(m,value,Lambda,Alpha,number_best_phase3,simnumbers)

	Print_DataFrame([Redux],targetfolder+'\\PhaseResults\\m'+str(m)+'_PhaseThree_posterior',['result'])

	Final=pd.DataFrame()

	for simulations in Redux['simnumber']:
		idx=Results[Results['simnumber']==simulations].index.tolist()
		Final=Final.append(Results.loc[idx,:])
		# Final=Final.append(Results.loc[simulations,:])


	Print_DataFrame([Final],targetfolder+'\\PhaseResults\\m'+str(m)+'_PhaseThree_final',['result'])



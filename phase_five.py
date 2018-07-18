#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2015-07-21"

import numpy as np
import pandas as pd
from LocalAuxiliary import *
from PrintAuxiliary import *



def PhaseFive(mlist,number_best,targetfolder):

	Totallist=pd.DataFrame()

	for m in mlist:

		PhaseThree_final=pd.read_excel(targetfolder+'\\PhaseResults\\m'+str(m)+'_PhaseThree_final.xlsx','result')
		PhaseThree_final['m']=m

		## To Do : add m-indication

		Totallist=Totallist.append(PhaseThree_final,ignore_index=True)


	AlphaList=Alpha_List(m); LambdaList=Lambda_List(m);

	value=Totallist[['Znew_PLUS']]
	Lambda=Totallist[LambdaList]
	Alpha=Totallist[AlphaList]
	simnumber=Totallist[['simnumber']]

	Totallist[np.isnan(Totallist)]=0
	Print_DataFrame([Totallist],'Tester',['result'])

	Best=ReduceSet(m,value,Lambda,Alpha,number_best,simnumber)
	Final=pd.DataFrame()


	for simulations in Best['simnumber']:
		idx=Totallist[Totallist['simnumber']==simulations].index.tolist()
		Final=Final.append(Totallist.loc[idx,:])
		# Final=Final.append(Results.loc[simulations,:])

	Print_DataFrame([Final],targetfolder+'\\PhaseResults\\PhaseFive',['result'])


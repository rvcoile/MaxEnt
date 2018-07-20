# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-06-28"

#
# sampling scheme for external model input
# L=5 is hardcoded - limited variable may exist at different locations, but has not been finalized
#


####################
## MODULE IMPORTS ##
####################

import pandas as pd
import numpy as np
from copy import deepcopy

from statFunc import F_Normal
from GaussWeightsAndPoints import GaussPoints
from probabCalc_MaxEnt import ParameterRealization_r, SamplePointCalc, MeanEval, GaussSampleScheme, CalculationPoints
from PrintAuxiliary import Print_DataFrame


##########
## CORE ##
##########

## user input ##
################

# filename
filename=input("\nPlease provide path to input file stochastic variables (*.xlsx): ")
if filename[0]=="\"": filename=filename[1:-1] # strips quotes from path

# sheet Excel file with data
print("\n## Input stochastic variables in worksheet 'INPUT'. Note required layout and limited options. ##")
u=input("Press ENTER to confirm, or provide name of worksheet: ")
if u!='': sheet=u;
else: sheet='INPUT'
print("\nWorksheet set to ", sheet)

# output directory
outdir=input("\nPlease provide target directory for sampling scheme: ")
if outdir[0]=="\"": outdir=outdir[1:-1] # strips quotes from path

# Number of Gauss points
print("\n5 Gauss points will be considered per variable. There is currently no other functionality.")
# print("\nDefault number of Gauss integration points L = 5")
# u=input("Press ENTER to confirm, or provide alternative number of Gauss points: ")
L=5 # number of Gauss points per variable

# defaults for testing
# filename="C:/Users/rvcoile/Google Drive/Research/Codes/Python3.6/MaxEnt/SamplingInput/Ref_SiF2018.xlsx"
# sheet='INPUT'
# outdir="C:/Users/rvcoile/Documents/Python Scripts/MaxEnt2018"
# L=5

# Safety format testing => include run for mean values
print("\n(DEVELOPER) ## Include simulation of mean value = FALSE. ##")
u=input("Press ENTER to confirm, or press any other key to add mean value calculation (DEVELOPER ONLY):")
if u=='': SW_add_mean=False
else: SW_add_mean=True; print("\n### MEAN VALUE EVALUATION ADDED ###\n###################################\n")

## sample points per variable ##
################################

print("\nCollecting input data Stochastic variables.")

# read input data stochastic variables
StochVar=pd.read_excel(filename, sheet)
n=len(StochVar.index) # number of stochastic variables. l=1..n
nSim=(L-1)*n+1 # number of sample points - correct for odd L only... But currently functionality limited to L=5. j=1..L
print("\nTotal stochastic variables = %i\nTotal number of sample points = %i" %(n,nSim))

# Gauss points for L, and corresponding quantiles for X
points=GaussPoints(L)
r_realizations=F_Normal(points,0,1) # quantiles corresponding with Gauss points
r_realizations=r_realizations.flatten()

# realizations per variable
GaussPoint_df=pd.DataFrame(index=np.arange(1,L+1))
StochVar=StochVar.transpose()
varList=pd.Series()
for var in StochVar.columns:
    local_StochVar=StochVar[var]
    samplepoints=SamplePointCalc(local_StochVar,r_realizations)
    GaussPoint_df[local_StochVar['number']]=samplepoints
    varList.set_value(local_StochVar['number'],local_StochVar['X'])

## assign in sampling scheme ##
samplingScheme=GaussSampleScheme(L,n,nSim)
samples_modelInput=CalculationPoints(samplingScheme,GaussPoint_df,nSim)

# add mean value realization if requested
if SW_add_mean:
    # initialize series
    s = pd.Series(index=samples_modelInput.columns); s.name='MeanEval'
    # iterate over stochastic variables and introduce mean value for each of them
    for var in StochVar.columns:
        local_StochVar=StochVar[var]
        mean=MeanEval(local_StochVar)
        s[local_StochVar['number']]=mean
    # add series to sampling dataframe
    samples_modelInput=samples_modelInput.append(s)

## print results ##
###################

reference=deepcopy(samples_modelInput)
reference.columns=varList[reference.columns]

Print_DataFrame([samples_modelInput,samplingScheme,reference],outdir+'/MDRMGauss_samples',['modelInput','samplingScheme','modelInput_named'])

# file stochastic variable reference path for future reference

text_file = open(outdir+"/REF_input_stoch.txt", "w")
text_file.write("Stochastic variable reference file:\n%s\n\nsheet:\n%s" %(filename,sheet)) 
text_file.close()


##########
## TEST ##
##########

# print(r_realizations)
# print(samples_modelInput)
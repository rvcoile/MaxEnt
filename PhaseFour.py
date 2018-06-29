# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-21"

import numpy as np
import pandas as pd
import scipy as scipy
from PrintAuxiliary import *
from LocalAuxiliary import *
from FxEvaluationNEW import *
from statFunc import p_Lognormal
from LocalAuxiliary import Default_PDF_approx


def PhaseFour(m, xmax, delta_print,targetfolder,RandomField_Eval,W,approxFunction):


    ### default distribution CDF and PDF approx ###
    ###############################################

    M,s,PDF_LN,CDF_LN,cCDF_LN=Default_PDF_approx(approxFunction,RandomField_Eval,W,xmax,delta_print)
    param=pd.DataFrame([M,s,s/M],index=['m','s','V'],columns=['Y'])
    Print_DataFrame([param],targetfolder+'\\CDF_PDF\\Parameters',['Result'])

    ### ME-MDRM Phase Four ###
    ##########################
    print("\n##############################")
    print("### Processing of results ###")
    print("##############################\n")

    Results = pd.read_excel(targetfolder+'\\PhaseResults\\m' + str(m) + '_PhaseThree_final.xlsx', 'result')

    AlphaList = Alpha_List(m)
    LambdaList = Lambda_List(m)
    columnlist = LambdaList + AlphaList + ['l0', 'a0']

    ### calculation CDF and PDF for Results ###
    ###########################################

    xlim = np.arange(0., xmax+delta_print, delta_print)

    for number in list(Results.index.values):
        tmp = pd.DataFrame(Results.loc[number, columnlist].values, columns=['min'], index=columnlist)
        # print '\n', tmp
        Lambda_Alpha = tmp.transpose()
        fx = fxCalc(xlim, Lambda_Alpha)
        Fx = FxCalc(xlim, Lambda_Alpha, xmax, method='numerical'); Fx=np.asarray(Fx)

        original_simnumber = Results.loc[number, 'simnumber']

        Fx_print = pd.DataFrame([Fx,1-Fx,CDF_LN,cCDF_LN], columns=xlim, index=['CDF_m' + str(m),'cCDF_m' + str(m),'CDF_LN','cCDF_LN'])
        Fx_print=Fx_print.transpose()
        fx_print = fx; fx_print['PDF_LN']=PDF_LN

        try:
            Print_DataFrame([Fx_print, fx_print], targetfolder+'\\CDF_PDF\\m' + str(m) + '_integration_' + str(original_simnumber),
                            ['CDF_m' + str(m), 'PDF_m' + str(m)])
        except:
            print("strange Python printing error for original simnumber: ", original_simnumber)
            try:
                Print_DataFrame([fx_print], targetfolder+'\\CDF_PDF\\m' + str(m) + '_integration_' + str(original_simnumber),
                                ['PDF_m' + str(m)])
                print("but PDF try works\n")
            except:
                print("PDF try doesn't help\n")

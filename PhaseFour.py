# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-21"

import numpy as np
import pandas as pd
import scipy as scipy
from PrintAuxiliary import *
from LocalAuxiliary import *
from FxEvaluationNEW import *


def PhaseFour(m, xmax, delta_print):
    print("\n##############################")
    print("### Processing of results ###")
    print("##############################\n")

    Results = pd.read_excel('PhaseResults\m' + str(m) + '_PhaseThree_final.xlsx', 'result')

    AlphaList = Alpha_List(m)
    LambdaList = Lambda_List(m)
    columnlist = LambdaList + AlphaList + ['l0', 'a0']

    ### calculation CDF and PDF for Results ###
    ###########################################

    xlim = np.arange(0., xmax, delta_print)

    for number in list(Results.index.values):
        tmp = pd.DataFrame(Results.loc[number, columnlist].values, columns=['min'], index=columnlist)
        # print '\n', tmp
        Lambda_Alpha = tmp.transpose()
        fx = fxCalc(xlim, Lambda_Alpha)
        Fx = FxCalc(xlim, Lambda_Alpha, xmax, method='numerical')

        original_simnumber = Results.loc[number, 'simnumber']

        Fx_print = pd.DataFrame(Fx, index=xlim, columns=['CDF_m' + str(m)])
        fx_print = fx

        try:
            Print_DataFrame([Fx_print, fx_print], 'CDF_PDF\m' + str(m) + '_integration_' + str(original_simnumber),
                            ['CDF_m' + str(m), 'PDF_m' + str(m)])
        except:
            print("strange Python printing error for original simnumber: ", original_simnumber)
            try:
                Print_DataFrame([fx_print], 'CDF_PDF\m' + str(m) + '_integration_' + str(original_simnumber),
                                ['PDF_m' + str(m)])
                print("but PDF try works\n")
            except:
                print("PDF try doesn't help\n")

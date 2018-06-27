# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-19"

import numpy as np
import pandas as pd
from GaussWeightsAndPoints import GaussWeighting


###########################
### FUNCTION DEFINITION ###
###########################

def Lambda_List(m):
    n = 1
    LambdaList = []
    while n <= m:
        LambdaList.append('l' + str(n))
        n = n + 1
    return LambdaList


def Alpha_List(m):
    n = 1
    AlphaList = []
    while n <= m:
        AlphaList.append('a' + str(n))
        n = n + 1
    return AlphaList


def Lambda_Starting(m):
    n = 1.
    LambdaStarting = []
    while n <= m:
        LambdaStarting.append(n / m)
        n = n + 1
    return LambdaStarting


def ReduceSet(m, value, Lambda, Alpha, number_best, simnumberlist):
    valueAbs = value.abs()

    print(valueAbs)

    AlphaList = Alpha_List(m)
    LambdaList = Lambda_List(m)
    tmp = AlphaList + ['Z', 'simnumber']
    columnlist = LambdaList + tmp

    Best = pd.DataFrame(columns=columnlist)

    n = 1
    while n <= number_best:
        simnumber = valueAbs.idxmin()

        Ltmp = list(map(list, Lambda.loc[simnumber, :].values))
        Atmp = list(map(list, Alpha.loc[simnumber, :].values))
        Ztmp = list(map(list, valueAbs.loc[simnumber, :].values))
        sim = list(map(list, simnumberlist.loc[simnumber, :].values))
        datalist = Ltmp[0] + Atmp[0] + Ztmp[0] + sim[0]

        tmp = pd.DataFrame(datalist, columns=[n], index=columnlist)
        Best = Best.append(tmp.transpose())

        valueAbs = valueAbs.drop(simnumber)
        n = n + 1

    return Best

def ReadDatapoints(SW_Gaussian,SW_oldInputSyntax,filename,sheet):

    # provide input read for old syntax to allow for continued use old datasets
    if SW_oldInputSyntax:
        RandomField_Eval = pd.read_excel(filename, 'DATA')
        if SW_Gaussian:
            W = GaussWeighting(RandomField_Eval)
            tmp = pd.read_excel(filename, 'MeanPointGauss')
            RandomField_Eval = RandomField_Eval.append(tmp)
        else:
            W = 0

    else: # standard code for reading datapoints
        RawData=pd.read_excel(filename, sheet) # formatting as pd.DataFrame: numerbering of realizations in column 1, realization values in single column with header (=> cel A1 empty)
        # can be further modified as dataframe with yjl, j, l => free ordering of input data => in this case the number of Gauss points can also be more flexible
        if not SW_Gaussian:
            W=0 #  Gauss weights zero, cfr. MCS input
            RandomField_Eval=pd.DataFrame(RawData.values,columns=['X'],index=RawData.index)
        else:
            pass

    return W, RandomField_Eval


#########################
### CONTROL & TESTING ###
#########################
""" note: for local use only """

# print AlphaList(3)
# print ColumnList(3)

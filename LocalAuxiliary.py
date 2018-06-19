# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-19"

import numpy as np
import pandas as pd


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


#########################
### CONTROL & TESTING ###
#########################
""" note: for local use only """

# print AlphaList(3)
# print ColumnList(3)

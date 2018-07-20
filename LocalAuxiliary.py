# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-19"

import numpy as np
import pandas as pd
from GaussWeightsAndPoints import GaussWeighting
from Entropy_Auxiliary import fraction_moment
from statFunc import p_Lognormal, f_Lognormal, F_Lognormal


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

def ReduceSet_Phase3(m, value, Lambda, Alpha, number_best, simnumberlist):
    # difference with ReduceSet not clear. Possible redundancy. To be confirmed with testing.
    valueAbs = value.abs()

    # clear valueAbs for infinite value
    valueAbs = valueAbs.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="all")
    print(valueAbs)

    AlphaList = Alpha_List(m);
    LambdaList = Lambda_List(m);
    tmp = AlphaList + ['Z', 'simnumber']
    columnlist = LambdaList + tmp

    Best = pd.DataFrame(columns=columnlist)

    n = 1
    while n <= number_best:
        simnumber = valueAbs.idxmin()

        Ltmp = map(list, Lambda.loc[simnumber, :].values);
        Atmp = map(list, Alpha.loc[simnumber, :].values);
        Ztmp = map(list, valueAbs.loc[simnumber, :].values);
        sim = map(list, simnumberlist.loc[simnumber, :].values)
        datalist = list(Ltmp)[0] + list(Atmp)[0] + list(Ztmp)[0] + list(sim)[0]

        tmp = pd.DataFrame(datalist, columns=[n], index=columnlist)
        Best = Best.append(tmp.transpose())

        valueAbs = valueAbs.drop(simnumber)
        n = n + 1

    return Best


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
            # determine number of Gauss points
            GaussIndex=RawData['j']
            print(GaussIndex)
            L=GaussIndex.max()
            if L != 5:
                print("Not standard functionality. Seek help for implementation.")
            else:
                # number of stochastic variables
                n=int(np.round((GaussIndex.size-1)/4)) # should be int anyway
                print("\nDataset identified as Gaussian, with L = %i and n = %i" % (L,n))
                # initialize RandomField_Eval
                columns=[]
                for l in np.arange(1,n+1): # starts from 2 to avoid CENTRAL at first entry
                    name='X'+str(l)
                    columns.append(name)
                CENTRAL=RawData.loc[1,'Y']
                RandomField_Eval=CENTRAL*pd.DataFrame(np.ones((L,n)),columns=columns,index=np.arange(1,L+1))
                # assign realizations to positions in DataFrame
                for index in RawData.index:
                    j=RawData.loc[index,'j']
                    l=RawData.loc[index,'l']
                    yjl=RawData.loc[index,'Y']
                    if j!=0: RandomField_Eval.loc[j,'X'+str(l)]=yjl
                # Determine Gauss weights
                print(RandomField_Eval)
                W = GaussWeighting(RandomField_Eval)
                # finalize original syntax by appending CENTRAL
                tmp=pd.DataFrame([CENTRAL],index=['CENTRAL'],columns=['CENTRAL'])
                RandomField_Eval = RandomField_Eval.append(tmp)

    return W, RandomField_Eval

def Default_PDF_approx(approxFunction,RandomField_Eval,W,xmax_printing,x_deltaprint):

    # LN distribution
    if approxFunction=='LN':
        # Moments of the PDF as assessed by MDRM-G (or MCS as appropriate)
        M=fraction_moment(1, RandomField_Eval, W)
        M2=fraction_moment(2, RandomField_Eval, W)
        s=np.sqrt(M2-M**2)
        
        # PDF and CDF evaluation
        PDF_LN=f_Lognormal(np.arange(0.,xmax_printing+x_deltaprint,x_deltaprint),M,s)
        CDF_LN=F_Lognormal(np.arange(0.,xmax_printing+x_deltaprint,x_deltaprint),M,s)
        cCDF_LN=1-CDF_LN

    return M,s,PDF_LN,CDF_LN,cCDF_LN



#########################
### CONTROL & TESTING ###
#########################
""" note: for local use only """

# print AlphaList(3)
# print ColumnList(3)

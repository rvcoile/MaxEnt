# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-21"

# from PrintAuxiliary import *
from PrintAuxiliary import Print_DataFrame
# from LocalAuxiliary import *
import pandas as pd
from LocalAuxiliary import ReduceSet


def PhaseTwo(m, number_best,targetfolder):
    # Read results of phase_one.py
    # ============================

    value = pd.read_excel(targetfolder+'\\PhaseResults\\m' + str(m) + '_PhaseOne.xlsx', 'value')
    Lambda = pd.read_excel(targetfolder+'\\PhaseResults\\m' + str(m) + '_PhaseOne.xlsx', 'Lambda')
    Alpha = pd.read_excel(targetfolder+'\\PhaseResults\\m' + str(m) + '_PhaseOne.xlsx', 'Alpha')
    simnumber = pd.DataFrame(list(value.index), index=list(value.index), columns=list(value.columns))

    ### determine reduced set of best realizations ###
    ##################################################

    Best = ReduceSet(m, value, Lambda, Alpha, number_best, simnumber)

    ### print result of PHASE TWO ###
    #################################

    Print_DataFrame([Best], targetfolder+'\\PhaseResults\\m' + str(m) + '_PhaseTwo', ['results'])

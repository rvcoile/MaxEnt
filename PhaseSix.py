# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-06-28"

# code adapted from visual_MaxEnt.py for stand-alone application

####################
## MODULE IMPORTS ##
####################

# general modules Python
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from visualizationME import LinePlot_XmultiY

from copy import deepcopy


def PhaseSix(reffolder):


    ## LOAD DATA AND VISUALIZE ##
    #############################

    ## Input ##
    ###########

    # folder with data MaxEnt results
    folder=reffolder
    name=folder.rsplit('\\', 1)[-1] # project name for *.png naming

    # offset for optimum simulation number choice
    simAdd=0 # can be elaborated to apply offset when CDF not correctly evaluated numerically

    ## Read ##
    ##########

    ## READ PHASE 5
    # PhaseFive.xlsx lists best results
    phase5file=folder+'/PhaseResults/PhaseFive.xlsx'
    # read file
    phase5=pd.read_excel(phase5file,'result')
    # series of best optimization simulations
    simList=phase5['simnumber']

    ## READ CDF-PDF
    n=simList[0+simAdd]
    m=phase5.loc[0+simAdd,'m']
    # file with data
    resultfile=folder+'/CDF_PDF/m'+str(m)+'_integration_'+str(n)+'.xlsx'
    # read file
    CDF=pd.read_excel(resultfile,'CDF_m'+str(m))
    PDF=pd.read_excel(resultfile,'PDF_m'+str(m))


    ## visualization ##
    ###################

    ## visualization of CDF and cCDF ##

    out=CDF

    # X-axis limits
    df=deepcopy(out); df=df[df['CDF_LN']>10**-6]; df=df[df['cCDF_LN']>10**-6]
    Xmin=min(df.index); Xmax=max(df.index)


    # axis labels and axis ticks
    axisLabels=['$Y$ [DIM]','CDF [-], cCDF [-], CDF_LN [-], cCDF_LN [-]']
    Xticks=np.linspace(Xmin,Xmax,5)
    Yticks=[10**-4,10**-3,10**-2,10**-1,1]
    # Xminorticks=np.arange(Xmin,Xmax+dX/5,dX/5)
    # Yminorticks=np.arange(Ymin,Ymax+dY/5,dY/5)

    savePath=folder+'\\'+name+'_CDF.png'

    ## magnelPy visual ##
    [fig,ax1]=LinePlot_XmultiY(out,axisLabels=axisLabels,SW_show=False,SW_return=True,Axes='logY',
        Yticks=Yticks,Xticks=Xticks,SW_grid=True,savePath=savePath)

    ## visualization of PDF ##

    out=PDF

    # range of PDF axis
    # fmax=PDF['PDF_LN'].max()
    # dY=0.02
    # Ymin=0
    # Ymax=0.1

    axisLabels=['$Y$ [DIM]','PDF [-]']
    Xticks=np.linspace(Xmin,Xmax,5)
    # Yticks=np.arange(Ymin,Ymax+dY,dY)
    # Xminorticks=np.arange(Xmin,Xmax+dX/5,dX/5)
    # Yminorticks=np.arange(Ymin,Ymax+dY/5,dY/5)

    savePath=folder+'\\'+name+'_PDF.png'

    ## magnelPy visual ##
    [fig,ax1]=LinePlot_XmultiY(out,axisLabels=axisLabels,SW_show=False,SW_return=True,Axes='lin',
        Xticks=Xticks,SW_grid=False,savePath=savePath)
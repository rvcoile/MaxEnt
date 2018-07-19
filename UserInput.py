# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-06-26"

import numpy as np
import json
import time
import os

def UserInput(SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint,branch='',SW_Independent=True,filename='',sheet='DATA',targetfolder='',SW_TestInitialize=False):
    # adapted for multiple call options - cost = loss of clarity 

    if SW_Independent: # standard evaluation == independent MaxEnt evaluation

        if not SW_TestInitialize:
            # filename
            filename=input("\nPlease provide path to input file (*.xlsx): ")
            if filename[0]=="\"": filename=filename[1:-1] # strips quotes from path

            # sheet Excel file with data
            print("\n## Simulation results in worksheet 'DATA'. Note required layout. ##")
            u=input("Press ENTER to confirm (default), or provide name of worksheet (Independent MaxEnt only): ")
            if u!='': sheet=u;
            else: sheet='DATA'
            print("\nWorksheet set to ", sheet)

        # target folder
        print("\n## MaxEnt results will be saved in local worker directory. ##")
        u=input("Press ENTER to confirm, or provide path to alternative directory: ")
        if u!='': 
            if u[0]=="\"": targetfolder=u[1:-1] # strips quotes from path
            else: targetfolder=u
            print("\nMaxEnt output will be saved in ", targetfolder)
        else: targetfolder=''

        if not SW_TestInitialize:
            # SW_Gaussian - SW_Debug and SW_Testing for developer only
            if SW_Gaussian: 
                print("\n## Gaussian input data = True ##")
                u1=input("Press ENTER to confirm, or other key to switch to MCS: ")
                if u1!='': SW_Gaussian=False; print("\nSwitched to MCS input")
            else:
                print("\n## MCS input data = True ##")
                u1=input("Press ENTER to confirm, or other key to switch to Gaussian: ")
                if u1!='': SW_Gaussian=True; print("\nSwitched to Gaussian input")        

        # nProc 
        print("\n## Number of processors = %i ##" % (nProc))
        u2=input("Press ENTER to confirm, or specify other number: ")
        if u2!='': nProc=int(u2); print("\nCalculation with %i processors" % (nProc))

        # mlist
        print("\n## m-values to be calucated are ", mlist, " ##")
        u3=input("Press ENTER to confirm, or specify alternative list (comma separated): ")
        if u3!='': my_list = u3.split(","); mlist=list(map(int,my_list)); print("\n## updated m-values to ", mlist, " ##")

        # samples_rAlpha
        print("\n## Number of alpha-realizations in LHS (per m-value) = 10**%i ##" % (np.log10(samples_rAlpha)))
        u4=input("Press ENTER to confirm, or specify other power 10**x): ")
        if u4!='': samples_rAlpha=10**int(u4); print("\n %i LHS realizations per m-value" % (samples_rAlpha))

        # xmax_default
        print("\n## PDF is normalized in range [0., xmax], with xmax = %d ##" % (xmax_default))
        u=input("Press ENTER to confirm, or specify other uper bound x_max): ")
        if u!='': xmax_default=float(u); print("\n PDF normalization to be performed for range [0., %d]" % (xmax_default))

        # xmax_default
        print("\n## PDF output will be printed according to 0. : %d : %d] ##" % (x_deltaprint,xmax_printing))
        u=input("Press ENTER to confirm, or specify...\nxMax for PDF printing: x_max = ")
        if u!='':
            xmax_printing=float(u)
            u=input("dDelta_x for PDF printing: delta_x = "); x_deltaprint=float(u)
            print("\nPDF output will be printed according to 0. : %d : %d]" % (x_deltaprint,xmax_printing))

    ##############################
    ### PRINT SIMULATION INFO  ###
    ##############################

    # with open('BRANCH.txt','r') as ff:
    #     branch=ff.readline()

    with open(targetfolder+'\\MaxEnt_calcParameters.txt','w') as f:
        
        f.write('OVERVIEW OF MaxEnt SIMULATION PARAMETERS\n\n')
        f.write('input file:\n%s\nworksheet: %s\n' % (filename,sheet))
        if SW_Gaussian: f.write('\nGaussian input data')
        else: f.write('\nMCS input data')
        f.write('\nm-values evaluated: ')
        json.dump(mlist, f)
        f.write('\nLHS alpha-evaluations = 10**%i\nxmax normalization = [0, %d]\n\nPDF-CDF printing according to [0. : %d : %d]' %(np.log10(samples_rAlpha),xmax_default,x_deltaprint,xmax_printing))

        f.write('\n\nCurrent branch: %s\nMaxEnt Worker directory is:\n%s\n' % (branch,os.getcwd()))
        f.write('\nStart time: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        f.write('\n\n%i processors' % nProc)


    return SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint,filename,sheet,targetfolder
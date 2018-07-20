# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-07-19"

# functionalized MaxEnt2018.py

from phase_one import phase_one
from PhaseTwo import PhaseTwo
from PhaseThree import PhaseThree
from PhaseFour import PhaseFour
from phase_five import PhaseFive
from PhaseSix import PhaseSix
from UserInput import UserInput
from LocalAuxiliary import ReadDatapoints, Default_PDF_approx
from PrintAuxiliary import Print_DataFrame, RemoveFolderData
import time

import os
import GaussWeightsAndPoints


### NOTE ###
############
# see all reference for MaxEnt2018.py

def MaxEnt2018(outdir,file,SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint):

    if __name__ == "__main__":
        # if __name__ ... # requirement for parallel computing capability

        start_time=time.time()
        print("\nStarting MaxEnt.py\n## All user input must conform with syntax requirements ##\n")

        """ ################################################################################## """
        """ ############################ INPUT SECTION ####################################### """
        """ ################################################################################## """

        ################
        ### SWITCHES ###
        ################

        SW_Debug = False  # OMIT standard application and DO SPECIAL REQUEST at end of the file

        SW_oldInputSyntax = False # old input syntax for Gauss datapoints

        ################
        ### CONTROLS ###
        ################

        ## Default values control parameters - no overwrite by user input

        branch='alphaTest' # to be manually updated in current scheme

        # Default values control parameters
        number_best_phase2 = 50  # number of best values considered for PHASE TWO
        number_best_phase3 = 10  # number of best values considered for PHASE THREE
        number_best_phase5 = 5  # number of best values considered for PHASE FIVE (i.e. considering m/N)

        approxFunction='LN' # default approximation MDRM-G procedure (currently only 'LN')

        #####################
        ###  DATA READING ###
        #####################

        """ ################################################################################## """
        """ ###################### USER INPUT & CONFIRMATION ################################# """
        """ ################################################################################## """

        ## Overview of default values and possibility of user correction ##
        # filename = 'Test_LN_3Var_Gauss5.xlsx' # can be used when deactivating UserInput
        SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint,filename,sheet,targetfolder=UserInput(
            SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint,branch,SW_Independent=False,filename=file,sheet='DATA',targetfolder=outdir)

        """ ################################################################################## """
        """ ###################### STANDARD CALCULATION CORE ################################# """
        """ ################################################################################## """


        ###########################
        ### CALCULATION CENTER  ###
        ###########################

        # read and format datapoints + provide Gauss weights as appropriate
        W,RandomField_Eval=ReadDatapoints(SW_Gaussian,SW_oldInputSyntax,filename,sheet)

        if SW_Debug == False:

            #################
            ###  CLEANING ###
            #################
            
            # create sub-folder if non-existent
            # remove possible old calculation results
            sub01='\\CDF_PDF'
            sub02='\\PhaseResults'
            subList=[sub01,sub02]
            for sub in subList:
                targetdir=str(targetfolder+sub)
                if not os.path.exists(targetdir): 
                    os.mkdir(targetdir)
                else: RemoveFolderData(targetdir)

            for m in mlist:

                ###############################################
                ### PHASE ONE: OPTIMIZATION FOR GIVEN ALPHA ###
                ###############################################

                # 1) LHS generation of alpha-values
                # 2) determine lambda values through minimization + determine associated Z-value
                # 3) print results

                phase_one(m, samples_rAlpha, RandomField_Eval, W, xmax_default, nProc,targetfolder)

                ###########################################################
                ### PHASE TWO: LHS Monte Carlo AROUND BEST REALIZATIONS ###
                ###########################################################
                """ TO be elaborated later -- for now just accept the best result !!! """

                # currently....
                # 1) filters results for - first glance - acceptability
                # 2) determines reduced set of best results
                # 3) print reduced set

                PhaseTwo(m, number_best_phase2,targetfolder)

                ##########################################
                ### PHASE THREE: ACCEPTING BEST RESULT ###
                ##########################################

                # 1) recalculate lambda_0 with increased (numerical) accuracy
                # 2) recalculate Z-value
                # 3) print results - no PYTHON reordering of results yet...

                PhaseThree(m, xmax_default, RandomField_Eval, number_best_phase3, W, targetfolder)

                ###################################
                ### PHASE FOUR: POST-PROCESSING ###
                ###################################
                # officially post-processing, but filtering may be necessary => check if Fx(inf)==1 else the normalization in lambda_0 is imperfect

                # currently pure printing
                # could be another acceptance rule (see note above)

                # sometimes problems in printing may occur!! -- not yet coded for correction !!

                PhaseFour(m, xmax_printing, x_deltaprint,targetfolder,RandomField_Eval,W,approxFunction)

            ################################
            ### PHASE FIVE: FINAL-RESULT ###
            ################################

            # read PhaseThree_final results for all m in mlist => determine reduced set of optimum overall simulations

            PhaseFive(mlist, number_best_phase5,targetfolder)

            #####################################
            ### PHASE SIX: AUTO-VISUALIZATION ###
            #####################################

            PhaseSix(targetfolder)

            print("finalized in %s min" % ((time.time()-start_time)/60))

        else:

            """ ################################################################################## """
            """ ###################### TEST CENTER FOR DEBUGGING ################################# """
            """ ################################################################################## """

            #################################
            ### TEST CENTER for CONTROLS  ###
            #################################
            """ only executed if SW_Debug=False """

            print("\n## Debug zone ##\n")


            # PhaseFive(mlist, number_best_phase5,targetfolder)

        ###############
        ### CLOSURE ###
        ###############

        totaltime=(time.time()-start_time)/60

        print("finalized in %f min" % totaltime)

        with open(targetfolder+'\\MaxEnt_calcParameters.txt','a') as f:
            
            f.write('\n\nTotal calculation time: %.1f min' % totaltime)


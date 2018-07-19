# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-06-26"


# reference versions
# 2015-07-09: full version Python 2.7: MaxEntropyPDFestimate.py
# spring 2018: Ian.Fu@olssonfire.com and Danny.Hopkin@olssonfire.com: transfer to Python 3.6 + multiprocessing capability: MaxEntropyPDFestimate.py
# current version: reconceptualization (samples in referenced directories + saving of output)

from phase_one import phase_one
from PhaseTwo import PhaseTwo
from PhaseThree import PhaseThree
from PhaseFour import PhaseFour
from phase_five import PhaseFive
from PhaseSix import PhaseSix
from UserInput import UserInput
from LocalAuxiliary import ReadDatapoints, Default_PDF_approx
from PrintAuxiliary import Print_DataFrame
import time

import os
import GaussWeightsAndPoints


### NOTE ###
############
# the range of the distribution should (mostly) be clearly above 1. If this is not the case, change the dimension by multiplying with a factor
# the MaxEnt formula considers an output bounded [0; inf[ 
# code applies numerical integration in limited domain => caution; domain specification important

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

    SW_Testing = False  # indicate if test calculation or not -- if SW_Testing == True, the Kullback - Leibler divergence will be calculated

    SW_Debug = False  # OMIT standard application and DO SPECIAL REQUEST at end of the file

    SW_Gaussian = True  # function realizations Y(X) are based on Quadrature points for X... -- make sure to adapt filename etc accordingly

    SW_oldInputSyntax = False # old input syntax for Gauss datapoints

    ################
    ### CONTROLS ###
    ################

    # Default values control parameters

    nProc = 2 # number of processors

    mlist = [4]  # order of the PDF approximation - extend later for multi-m search conform (Inverardi and Tagliani, 2013)

    samples_rAlpha = 10 ** 3  # number of LHS samples Alpha - PHASE ONE - fixed Alpha values

    number_best_phase2 = 50  # number of best values considered for PHASE TWO
    number_best_phase3 = 10  # number of best values considered for PHASE THREE
    number_best_phase5 = 5  # number of best values considered for PHASE FIVE (i.e. considering m/N)

    """ TAKE NOTE TAKE NOTE TAKE NOTE """
    xmax_default = 1000.  # # extremely import variable if you move away from the LN testcase

    xmax_printing = 500.  # range for calc CDF and PDF -- make sure this is a float!!!!
    x_deltaprint = 1.0

    approxFunction='LN' # default approximation MDRM-G procedure (currently only 'LN')

    #####################
    ###  DATA READING ###
    #####################


    """ ################################################################################## """
    """ ###################### USER INPUT & CONFIRMATION ################################# """
    """ ################################################################################## """

    ## Overview of default values and possibility of user correction ##
    # filename = 'Test_LN_3Var_Gauss5.xlsx' # can be used when deactivating UserInput
    SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint,filename,sheet,targetfolder=UserInput(SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint)

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

            ###########################
            ### EXTRA: TESTING DATA ###
            ###########################

            if SW_Testing:
                Results = pd.read_excel(targetfolder+'PhaseResults\\m' + str(m) + '_PhaseThree_final.xlsx', 'result')

                # Testing LN variable
                mean_LN = 46.8
                cov_LN = 0.467401326

                K = pd.Series(index=Results.index.values)

                for entries in Results.index.values:
                    ### Kullback - Leibler divergence ###
                    #####################################
                    # print "\nKullback-Leibler divergence between true pdf and estimated pdf"
                    K[entries] = -Entropy(mean_LN, cov_LN, xmax_default) + Results.loc[entries, 'Znew']

                Results['K'] = K
                # reprint the Result dataframe
                Print_DataFrame([Results], targetfolder+'PhaseResults\\m' + str(m) + '_PhaseThree_final', ['result'])

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


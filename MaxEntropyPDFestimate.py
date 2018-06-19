# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-09"

from phase_one import *
from PhaseTwo import *
from PhaseThree import *
from PhaseFour import *
from phase_five import *
from GaussWeightsAndPoints import *

### NOTE ###
############
"""
MC or LHS input sample points of LN-distribution have been moved to separate file 'InputForTesting.py'

big difference with V3 => updated search algorithm for minimization based on fixed (random realization of) alpha

TO DO: beter alpha als tuple doorsturen naar Z etc. Huidige werkwijze is bullshit 

Of IDEE: doorsturen raw data etc. naar Entropy_Auxiliary en daarin dan "veilig" de alpha's en fractional moments constant !!!

the range of the distribution should (mostly) be clearly above 1. If this is not the case, change the dimension by multiplying with a factor
"""
# for example: calculation in m =>  calculation in mm

if __name__ == "__main__":

    """ ################################################################################## """
    """ ############################ INPUT SECTION ####################################### """
    """ ################################################################################## """

    ################
    ### SWITCHES ###
    ################

    SW_Testing = False  # indicate if test calculation or not -- if SW_Testing == True, the Kullback - Leibler divergence will be calculated

    SW_Debug = False  # OMIT standard application and DO SPECIAL REQUEST at end of the file

    SW_Gaussian = True  # function realizations Y(X) are based on Quadrature points for X... -- make sure to adapt filename etc accordingly

    ################
    ### CONTROLS ###
    ################

    nProc = 3 # number of processors

    mlist = [4]  # order of the PDF approximation - extend later for multi-m search conform (Inverardi and Tagliani, 2013)

    samples_rAlpha = 10 ** 2  # number of LHS samples Alpha - PHASE ONE - fixed Alpha values

    number_best_phase2 = 50  # number of best values considered for PHASE TWO
    number_best_phase3 = 10  # number of best values considered for PHASE THREE
    number_best_phase5 = 5  # number of best values considered for PHASE FIVE (i.e. considering m/N)

    """ TAKE NOTE TAKE NOTE TAKE NOTE """
    xmax_default = 1000.  # # extremely import variable if you move away from the LN testcase

    xmax_printing = 500.  # range for calc CDF and PDF -- make sure this is a float!!!!
    x_deltaprint = 1.

    #####################
    ###  DATA READING ###
    #####################

    filename = 'Test_LN_3Var_Gauss5.xlsx'

    """ ################################################################################## """
    """ ###################### STANDARD CALCULATION CORE ################################# """
    """ ################################################################################## """

    ###########################
    ### CALCULATION CENTER  ###
    ###########################

    RandomField_Eval = pd.read_excel('Samples\\' + filename, 'DATA')
    if SW_Gaussian:
        W = GaussWeighting(RandomField_Eval)
        tmp = pd.read_excel('Samples\\' + filename, 'MeanPointGauss')
        RandomField_Eval = RandomField_Eval.append(tmp)
    else:
        W = 0

    if SW_Debug == False:

        #################
        ###  CLEANING ###
        #################

        RemoveFolderData('CDF_PDF')
        RemoveFolderData('PhaseResults')

        for m in mlist:

            ###############################################
            ### PHASE ONE: OPTIMIZATION FOR GIVEN ALPHA ###
            ###############################################

            # 1) LHS generation of alpha-values
            # 2) determine lambda values through minimization + determine associated Z-value
            # 3) print results

            phase_one(m, samples_rAlpha, RandomField_Eval, W, xmax_default, nProc)

            ###########################################################
            ### PHASE TWO: LHS Monte Carlo AROUND BEST REALIZATIONS ###
            ###########################################################
            """ TO be elaborated later -- for now just accept the best result !!! """

            # currently....
            # 1) filters results for - first glance - acceptability
            # 2) determines reduced set of best results
            # 3) print reduced set

            PhaseTwo(m, number_best_phase2)

            ##########################################
            ### PHASE THREE: ACCEPTING BEST RESULT ###
            ##########################################

            # 1) recalculate lambda_0 with increased (numerical) accuracy
            # 2) recalculate Z-value
            # 3) print results - no PYTHON reordering of results yet...

            PhaseThree(m, xmax_default, RandomField_Eval, number_best_phase3, W)

            ###########################
            ### EXTRA: TESTING DATA ###
            ###########################

            if SW_Testing:
                Results = pd.read_excel('PhaseResults\m' + str(m) + '_PhaseThree_final.xlsx', 'result')

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
                Print_DataFrame([Results], 'PhaseResults\m' + str(m) + '_PhaseThree_final', ['result'])

            ###################################
            ### PHASE FOUR: POST-PROCESSING ###
            ###################################
            # officially post-processing, but filtering may be necessary => check if Fx(inf)==1 else the normalization in lambda_0 is imperfect

            # currently pure printing
            # could be another acceptance rule (see note above)

            # sometimes problems in printing may occur!! -- not yet coded for correction !!

            PhaseFour(m, xmax_printing, x_deltaprint)

        ################################
        ### PHASE FIVE: FINAL-RESULT ###
        ################################

        # read PhaseThree_final results for all m in mlist => determine reduced set of optimum overall simulations

        PhaseFive(mlist, number_best_phase5)

    else:

        """ ################################################################################## """
        """ ###################### TEST CENTER FOR DEBUGGING ################################# """
        """ ################################################################################## """

        #################################
        ### TEST CENTER for CONTROLS  ###
        #################################
        """ only executed if SW_Debug=False """

        print(RandomField_Eval)

        print()

        print(W)

        Print_DataFrame([W], 'Wtmp', ['result'])

        print()

        print(fraction_moment(0.3, RandomField_Eval, W))

        Points = GaussPoints(17)

        Print_DataFrame([Points], 'Ztmp', ['result'])

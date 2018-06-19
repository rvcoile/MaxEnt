# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2015-07-21"

from scipy.optimize import *
import multiprocessing as mp
import time
from Entropy_Auxiliary import *
from LatinHypercube import LHS_rand
from LocalAuxiliary import *
from PrintAuxiliary import *
import warnings


def z_optimization(Lambda, random_field_eval, alpha_list_for_z, W, x_max_default):

    M = [fraction_moment(i, random_field_eval, W) for i in alpha_list_for_z]

    alpha = alpha_list_for_z

    l0 = lambda_0(Lambda, alpha, xmax=x_max_default, limit=100000, method='quad')

    return l0 + np.sum(np.multiply(Lambda, M))


def wrapper_queue(arg):
    # kwargs, q = arg
    kwargs = arg
    result = fmin(z_optimization, **kwargs)
    # q.put(kwargs)
    return result


def phase_one(m, samples_r_alpha, random_field_eval, W, x_max_default, n_proc):

    # warnings.filterwarnings("ignore") # doesn't seem to make a difference here

    # OPTIMISATION FUNCTION DEFINITION
    # ================================

    # def z_optimization(Lambda):
    #     M = [fraction_moment(i, random_field_eval, W) for i in alpha_list_for_z]
    #     alpha = alpha_list_for_z
    #
    #     l0 = lambda_0(Lambda, alpha, xmax=x_max_default, limit=100000, method='quad')
    #     return l0 + np.sum(np.multiply(Lambda, M))

    ### LHS alpha generation ###
    ############################

    A_range = [-2, 2]  # range for fractional exponents
    AlphaList = Alpha_List(m)

    aselect = LHS_rand(samples_r_alpha, m)
    aselect = aselect.as_matrix()
    aselect = pd.DataFrame(aselect, index=np.arange(1, samples_r_alpha + 1, 1), columns=AlphaList)
    tmp = aselect.multiply(A_range[1] - A_range[0])
    Alpha = tmp.add(A_range[0])

    ### optimization calculation for lambdas ###
    ############################################

    value = pd.DataFrame(index=np.arange(1, samples_r_alpha + 1, 1), columns=['Z'])
    LambdaList = Lambda_List(m)
    Lambda = pd.DataFrame(index=np.arange(1, samples_r_alpha + 1, 1), columns=LambdaList)

    # MAKE WRAPPED INPUT VARIABLES IN THE FORM OF KWARGS
    # ==================================================

    list_kwargs = []

    for simulations in Alpha.index.tolist():
        lambda_starting = Lambda_Starting(m)
        alpha_list_for_z = Alpha.loc[simulations, :]
        alpha_list_for_z = alpha_list_for_z.values

        # (minimum_opt, Zval, extra1, extra2, extra3) = fmin(z_optimization, lambda_starting, maxfun=1000, maxiter=1000,
        #                                                    full_output=True)  # can be optimized by not recalculating fractional moment every time... (input as arguments)
        # (minimum_opt,Zval,d)=fmin_l_bfgs_b(Z,LambdaStarting,approx_grad=True)

        list_kwargs.append({
            # "func": z_optimization,
            "x0": lambda_starting,
            "args": (random_field_eval, alpha_list_for_z, W, x_max_default),
            "maxfun": 1000,
            "maxiter": 1000,
            "full_output": True,
            "disp": False,
            # "alpha_list_for_z": alpha_list_for_z,
            # "random_field_eval": random_field_eval,
            # "Lambda": Lambda,
            # "W": W,
            # "x_max_default": x_max_default,
        })

    # MINIMISATION CALCULATION
    # ========================

    # Defined variables
    # -----------------

    # n_proc = 1 # number of processors

    # Derived variables
    # -----------------

    n_iteration = len(list_kwargs)

    # Calculation main body
    # ---------------------

    # m_ = mp.Manager()
    p = mp.Pool(n_proc)
    # q = m_.Queue()
    # jobs = p.map_async(wrapper_queue, [(kwargs, q) for kwargs in list_kwargs])
    jobs = p.map_async(wrapper_queue, [(kwargs) for kwargs in list_kwargs])

    time_start = time.time()
    while True:
        if jobs.ready():
            print("Simulation completed in {} min.".format(str((time.time()-time_start)/60)))
            break
        # else:
        #     print("{:25}{:<10.3f}{:10}".format("Simulation progress", q.qsize() * 100 / n_iteration, "%"))
        #     time.sleep(5)
    p.close()
    p.join()
    j = jobs.get()

    results = np.array(j)

    for i, each_results in enumerate(results):
        minimum_opt, Zval, _, _, _ = each_results

        Zval = max(Zval, -1000)

        value.loc[i+1, :] = Zval
        Lambda.loc[i+1, :] = minimum_opt

    Print_DataFrame([Alpha, Lambda, value], 'PhaseResults\m' + str(m) + '_PhaseOne', ['Alpha', 'Lambda', 'value'])

from typing import List, Any


def prop_finder(prop_array,t):
    # Inputs: prop_array-array of propeller object as defined in propeller class
    pvals = [[], [], []]  # 0 - indices of the props, 1-index of T array, 2 - Power value
    i_prop = 0
    for prop in prop_array:
        for i in range(len(prop.T)-2):
            t1 = prop.T[i]
            t2 = prop.T[i+1]

            if (t1 <= t < t2) or (t1 > t >= t2):
                # making an array of indecies and power values to minimize later
                pvals[0].append(i_prop)
                pvals[1].append(i)
                pval = prop.P[i]
                pvals[2].append(pval)

        i_prop += 1

    # Finding the optimal propeller
    p_opt = min(pvals[3])
    i_inpopt  = pvals[3].index(p_opt)
    i_optprop = pvals[0][i_inpopt]
    i_tval    = pvals[1][i_optprop]
    opt_prop  = prop_array[i_optprop]

    return [i_tval, p_opt, opt_prop]
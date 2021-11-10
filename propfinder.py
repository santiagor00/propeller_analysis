from typing import List, Any


def prop_finder(prop_array, t):
    # Inputs: prop_array-array of propeller object as defined in propeller class
    pvals = [[], [], []]  # 0 - indices of the props, 1-index of T array, 2 - Power value
    i_prop = 0
    for prop in prop_array:
        for i in range(len(prop.thrust_list)-2):
            t1 = prop.thrust_list[i]
            t2 = prop.thrust_list[i+1]

            if (t1 <= t < t2) or (t1 > t >= t2):
                # making an array of indecies and power values to minimize later
                pvals[0].append(i_prop)
                pvals[1].append(i)
                pval = prop.power_list[i+1]
                pvals[2].append(pval)

        i_prop += 1

    # Finding the optimal propeller
    p_opt = min(pvals[2])
    i_inpopt  = pvals[2].index(p_opt) # Index of the optimal propeller in p_opt
    i_optprop = pvals[0][i_inpopt] # Index of the optimal prop in prop_list

    i_inprop  = pvals[1][i_optprop] # Index of the thrust value in thrust list
    opt_prop  = prop_array[i_optprop] # Optimal prop objects

    return [i_inprop, p_opt, opt_prop]

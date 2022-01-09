from funcs import *

def main():
   # ========================== Inputs ======================================= #

   weight = 21  # total weight of the multicopter in lbf
   thrust_to_weight_ratio = 2  # ratio of total propeller thrust to total multicopter weight
   num_propellers = 4  # number of propellers on the multicopter

   x_axis = 'rpm'  # can be: rpm, thrust, power, torque, cp, ct
   y_axis = 'thrust'  # can be: rpm, thrust, power, torque, cp, ct

   interpolate = True  # Do you want to interpolate? (True/False)
   num_winners = 10  # How many best propellers will be shown

   # =========================================================================== #

   req_thrust = weight * thrust_to_weight_ratio / num_propellers

   text = get_text('static_data.txt')
   data = get_data(text)

   propellers_list = objectify(data)

   print(len(propellers_list), 'propellers analyzed')

   if interpolate:
      winners_list = interpolate_best_n_propellers(propellers_list, req_thrust, num_winners)
      print_winners_interpolated(winners_list, req_thrust)
      plot_winners_interpolated(winners_list, x_axis, y_axis, req_thrust)

   else:
      winners_list = find_best_n_propellers(propellers_list, req_thrust, num_winners)
      print_winners(winners_list)
      plot_winners(winners_list, x_axis, y_axis, req_thrust)


if __name__ == "__main__":
   main()

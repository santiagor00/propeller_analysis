from objects import *
import matplotlib.pyplot as plt


def get_text(filename):
   with open(filename, 'r') as spreadsheet:
      lines = spreadsheet.readlines()
      text = []
      for line in lines:
         text.append(line.split())
   return text


def get_data(text):
   data = []
   data_line = [None, []]
   for line in text:
      try:
         int(line[0][0])  # checks if line has a propeller name or numerical data
         try:
            data_line[1].append([float(x) for x in line])  # try append list of floats to data line
         except:
            if data_line[0] != None:
               data.append(data_line)
            data_line = [None, []]
            data_line[0] = line[0].strip('.dat')
      except:
         pass
   data.append(data_line)
   return data


def transpose(matrix):
   transposed_matrix = [[] for _ in range(len(matrix[0]))]
   for j in range(len(matrix[0])):
      for i in range(len(matrix)):
         transposed_matrix[j].append(matrix[i][j])
   return transposed_matrix


def objectify(data):
   """
   Creates a list of Propeller objects from the data
   """
   propeller_list = []  # initialize list of Propeller objects
   for line in data:
      propeller_name = line[0]
      numerical_data = transpose(line[1])  # list of lists of rpm's, torques, etc.

      propeller = Propeller()
      propeller.name = propeller_name
      propeller.rpm_list = numerical_data[0]
      propeller.thrust_list = numerical_data[1]
      propeller.power_list = numerical_data[2]
      propeller.torque_list = numerical_data[3]
      propeller.cp_list = numerical_data[4]
      propeller.ct_list = numerical_data[5]

      propeller_list.append(propeller)
   return propeller_list


def find_optimal_condition(propeller, req_thrust):
   thrust_list = propeller.thrust_list
   power_list = propeller.power_list

   optimal_power = None
   optimal_thrust = None
   optimal_i = None
   for i in range(len(power_list)):
      if thrust_list[i] >= req_thrust:
         if (optimal_power is None) or (power_list[i] < optimal_power) or \
                 ((optimal_power == power_list[i]) and (optimal_thrust < thrust_list[i])):
            optimal_power = power_list[i]
            optimal_thrust = thrust_list[i]
            optimal_i = i
   return optimal_thrust, optimal_power, optimal_i


def find_optimal_propeller(propellers_list, req_thrust):
   """
   inputs: list of propeller objects, required thrust
   outputs: propeller object, thrust, power
   finds the propeller with the lowest power
   """
   optimal_propeller = None
   overall_optimal_thrust = None
   overall_optimal_power = None
   i = None

   for propeller in propellers_list:
      optimal_thrust, optimal_power, optimal_i = find_optimal_condition(propeller, req_thrust)
      if optimal_thrust is not None:
         if (optimal_propeller is None) or (optimal_power < overall_optimal_power) or \
                 ((optimal_power == overall_optimal_power) and (optimal_thrust > overall_optimal_thrust)):
            overall_optimal_thrust = optimal_thrust
            overall_optimal_power = optimal_power
            optimal_propeller = propeller
            i = optimal_i
   return optimal_propeller, i


def find_best_n_propellers(propellers_list, thrust_req, n):
   winners_list = []  # contains tuples containing propeller object and index of optimal condition
   for _ in range(n):
      propeller, i = find_optimal_propeller(propellers_list, thrust_req)
      winners_list.append((propeller, i))
      propellers_list.remove(propeller)
   return winners_list


def print_results(propeller, i):
   print(f"""
         Name:   {propeller.name}
         RPM:    {propeller.rpm_list[i]} rpm
         Thrust: {propeller.thrust_list[i]} lbf
         Power:  {propeller.power_list[i]} hp
         Torque: {propeller.torque_list[i]} in-lbf
         Cp:     {propeller.cp_list[i]}
         Ct:     {propeller.ct_list[i]}
         """)


def print_winners(winners_list):
   for winner in winners_list:
      propeller = winner[0]
      i = winner[1]
      print_results(propeller, i)
      print("\n")


def plot_winners(winners_list, x_axis: str, y_axis: str, req_thrust):
   x_attr = x_axis + '_list'
   y_attr = y_axis + '_list'
   for winner in winners_list:
      propeller = winner[0]
      i = winner[1]
      x_list = getattr(propeller, x_attr)
      y_list = getattr(propeller, y_attr)
      plt.plot(x_list, y_list, label=propeller.name, linewidth=1)
      plt.plot(x_list[i], y_list[i], marker='.', markersize='3', c='black')

   labels = {'rpm': 'RPM', 'thrust': 'Thrust (lbf)', 'power': 'Power (hp)', 'torque': 'Torque (in-lbf)',
             'cp': 'Cp', 'ct': 'Ct'}

   plt.xlabel(labels.get(x_axis))
   plt.ylabel(labels.get(y_axis))
   plt.legend()

   if x_axis == 'thrust':
      plt.axvline(x=req_thrust, c='r', linestyle='--', linewidth=1)
   elif y_axis == 'thrust':
      plt.axhline(y=req_thrust, c='r', linestyle='--', linewidth=1)
   plt.grid()
   plt.show()


def print_all_tables(data):
   """
   prints data for each propeller in tables
   just used to visually check that all the obtained data is consistent with original data file
   """
   for propeller_data in data:
      print('\n', propeller_data[0])
      w = 10  # table column spacing

      print(f'{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}'.format(
         'RPM', 'THRUST', 'POWER', 'TORQUE', 'Cp', 'Ct'))
      print(f'{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}'.format(
         '', '(LBF)', '(HP)', '(IN-LBF)', '', ''))
      print('-' * 6 * w)
      for line in propeller_data[1]:
         rpm = line[0]
         thrust = line[1]
         power = line[2]
         torque = line[3]
         cp = line[4]
         ct = line[5]
         print(f'{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}{{:<{w}}}'.format(
            rpm, thrust, power, torque, cp, ct))


# ============================ Interpolation Functions ============================ #

def interpolate_optimal_condition(propeller, req_thrust):
   rpm_list = propeller.rpm_list
   thrust_list = propeller.thrust_list
   power_list = propeller.power_list
   torque_list = propeller.torque_list
   optimal_rpm = None
   optimal_power = None
   optimal_torque = None
   for i in range(len(power_list) - 1):
      if thrust_list[i + 1] >= req_thrust:
         optimal_rpm = rpm_list[i] + \
                       (rpm_list[i + 1] - rpm_list[i]) * (req_thrust - thrust_list[i]) / (
                               thrust_list[i + 1] - thrust_list[i])
         optimal_power = power_list[i] + \
                         (power_list[i + 1] - power_list[i]) * (req_thrust - thrust_list[i]) / (
                                 thrust_list[i + 1] - thrust_list[i])
         optimal_torque = torque_list[i] + \
                          (torque_list[i + 1] - torque_list[i]) * (req_thrust - thrust_list[i]) / (
                                  thrust_list[i + 1] - thrust_list[i])
         return optimal_rpm, optimal_power, optimal_torque
   return None, None, None


def interpolate_optimal_propeller(propellers_list, req_thrust):
   """
   inputs: list of propeller objects, required thrust
   outputs: propeller object, thrust, power
   finds the propeller with the lowest power
   """
   optimal_propeller = None
   overall_optimal_rpm = None
   overall_optimal_power = None
   overall_optimal_torque = None

   for propeller in propellers_list:
      optimal_rpm, optimal_power, optimal_torque = interpolate_optimal_condition(propeller, req_thrust)

      if optimal_power is not None:
         if (optimal_propeller is None) or (optimal_power < overall_optimal_power):
            optimal_propeller = propeller
            overall_optimal_rpm = optimal_rpm
            overall_optimal_power = optimal_power
            overall_optimal_torque = optimal_torque

   return optimal_propeller, overall_optimal_rpm, overall_optimal_power, overall_optimal_torque


def interpolate_best_n_propellers(propellers_list, req_thrust, n):
   winners_list = []  # list of tuples containing propeller object, rpm, power, torque
   for _ in range(n):
      propeller, rpm, power, torque = interpolate_optimal_propeller(propellers_list, req_thrust)
      winners_list.append((propeller, rpm, power, torque))
      propellers_list.remove(propeller)
   return winners_list


def print_results_interpolated(name, rpm, power, torque, req_thrust):
   print(f"""
         Name:   {name}
         RPM:    {rpm} rpm
         Thrust: {req_thrust} lbf
         Power:  {power} hp
         Torque: {torque} in-lbf
         """)


def print_winners_interpolated(winners_list, req_thrust):
   for k in range(len(winners_list)):
      print("")
      print(f"#{k + 1} Best Propeller:")
      name = winners_list[k][0].name
      rpm = winners_list[k][1]
      power = winners_list[k][2]
      torque = winners_list[k][3]
      print_results_interpolated(name, rpm, power, torque, req_thrust)
      print("\n")


def plot_winners_interpolated(winners_list, x_axis: str, y_axis: str, req_thrust):
   x_attr = x_axis + '_list'
   y_attr = y_axis + '_list'
   for winner in winners_list:
      propeller = winner[0]

      x_list = getattr(propeller, x_attr)
      y_list = getattr(propeller, y_attr)
      plt.plot(x_list, y_list, label=propeller.name, linewidth=1,
               marker='.', markersize='3')
      interpolated_values = {'rpm': winner[1], 'power': winner[2], 'torque': winner[3], 'thrust': req_thrust}

      if (x_axis != 'cp') and (x_axis != 'ct') and (y_axis != 'cp') and (y_axis != 'ct'):
         plt.plot(interpolated_values.get(x_axis), interpolated_values.get(y_axis),
                  marker='o', markersize='4', c='black')

   labels = {'rpm': 'RPM', 'thrust': 'Thrust (lbf)', 'power': 'Power (hp)', 'torque': 'Torque (in-lbf)',
             'cp': 'Cp', 'ct': 'Ct'}

   plt.xlabel(labels.get(x_axis))
   plt.ylabel(labels.get(y_axis))
   plt.legend()

   if x_axis == 'thrust':
      plt.axvline(x=req_thrust, color='r', linestyle='--', linewidth=1)
   elif y_axis == 'thrust':
      plt.axhline(y=req_thrust, color='r', linestyle='--', linewidth=1)
   plt.grid()
   plt.show()

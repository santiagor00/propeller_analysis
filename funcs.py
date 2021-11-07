from objects import *

def get_text(filename):
   with open(filename, 'r') as spreadsheet:
      lines = spreadsheet.read().splitlines()
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


def print_data(data):
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






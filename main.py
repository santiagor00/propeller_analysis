from funcs import *
from propfinder import *

def main():
   text = get_text('static_data.txt')
   data = get_data(text)
   propeller_list = objectify(data)
   for propeller in propeller_list:
      print(propeller.thrust_list)

   optpropout = prop_finder(propeller_list, 6)
   print(optpropout[2].power_list,optpropout[2].thrust_list)

if __name__ == "__main__":
   main()
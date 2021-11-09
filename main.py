from funcs import *

def main():
   text = get_text('static_data.txt')
   data = get_data(text)
   propeller_list = objectify(data)
   for propeller in propeller_list:
      print(propeller.thrust_list)

if __name__ == "__main__":
   main()
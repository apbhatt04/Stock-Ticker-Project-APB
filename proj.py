    ###########################################################

    # Prompt and check for file names

    #  Use function to read data

    #  Run calculations (max, average) using data

    #  Create a function to display items in a list

    #  Display menu and prompt for choice

    #  Display and format output

    #  End program if prompted

    ###########################################################

import csv

MENU = '''\nSelect an option from below:
            (1) Display all companies in the New York Stock Exchange
            (2) Display companies' symbols
            (3) Find max price of a company
            (4) Find the company with the maximum stock price
            (5) Find the average price of a company's stock
            (6) quit
    '''
WELCOME = "Welcome to the New York Stock Exchange.\n"
    
def open_file():
    '''This function prompts for files and return 2 file pointers.
       parameters: None
       returns: prices and securities file pointers.'''
    
    prices_fp_input = input("\nEnter the price's filename: ")
    while True: #Ensure that prices file exists
        try:
            prices_fp = open(prices_fp_input)
            break
        except FileNotFoundError:
            prices_fp_input = input("\nEnter the price's filename: ")
            
    security_fp_input = input("\nEnter the security's filename: ")
    while True: #Ensure that securities files exists
        try:
            securities_fp = open(security_fp_input)
            break
        except FileNotFoundError:
            security_fp_input = input("\nEnter the security's filename: ")

    return prices_fp, securities_fp

def read_file(securities_fp):
    '''This function takes a fp and returns a set and dictionary containing company data.
       parameters: a fp containing securities data
       returns: a set of all company names in fp and a dictionary of company data'''

    reader = csv.reader(securities_fp)
    next(reader, None)

    master_dict = {} #Create a dictionary to store all the values.
    master_set = set()
    
    for line in reader:
        code = line[0]
        name = line[1]
        sector = line[3]
        subsector = line[4]
        address = line[5]
        date_add = line[6]
        blank = []

        master_dict[code] = [name, sector, subsector, address, date_add, blank]    
        master_set.add(name)
        
    return master_set, master_dict

def add_prices (master_dictionary, prices_file_pointer):
    '''This function adds price information to the master dictionary.
       parameters: a master dictionary containing all company data, and a fp containing price data.
       returns: None'''

    reader = csv.reader(prices_file_pointer)
    next(reader, None)

    for line in reader:
        date = line[0]
        name = line[1]
        open_num = float(line[2])
        close_num = float(line[3])
        low_num = float(line[4])
        high_num = float(line[5])
        app_list = [date, open_num, close_num, low_num, high_num]

        for key, value in master_dictionary.items():
            if key == name:
                value[5].append(app_list)

    return None
    
def get_max_price_of_company(master_dictionary, company_symbol):
    '''This function finds the max high price of given company in the master dictionary.
       parameters: master dictionary containing company data, and a three letter ticker symbol
       returns: a tuple containing the max price and its corresponding date.'''
    
    master_list = []
    price_max = 0

    for key, values in master_dictionary.items():
        if key == company_symbol:
            for lists in values[5]:
                tup = (lists[4], lists[0]) #Returns the high price and the date
                master_list.append(tup)
                price_max = max(master_list) #Find the max
        elif company_symbol not in master_dictionary.keys():
            tup = (None, None)
            return tup

    return price_max


def find_max_company_price (master_dictionary):
    '''This function finds the company with the highest max high price in a dictionary. 
       parameters: master dictionary containing all the company data.
       returns: a tuple containing company and the max high price.'''
    max_list = []
    for key, value in master_dictionary.items():
        if value[5] != []: #If the price list is not empty...
            company_max_price = get_max_price_of_company(master_dictionary, key)
            tup = (company_max_price[0], key)
            max_list.append(tup) #Append to a list of tuples
    
    max_comp = max(max_list) 

    return_tup = max_comp[::-1] #Reverse the tuple to get the correct output

    return return_tup
    

def get_avg_price_of_company (master_dictionary, company_symbol):
    '''This function finds the average high price for a specified company.
       parameters: a master dictionary containing company data and the string ticker symbol for the company
       returns: float value of the average high price for the company.'''
    average_list = []

    for key, values in master_dictionary.items():
        if key == company_symbol and values[5] != []:
            for lists in values[5]:
                average_list.append(lists[4]) #Append the high price
        if company_symbol not in master_dictionary.keys():
            average_list.append(0.0)
        if key == company_symbol and values[5] == []:
            average_list.append(0.0)
        

    average = sum(average_list)/len(average_list) #Find the average 

    return round(average,2)
            
def display_list(lst): 
    '''This function displays a list of values in a specific format.
       parameters: a list 'lst' containing string values.
       returns: None'''
       
    for i in range(0, len(lst), 3):
        count = 0
        for a in lst[i:i+3]:
            count = count + 1 #Increase the count by 1 for every iterated element
            print("{:^35s}".format(a), end = "")
        if count == 3:
            print() #Print a new line
        elif count < 3:
            print()

    print((count-2) * "\n") #Subtract count by 2 to account for extra print statements
        
    return None
    
def main():
    print(WELCOME)

    prices_fp, securities_fp = open_file() 
    master_set, master_dictionary = read_file(securities_fp)
    
    add_prices(master_dictionary, prices_fp) #Add the prices to the master dictionary


    print(MENU)
    user_input = input("\nOption: ")

    while user_input not in "123456": #If the option is invalid, print error statement.
        print("\nInvalid option. Please try again.")
        user_input = input("\nOption: ")

    while user_input != "6":

        if user_input == "1":
            lst = sorted(master_set) #Sort alphabetically
            print("\n{:^105s}".format("Companies in the New York Stock Market from 2010 to 2016"))
            display_list(lst)

            print(MENU)
            user_input = input("\nOption: ")

        
        elif user_input == "2":
            lst = sorted(master_set)
            lst2 = []

            
            for keys, values in master_dictionary.items():
                for comp in lst:
                    if comp == values[0]:
                        lst2.append(keys)

            lst2 = sorted(lst2) #Sort list of company symbols

            print("\ncompanies' symbols:")
            display_list(lst2)

            print(MENU)
            user_input = input("\nOption: ")


        elif user_input == "3":
            symbol_input = input("\nEnter company symbol for max price: ")
            
            if symbol_input not in master_dictionary.keys():
                print("\nError: not a company symbol. Please try again.")
                symbol_input = input("\nEnter company symbol for max price: ")
              
            if symbol_input in master_dictionary.keys():
                max_price = get_max_price_of_company(master_dictionary,  symbol_input) #Find max price
                
                      
                if max_price != 0:
                    print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".format(max_price[0], max_price[1]))
                else:
                    print("\nThere were no prices.")
                 
                
            print(MENU)
            user_input = input("\nOption: ")

        elif user_input == "4":
            max_ticker = find_max_company_price(master_dictionary)
            print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".format(max_ticker[0], max_ticker[1]))
    
            
            print(MENU)
            user_input = input("\nOption: ")

        elif user_input == "5":
            
            
            average_symbol = input("\nEnter company symbol for average price: ")
            
            if average_symbol not in master_dictionary.keys():
                print("\nError: not a company symbol. Please try again.")
                average_symbol = input("\nEnter company symbol for average price: ")
                
            if average_symbol in master_dictionary.keys():
                avg_price = get_avg_price_of_company(master_dictionary, average_symbol)
                print("\nThe average stock price was ${:.2f}.\n".format(avg_price))
            
            print(MENU)
            user_input = input("\nOption: ")
                

       
if __name__ == "__main__": 
    main() 

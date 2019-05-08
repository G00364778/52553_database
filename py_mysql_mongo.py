'''
This is a pythin based console application that connects to background 
Database MySQL and MongoDB application to perform various display and 
update functions from a menu driven console interface.

The application depends on a local MySQL and MongoDB database to be up 
and running.

The application also requires some non standard pythoin libraries to be 
installed. Check the dependancies from the console menu "c" or run the 
check_dependansies() command from the console.

Run the application from a python or command console.

'''
debug = False
country_data_loaded = False
mongoclient=None
df=None
import pymysql
import pymongo
#import collections
from collections.abc import MutableMapping 
from terminaltables import AsciiTable
from pkgutil import iter_modules
import keyboard
import os
import sys
import re
import pandas as pd

# Main function
def main():
    '''
    Display the menu and execute the choices returned from the user selection menu
    '''
    global mongoclient
    display_menu()

    while True:
        choice = input("Enter choice: ").strip()
        if (choice == "1"):
            view_15_cities()
            display_menu()
        elif (choice == "2"):
            view_cities_by_population()
            display_menu()
        elif (choice == "3"):
            add_new_city()
            display_menu()
        elif (choice == "4"):
            find_car_by_enginesize()
            display_menu()
        elif (choice == "5"):
            add_new_car()
            display_menu()
        elif (choice == "6"):
            view_countries_by_name()
            display_menu()
        elif (choice == "7"):
            view_countries_by_population()
            display_menu()
        elif (choice == "c"):
            check_dependansies()
            display_menu()
        elif (choice == "x"):
            # gracefully terminate the mongo client connection
            # mongoclient.close()
            break
        else:
            display_menu()

def view_15_cities():
    while True:
        '''
        Clear the screen between menu selections
        '''
        clear()
        #print('View 15 Cities')
        query = "select * from city limit 15;"
        print('\rrunning query, please wait ..... ',end='')
        result = mysql_query(query)
        #clear()
        print('\rView 15 Cities                   ')
        print_nice(result)
        wait_here()
        return True

def view_cities_by_population():
    '''
    This fiunction is called from the main console menu.

    Cities by population connects the the MySQL database and executes the query
    after appending the where clause returned by the 'add_where_clause' function.

    The returned query result then uses another function 'print_nice' to create 
    an ascii table style output to the console of the query result returned and waits
    for the spacebar key beore proceeding back to the menu.
    '''
    clear()
    print('Cities by population\nCreate population filter')
    wc=add_where_clause()
    query = "SELECT * FROM world.city as c " + wc + " order by c.Population"
    print('\rRunning Cities by population query ...',end='')
    result = mysql_query(query)
    print('\rCities by population                  ')
    print_nice(result)
    wait_here()
    return True
        
def add_new_city():
    '''
    This function is called from the main console menu.

    add_new_city prompts for user data input and adds a new city the the mysql 
    database. 
    '''
    print('Add new city')
    citydata = prompt_city_data()
    mysql_add_city_data(citydata)
    wait_here()
    return True
    
    
def find_car_by_enginesize():
    '''
    This function is called from the main console menu.

    find_car_by_enginesize prompts the user for input and creates a query using the imput
    to show the enginesizes in an flattened ascii table returned by the mongodb query.

    The function uses the following internal function calls to complete and parse the query data.

        mongo_connect()
        mongo_to_list()
        print_nice()
        wait_here()

    '''
    global mongoclient
    Valid=False
    while Valid == False:
        size = input("Enter enginesize (eg 1.5 or * for all) : ").strip()
        if size == '*':
            Valid=True
        elif len(size)>=1:
            enginsize=float(size)
            if (enginsize > 0.8 and enginsize < 5.0):
                Valid = True
    if size == '*':
        query={'$and':[{'car':{'$exists':'true'}}]}
    else:
        query={'$and':[{'car':{'$exists':'true'}},{'car.engineSize':enginsize}]}
    print('\rProcessing query ....',end='')
    mongoclient=mongo_connect(mongoclient)
    print('\rCar by enginesize     ')
    #cars=mongo_find(mongoclient,'proj','docs',{"car":{"$exists":"true"}})
    cars=mongo_find(mongoclient,'proj','docs',query)
    if debug==True:
        for car in cars:
            print(car)
    car_list=mongo_to_list(cars)
    print_nice(car_list)
    wait_here()
    return True

def add_new_car():
    '''
    This function is called from the main console menu.

    add_new_car creates a new enrt in the mongodb database from the user input provided 
    in the console prompts. The prompt input is collected and returned by a sub-function.

    The followjng sub-functions are called from here:

        add_new_car_get_data()
        mongo_add_data()
        wait_here()

    The sub function details discussed in their own space.
    '''
    print('Add new Car')
    cardetails=add_new_car_get_data()
    id,reg,cc=cardetails
    id=float(id) # in line with exixsting variable types for cars??
    # print(id,reg,cardetails)
    db="proj"
    collection="docs"
    # newDoc = {"_id":7, "car":{"reg":"99-D-69674", "enginesize":1.0}}
    newDoc = {"_id":id, "car":{"reg":reg, "enginesize":cc}}
    mongodb_add_data(db,collection,newDoc)
    wait_here()
    return True

def view_countries_by_name():
    '''
    This function is called from the main console menu

    This function queries the MySQl databases and return all the data in the 
    world.country table to a pandas dataframe and then processes all subsequent 
    request for data from the dataframe.

    To load an up to date copy for any queries related to the table the console 
    application must be terminted and restarted or set the global variable 
    country_data_loaded to False and the next call to any of the queries will 
    reload the data from the database.

    This function depends on the following sub functions:
        country_data_to_df()
        reduce_df_to_header_list()
        AsciiTable() - external library
        wait_here()

    The table outputs the list of countries filtered by the country name or partial 
    name entered at the user console inputs.

    '''
    print('Countries by name')
    if country_data_loaded == False:
        country_data_to_df()
    else:
        print('Data aready loaded')
    cname = input('Enter the full/partial country name: ').strip()
    case = input('Case sensitive? (True/False): ').strip().capitalize()
    if case.startswith('True'):
        case = True
    elif case.startswith('False'):
        case = False
    else:
        case = False
    datalist = reduce_df_to_header_list('Name', cname, 'str', case)
    table=AsciiTable(datalist)
    print(table.table)
    wait_here()
    return True

def view_countries_by_population():
    '''
    This function is called from the main console menu

    This function queries the MySQl databases and return all the data in the 
    world.country table to a pandas dataframe and then processes all subsequent 
    request for data from the dataframe.

    To load an up to date copy for any queries related to the table the console 
    application must be terminted and restarted or set the global variable 
    country_data_loaded to False and the next call to any of the queries will 
    reload the data from the database.

    This function depends on the following sub functions:
        country_data_to_df()
        reduce_df_to_header_list()
        AsciiTable() - external library
        wait_here()

    The table outputs the list of countries filtered by the country population criteria 
    entered at the user console inputs.

    '''
    print('Countries by population')
    if country_data_loaded == False:
        country_data_to_df()
    else:
        print('Data aready loaded')
    pfilter=input('Enter a population filter (eg. <=1000): ').strip()
    if pfilter.strip().startswith('<') or pfilter.strip().startswith('>'):
        pfilter=pfilter
    elif pfilter.strip().startswith('='):
        if pfilter.strip().startswith('=='):
            pfilter=pfilter
        else:
            pfilter='='+pfilter
    elif pfilter.isalnum:
        pfilter='=='+pfilter
    datalist = reduce_df_to_header_list('Population', pfilter, 'val', False)
    table=AsciiTable(datalist)
    print(table.table)
    wait_here()
    return True

def check_dependansies(mode='show_missing'):
    '''
    This function is an extra function called from the console menu. 

    The purpose of the function is to verify that all dependant python libraries are installed
    and available that is required to run this application. 

    mode options:
       show_missing: show only missisng items
      show_required: show a list of required modules

    This function is dependant on the followin submodules

        module_exists()

    '''
    module_list=['pymysql','pymongo', 'terminaltables', 'keyboard', 'pandas', 'collections', 'pkgutil']
    if mode == 'show_missing':
        some_missing=False
        print('Running Application dependancy checker\n')
        for module in  module_list:
            exist=module_exists(module)
            if exist == False:
                some_missing=True
                print('\tMissing: {}'.format(module))    
        if some_missing==True:
            print('\n Please install missing components first')
        else:
            print('No missing modules')
    elif mode == 'show_required':
        print('Required modules:')
        for module in module_list:
            print('\t',module)
    wait_here()
    return True

def display_menu():
    '''
    This function generates the console menu for the console application 
    and is called from the main() function.
    '''
    clear()
    print("World DB")
    print("--------")
    print("")
    print("MENU")
    print("=" * 4)
    print("1 - View 15 Cities")
    print("2 - View Cities by population")
    print("3 - Add New City")
    print("4 - Find car by enginesize")
    print("5 - Add New Car")
    print("6 - View Countries by name")
    print("7 - View Countries by population")
    print("c - Check dependancies")
    print("x - Exit")

def module_exists(module_name):
    '''
    module_exixts is a sub function iterating through a list of names passed to the function
    and simply returning True or false if able to determine of the module name is available 
    to be called or loaded.

    parameters passed into the module is a python library name.
    '''
    return module_name in (name for loader, name, ispkg in iter_modules())

def reduce_df_to_header_list(columnName, filterstr, filtertype='str',caseSenstive=True):
    '''
    this sub-function references the globally decaled dataframe df and creates a subset from
    the complete dataset in the dataframe based on the filter criteria passed into the function.

    The function call accepts four parameters and the last two is optional.

        columnName:   - See list below
        filterstr:    - examples: 'Ire' for str types or '<1000' for val etc
        filtertype:   - 'str' or 'val'
        caseSenstive: - True or False

    Available column names are:
        (['Capital', 'Code', 'Continent', 'GNP', 'GovernmentForm', 'HeadOfState',
        'IndepYear', 'LifeExpectancy', 'LocalName', 'Name', 'Population',
        'Region', 'SurfaceArea']

        The list of names is generated calling the pandas command df.columns

        The rest of the code the creats a python list of values with a header row and
        rows of data ready to create user friendly asccii tables and returns this data
        to the calling function in a python list format.

    '''
    if filtertype.lower().__contains__('str'):
        filtered=df[df[columnName].str.contains(filterstr,case=caseSenstive)]
    elif filtertype.lower().__contains__('val'):
        #filtered = df[df[columnName]<1000]
        filtered=df[eval('df[columnName]'+filterstr)]
    # extract headings
    header=list(filtered)
    # extract rows
    rows=filtered.values.tolist()
    dat=[]
    dat.append(header)
    for row in rows:
        dat.append(row)
    return dat

def country_data_to_df():
    '''
    This sub-function is not called directly but rather called from 
    view_counries_by_population() and view_countries_by_name().

    This routine fundamentally calls routines to connect to the MySQL 
    database and load the country  data into a dataframe for subsequent 
    refinement and interrogation and the dataframe is active and accessible 
    globally for the duration of the python session.

    This function is dependant on:
        load_country_data()
    
    The function take the query result and converts it to a dataframe df that
    is accessible globally.

    '''
    global df
    global country_data_loaded
    print('\rLoading country data to memory...', end='')
    countries=load_country_data()
    df=pd.DataFrame(countries)
    country_data_loaded=True
    print('\rCountry data loaded to memory    ')

def load_country_data():
    '''
    This sub-function executes a mysql query on the database and returns the
    query result or en error to the calling routine.
    '''
    #load and store country data in memory for functions 6 and 7 calls
    try:
        country_data=mysql_query("select * from country")
    except Exception as e:
        print(e)
    else:
        return country_data


def mysql_add_city_data(citydata):
    '''
    This routine creates a database connection and inserts new city data 
    passed to the function into the mysql word.city database. 

    The data passed into the routine is a python list that requires four parameters
    passed into the routine:

        Name         - Name of the new city added
        CountryCode  - A valid country code, if not valid the entry will fail 
        District     - The name of the district or county
        Population   - The population of the city added

    The function call on completion will return a success or failure message. 

    '''
    conn = pymysql.connect( "localhost", "root", "root", "world", 
                    cursorclass=pymysql.cursors.DictCursor)
    ins = "Insert INTO city (Name, CountryCode, District, Population) VALUE(%s, %s, %s, %s)"

    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(ins, (citydata[0], citydata[1], citydata[2], citydata[3]))
            conn.commit()   
            print("Insert successful")
        except Exception as e:
            print("Insert failed! Invalid county entered", e)


def prompt_city_data():
    '''
    This sub-routine simply creates prompts for user input for data to create the new city
    with. It also stips white space and capatalise to ensure consistency and data integrity.
    When all the data is collected, its added to a sigle list variable and returned to the 
    calling function

    '''
    # Name, CountryCode, District, Population, latitude, longitude
    clear()
    print('Enter the values in at the prompts adding a new City to the city database\n')
    Name = input('City Name: ').strip().capitalize()
    CountryCode = input('Country Code: ').strip().upper()
    District = input('District/County: ').strip().capitalize()
    Population = int(input('Population: ').strip())
    citydata=[Name, CountryCode, District, Population]
    if debug==True: print(citydata)
    return citydata

def mongodb_add_data(db,collection,newdoc):
    '''
    The routine adds data to the MongDB database passed into the function in newdoc.
    The function call expects three variable to be populated.

        db          - is the name of the MongoDB database to use
        collection  - collection is the name of the collection in the database 
        newdoc      - newdoc is the datastring in the format specified below
    
    newDoc = {"_id":7, "car":{"reg":"99-D-69674", "enginesize":1.0}}

    The function call will return a success or failure to inser the data

    '''
    # connect if not already connected, otherwise skip and use current connection
    global mongoclient
    mongoclient=mongo_connect(mongoclient)

    db = mongoclient[db] #db = mongoclient["proj"]
    docs = db[collection]#docs = db["docs"]
    #newDoc = {"_id":7, "car":{"reg":"99-D-69674", "enginesize":1.0}}

    try:
        docs.insert_one(newdoc)
    except pymongo.errors.DuplicateKeyError:
        print('A duplicate key was entered, please try again.')
    except Exception as e:
        print(e)
    else:
        print('Successfully added the new car')
    

def add_new_car_get_data():
    '''
    This function creates the user prompts, collects and formats the data and assemble
    the results into a list and returns it to the calling function for adding a new car 
    to the database. 

    The function prompts the user for three values, a new id, the car reg and the enginesize.

    '''
    print('\nPlease enter details for new car to add\n')
    _id=input('_id: ').strip()
    carreg=input('car reg(eg:99-D-123): ').strip().upper()
    if carreg.find('-') < 0: #ife there is no dashes in the reg
        carreg = re.sub(r'([A-Za-z]+)',r'-\1-',carreg.upper())# add dashes to the reg
    enginesize=float(input('engine size(eg: 1.6): ').strip())
    #print('{} {} {}'.format(_id,carreg,enginesize))
    cardetails=[_id, carreg, enginesize]
    return cardetails


def flatten_dict(d, parent_key='', sep='_'):
    '''
    This function performs an intermediate step on the mongoDB data query result
    by flattening the json file structure returned by the mongoDB query to facilitare
    the printing of the query results in a user friendly tabular format.

    '''
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def mongo_to_list(mongo_cursor):
    '''
    iterate over the raw mongo cursor return and flatten the dictionary like format 
    to a python list to facilitate user friendly tabular style prints

    '''
    to_list=[]
    for item in mongo_cursor:
        to_list.append(flatten_dict(item))
    return to_list

def mongo_connect(mongoclient):
    '''
    Conneect to the mongoclient of not already connected and return the connection reference.

    '''
    if (not mongoclient):
        try:
            mongoclient = pymongo.MongoClient()
            mongoclient.admin.command('ismaster')
            if debug==True: print('client_connect: ',mongoclient)
        except Exception as e:
            print('Error', e)
    return mongoclient

def mongo_find(mongoclient,db,collection,query):
    '''
    find data in the mongodb using the parameters passed into the function and return
    the query data from the function call.

    Parameters passed in:
        mongoclient  - client info passed on from the db connect function call
        db           - the database to connect to
        collection   - the collection to query
        query        - mongoDB style query eg: {'car':{'$exists':'true'}}

    '''
    db = mongoclient[db]
    docs = db[collection]
    query = query
    query_result = docs.find(query)
    if debug == True:
        prdata=query_result.copy()
        for line in prdata:
            print(line)
    return query_result

def add_where_clause():
    '''
    This function takes user input and creates a where clause for a mysql query 
    from the input prompts and returns the where clause to the calling function
    
    '''
    signs=['<','>','=']
    Valid=False
    while Valid == False:
        sign = input("Enter < > or = : ").strip()
        if sign in signs:
            Valid = True
    value = input("Enter population : ").strip()
    whereclause = 'where c.Population {} {}'.format(sign,value)
    return whereclause

def wait_here():
    '''
    This function creates a wait step anywhere in the application where required and 
    display a messages that it is waiting untill the space bar is pressed.
    
    '''
    print("Press space to continue ...")
    keyboard.wait('space')

def clear():
    '''
    This clears the terminal output for linux or windows systems
    
    '''
    os.system( "cls" if os.name == "nt" else "clear")


def mysql_query(query):
    '''
    This function connects to the locally running mysql server assuming host and 
    user credentials and execute the MySQL query passed into the function and return 
    the query results in a python list structure to the calling function
    
    '''
    conn = pymysql.connect( "localhost", "root", "root", "world", 
                    cursorclass=pymysql.cursors.DictCursor)
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    conn.close()
    return results

def print_nice(QueryData):
    '''
    This function takes the data returned from a mysql query and generates an ascii 
    table from the data and output the result to the console window

    The input to the function call is the raw data returned from the sql query function
    mysql_query().

    '''
    #print(QueryData)
    if len(QueryData) == 0:
        print('No data returned!')
    else:
        heading=[]
        data=[]
        for txt in QueryData[0]:
            heading.append(txt)
        data.append(heading)
        for line in QueryData:
            vals=[]
            for idx,val in line.items():
                vals.append(val)
            data.append(vals)
        table=AsciiTable(data)
        print(table.table)

if __name__ == "__main__":
    '''
    The main function where everyting starts from end ends
    
    '''
    # execute only if run as a script
    #debug = True
    main()

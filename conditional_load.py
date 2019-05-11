import pymysql
import pandas as pd

mysql_data_loaded = False
df=None

def mysql_load_data():
  global mysql_data_loaded
  if mysql_data_loaded == False:
    print('Loading the data')
    # load the data here
    country_data = load_country_data()
    country_data_to_df()
    mysql_data_loaded = True # set to true to indicate it's loaded
  else:
    print('data is already loaded, skip loading again')
    
  # now the data is loaded so do whatever is required liek display 
  print('do something with the data')
  print(df)


def load_country_data():
  #load and store country data in memory for functions 6 and 7 calls
  try:
      country_data=mysql_query("select * from country")
  except Exception as e:
      print(e)
  else:
      return country_data

def mysql_query(query):
    conn = pymysql.connect( "localhost", "root", "root", "world", 
                    cursorclass=pymysql.cursors.DictCursor)
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    conn.close()
    return results

def country_data_to_df():
    global df
    print('\rLoading country data to memory...', end='')
    countries=load_country_data()
    df=pd.DataFrame(countries)
    print('\rCountry data loaded to memory    ')


if __name__ == "__main__":
  mysql_load_data()
  # show the dataframe columns
  print(df.columns)
  print(df[df.Population<1000])
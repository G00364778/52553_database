import pymysql

conn = pymysql.connect( "localhost", "root", "root", "world", 
                 cursorclass=pymysql.cursors.DictCursor)

query = "select * from country;"

with conn:
    cursor = conn.cursor()
    cursor.execute(query)
    subjects = cursor.fetchall()
    for s in subjects:
        print(s)

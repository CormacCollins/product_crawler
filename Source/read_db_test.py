import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect('..\Data\product_data_db.db')

cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
rows = list()

for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"):
    rows.append(row[0])

for r in rows:
    
    print(" ----------- {} ----------- \n".format(r))
    for row in cur.execute("SELECT * from {} LIMIT 10;".format(r)):
        print(row) 

# Be sure to close the connection

con.close()
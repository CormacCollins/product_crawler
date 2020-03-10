import pandas as pd
import sqlite3
from pathlib import Path
# Temporary - Get files from CSV to put into SQL Lite Database - Should do it straight from the dataframes eventually

# Delete the current data out of the existing database - then put it back in with the code below "-----ADD------"
# This is to prevent duplicates from testing "Seeding"

#----DELETE-------

def deleteData():
    try:
        sqliteConnection = sqlite3.connect('..\Data\Abbott\TestDB.db')
        cursor = sqliteConnection.cursor()

        sql_delete_query = """DELETE from Abbot_product_flavours"""
        cursor.execute(sql_delete_query)
        sql_delete_query = """DELETE from Abbot_products"""
        cursor.execute(sql_delete_query)
        sql_delete_query = """DELETE from Abbot_main_ingredients"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Records deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")

deleteData()



#------ADD--------

Abbot_product_flavours = pd.read_csv(r"..\Data\Abott_products_flavours.csv")
Abbot_product_flavours = Abbot_product_flavours[["name", "Flavours"]] 
Abbot_products = pd.read_csv(r"..\Data\Abbot_products.csv")
Abbot_products = Abbot_products[['name',
                'price',
                'availability',
                'item_type',
                'description',
                'product_format',
                'number_in_case',
                'product_weight_numeric',
               'product_weight_metric',
                                'Form']]
Abbot_main_ingredients = pd.read_csv(r"..\Data\Abott_products_ingredients.csv")
Abbot_main_ingredients = Abbot_main_ingredients[["name", "ingredient"]]

conn = sqlite3.connect('..\Data\TestDB.db')

c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Abbot_product_flavours ({})".format(' ,'.join(Abbot_product_flavours.columns)))

for row in Abbot_product_flavours.iterrows():
    sql = "INSERT INTO Abbot_product_flavours ({}) VALUES ({})".format(' ,'.join(Abbot_product_flavours.columns), ','.join(['?']*len(Abbot_product_flavours.columns)))
    c.execute(sql, tuple(row[1]))
conn.commit()

c.execute("CREATE TABLE IF NOT EXISTS Abbot_products ({})".format(' ,'.join(Abbot_products.columns)))

for row in Abbot_products.iterrows():
    sql = "INSERT INTO Abbot_products ({}) VALUES ({})".format(' ,'.join(Abbot_products.columns), ','.join(['?']*len(Abbot_products.columns)))
    c.execute(sql, tuple(row[1]))
conn.commit()

c.execute("CREATE TABLE IF NOT EXISTS Abbot_main_ingredients ({})".format(' ,'.join(Abbot_main_ingredients.columns)))

for row in Abbot_main_ingredients.iterrows():
    sql = "INSERT INTO Abbot_main_ingredients ({}) VALUES ({})".format(' ,'.join(Abbot_main_ingredients.columns), ','.join(['?']*len(Abbot_main_ingredients.columns)))
    c.execute(sql, tuple(row[1]))
conn.commit()
print("Records Added to SQLLite Database")


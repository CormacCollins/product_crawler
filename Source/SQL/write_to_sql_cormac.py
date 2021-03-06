import pandas as pd
import sqlite3
from pathlib import Path
import xml_reader as xml_read
import sqlite_helper as sqlite_helper

'''
Class that will take any csv file (final products file after cleaning) 
from any stores scraping, any write it'a contents to the sqllite tables.
These files will need to have columns and data correspondeing to the 
pre-established schema stored in Data/table_columns_list.xml
This can be easily read from using the xml_reader.py helper class
'''



DATABASE_PATH = '..\..\Data\product_data_db.db'


def get_table_names_with_attributes_dict():
    '''
    Uses our xml helper to read our data schema that's stored in
    our xml file, therefore any changes to that xml file should
    carry into our db automatically
    '''

    r = xml_read.reader('../../Data/table_columns_list.xml')
    table_names = r.table_names

    tables_contents = {}
    for nm in table_names:
        contents = r.get_text_contents_children(nm)
        tables_contents[nm] = contents
    return tables_contents
    
    
def delete_tables(path):
    '''
    Remove all tables in database
    '''

    # Get all current tbales in db
    con = sqlite3.connect(path)
    cursor = con.cursor()
    table_names = sqlite_helper.get_all_table_names(cursor)

    try:
        for nm in table_names:
            sql_delete_query = """DROP TABLE """ + str(nm)
            cursor.execute(sql_delete_query)
            
        con.commit()
        print("Records deleted successfully ")

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)

    cursor.close()
    con.close()


# ----------------------------------------------------------
# ------------------- Write each table ---------------------
# ----------------------------------------------------------

#delete all current tables
delete_tables(DATABASE_PATH)

# use xml reader to get the attritbutes for each of our
# tables from our data schema xml
table_info = get_table_names_with_attributes_dict()

#eventually when all tables are good from the workbook end - won't need this approved list, just get them all
approved_tables = {
    #eventually have all naming the same
                #ABBOTT
                'products_table':r"..\..\Data\Abbott\Abbot_products.csv", 
                'flavour_table':r"..\..\Data\Abbott\flavours.csv",
                'ingredient_table':r"..\..\Data\Abbott\ingredients.csv",
                'vitamins_table':r"..\..\Data\Abbott\Abbot_vitamins_full.csv",
                'minerals_table':r"..\..\Data\Abbott\Abbot_mineral_full.csv",
                'nutrition_table':r"..\..\Data\Abbott\Abbot_nutrients_full.csv",
                # NCARE
                'products_table':r"..\..\Data\Ncare\products_table.csv", 
                'flavour_table':r"..\..\Data\Ncare\flavour_table.csv",
                'ingredient_table':r"..\..\Data\Ncare\ingredient_table.csv",
                'nutrition_table':r"..\..\Data\Ncare\nutrition_table.csv",
                'clinical_indications_table':r"..\..\Data\Ncare\clinical_indications_table.csv" 
                 }

for tbl, csv_path in approved_tables.items():
    columns = table_info[tbl]
    #Abbot_product_flavours = pd.read_csv(r"..\Data\Abbott\Abbot_products.csv")
    #Abbot_product_flavours = Abbot_product_flavours[["item_type", "Flavours"]] 
    data = pd.read_csv(r'' + csv_path)

    #get the exact columns as per table column list data schema
    print(tbl)
    print(columns)
    data = data[columns]

    #Abbot_main_ingredients = pd.read_csv(r"..\Data\Abbott\Abott_products_ingredients.csv")
    #Abbot_main_ingredients = Abbot_main_ingredients[["item_type", "ingredient"]]

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS {} ({})".format(tbl, ' ,'.join(data.columns))
    #print(query)
    c.execute(query)

    for row in data.iterrows():
        sql = "INSERT INTO {} ({}) VALUES ({})".format(tbl, ' ,'.join(data.columns), ','.join(['?']*len(data.columns)))
        c.execute(sql, tuple(row[1]))
    conn.commit()
    conn.close()

'''


c.execute("CREATE TABLE IF NOT EXISTS Abbot_product_flavours ({})".format(' ,'.join(Abbot_product_flavours.columns)))

for row in Abbot_product_flavours.iterrows():
    sql = "INSERT INTO Abbot_product_flavours ({}) VALUES ({})".format(' ,'.join(Abbot_product_flavours.columns), ','.join(['?']*len(Abbot_product_flavours.columns)))
    c.execute(sql, tuple(row[1]))
conn.commit()



c.execute("CREATE TABLE IF NOT EXISTS Abbot_main_ingredients ({})".format(' ,'.join(Abbot_main_ingredients.columns)))

for row in Abbot_main_ingredients.iterrows():
    sql = "INSERT INTO Abbot_main_ingredients ({}) VALUES ({})".format(' ,'.join(Abbot_main_ingredients.columns), ','.join(['?']*len(Abbot_main_ingredients.columns)))
    c.execute(sql, tuple(row[1]))
conn.commit()

print("Records Added to SQLLite Database")

'''
import pandas as pd
import numpy as np

# Extract more features and create an individual table

Abbot_products = pd.read_csv("../Data/data2.csv") #This could be replaced with output from other parser

Abbot_products = Abbot_products[pd.notnull(Abbot_products['ID'])]
Abbot_products[['size_or_weight','number_in_case']] = (Abbot_products['size_or_weight'].str.split('/', expand=True))
Abbot_products['product_weight_numeric'] = Abbot_products.size_or_weight.str.extract(r'([^ ]*)')
Abbot_products['product_format'] = Abbot_products.size_or_weight.str.split().str[-1]
Abbot_products['product_weight_metric'] = Abbot_products.size_or_weight.str.split().str[-2]
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

Abbot_products.drop_duplicates(keep='first', inplace=True)

# Can't make name index
# we lose the product variants (i.e. can, case of variant numbers, container - because they are all tied to the name key)
#Ryan - Fair enough, was just taking out the ugly default index number

#Abbot_products.set_index(['name'], inplace=True)
Abbot_products.to_csv("../Data/Abbot_products.csv")

# -----------

# Set up table which shows all the ingredients for products vertically for analytics

Abbot_products_ingredients_name = pd.read_csv("../Data/data2.csv") #This could be replaced with output from other parser

Abbot_products_ingredients_name = Abbot_products_ingredients_name[pd.notnull(Abbot_products_ingredients_name['ID'])]
Abbot_products_ingredients = Abbot_products_ingredients_name[['ID','ingredients']]
Abbot_products_name = Abbot_products_ingredients_name[['ID', 'name']]
Abbot_main_ingredients = pd.concat([Abbot_products_name,
                                    Abbot_products_ingredients['ingredients'].str.split(', ', expand=True)], axis=1)

Abbot_main_ingredients = pd.melt(Abbot_main_ingredients, id_vars = ["name"])
Abbot_main_ingredients.dropna(inplace=True)
Abbot_main_ingredients = Abbot_main_ingredients[(Abbot_main_ingredients['value'] != 0)]
Abbot_main_ingredients.rename(columns={'value' : 'ingredient'},inplace=True)
Abbot_main_ingredients.head()
Abbot_main_ingredients = Abbot_main_ingredients[['name', 'ingredient']]
Abbot_main_ingredients.sort_values('name', inplace=True, ascending=True)
# We can make name the index here if wanted because the ingredients are the same for each varient
Abbot_main_ingredients.set_index(['name'], inplace=True)
Abbot_main_ingredients.drop_duplicates(keep='first', inplace=True)
Abbot_main_ingredients.to_csv("../Data/Abott_products_ingredients.csv")

# -----------

# Set up table which shows all the flavours for products vertically for analytics

Abbot_product_flavours_name = pd.read_csv("../Data/data2.csv") #This could be replaced with output from other parser
Abbot_product_flavours_name = Abbot_product_flavours_name[pd.notnull(Abbot_product_flavours_name['ID'])]
Abbot_products_name = Abbot_product_flavours_name[['ID', 'name']]
Abbot_product_flavours = Abbot_product_flavours_name[['ID','Flavours']]
Abbot_product_flavours = pd.concat([Abbot_products_name,
                                    Abbot_product_flavours['Flavours'].str.split(', ', expand=True)], axis=1)

Abbot_product_flavours = pd.melt(Abbot_product_flavours, id_vars = ["name"])
Abbot_product_flavours.dropna(inplace=True)
Abbot_product_flavours = Abbot_product_flavours[(Abbot_product_flavours['value'] != 0)]
Abbot_product_flavours.rename(columns={'value' : 'Flavours'},inplace=True)
Abbot_product_flavours.head()
Abbot_product_flavours = Abbot_product_flavours[['name', 'Flavours']]
Abbot_product_flavours.sort_values('name', inplace=True, ascending=True)
Abbot_product_flavours.drop_duplicates(keep='first', inplace=True)
# We may need to add more conditions below this:
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("'", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("[", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("]", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace(" Chocolate", "Rich Chocolate", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("Rich", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("&", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("-", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("Peanut", "Peanut Butter", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("Butter", "", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("Homemade", "Homemade Vanilla", regex=False)
Abbot_product_flavours['Flavours'] = Abbot_product_flavours['Flavours'].str.replace("Vanilla", "", regex=False)
Abbot_product_flavours = Abbot_product_flavours[(Abbot_product_flavours['Flavours'] != '')]
Abbot_product_flavours.to_csv("../Data/Abott_products_flavours.csv")
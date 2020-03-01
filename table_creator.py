import pandas as pd
import numpy as np

# Extract more features and create an individual table

Abbot_products = pd.read_csv("data.csv") #This could be replaced with output from other parser

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
               'product_weight_metric']]

Abbot_products.set_index(['name'], inplace=True)
Abbot_products.to_csv("Abbot_products.csv")

# -----------

# Set up table which shows all the ingredients for products vertically for analytics

Abbot_products_ingredients_name = pd.read_csv("data.csv") #This could be replaced with output from other parser

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
Abbot_main_ingredients.set_index(['name'], inplace=True)
Abbot_main_ingredients.drop_duplicates(keep='first', inplace=True)
Abbot_main_ingredients.to_csv("Abott_products_ingredients.csv")


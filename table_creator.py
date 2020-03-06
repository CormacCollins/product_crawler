import pandas as pd
import numpy as np

# Extract more features and create an individual table

Abbot_products = pd.read_csv("data.csv") #This could be replaced with output from other parser

#TODO/PRODUCT INFO RETHINK: 
# The more info columns that are being turned into number_in_case, product_weight_numeric etc. are not just these, they can be variable, such as categories like {'Ready-to-feed', 'Concentrated liquid', 'Powder', 'Shake', 'Snack bar'} or flavour categories (Flavor categories can be scrapped seperately from another spot on the url)
# this is because these values come from dot points at the end of the product, there are varying numbers of these dot points, so these added info columns don't line up for each product. e.g. It may say Case of 48 in 'more_info_1' in 1 product, and in the next say case of 48 in 'more_info_2'.
# I (cormac) can change the scrapper to get these info's relative to their names: falvour, sizes, form - so below will need to be changed slightly after, less 

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

Abbot_products.drop_duplicates(keep='first', inplace=True)

# Can't make name index
# we lose the product variants (i.e. can, case of variant numbers, container - because they are all tied to the name key)

#Abbot_products.set_index(['name'], inplace=True)
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
# We can make name the index here if wanted because the ingredients are the same for each varient
Abbot_main_ingredients.set_index(['name'], inplace=True)
Abbot_main_ingredients.drop_duplicates(keep='first', inplace=True)
Abbot_main_ingredients.to_csv("Abott_products_ingredients.csv")


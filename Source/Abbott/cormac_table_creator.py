import pandas as pd
import numpy as np
from Abbott_lookup import ab_lookup 

# Create a Lookup Table to manually replace missing values in Abbot Product Table
# This can be mannually updated with research projects
construct = ab_lookup  #Just to get this out of the analysis page
# Create a dataframe from constructed table above
lookup = pd.DataFrame(data=construct)
# Create an array from lookup table to help filter later on
lookup_filter = lookup["item_type"].array
lookup.drop(["name"], axis=1, inplace=True)
lookup = lookup.set_index("item_type")

# ---------------------------- End of Lookup Table work ---------------------------------

# Create the Abbott product table
Abbot_products_original = pd.read_csv("../Data/Abbott/Abbott_scrape_data.csv", error_bad_lines=False) #This could be replaced with output from other parser
Abbot_products = Abbot_products_original #to be used by future analysis

# --------------------------------
#I'm unsure of this for now
Abbot_products = pd.concat([Abbot_products, lookup], sort=True)
# --------------------------------



# ------------- Setup dataframe and columns -----------------
Abbot_products.drop(['Unnamed: 0'], axis=1, inplace=True)
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
                                'Form',
                        'Cans Type X',
                        'Cans Type Y',
                        'entry_date', 
                                 'url'
]]

Abbot_products.drop_duplicates(keep='first', inplace=True)
Abbot_products[pd.isnull(Abbot_products['product_format'])]

# Turn series into string so it can be used in joins below
Abbot_products['item_type'] = Abbot_products['item_type'].astype(str)
# Take out the SKUs with missing values
get_subset = Abbot_products[Abbot_products['item_type'].isin(lookup_filter)]
# Delete the columns, because they will be replaced with the lookup table above
get_subset = get_subset.drop(["product_format", "number_in_case", "product_weight_numeric", "product_weight_metric"],
                            axis=1)

get_subset = get_subset.join(lookup, on="item_type")
# The ~ means it is NOT in - we are removing the SKUs with missing values first
Abbot_products = Abbot_products[~Abbot_products['item_type'].isin(lookup_filter)]

# Now re-adding it back in with a concat - join
Abbot_products = pd.concat([Abbot_products, get_subset], sort=True)

# Clean any white space
Abbot_products.name = Abbot_products.name.str.strip()
Abbot_products.item_type = Abbot_products.item_type.str.strip()
Abbot_products.description = Abbot_products.description.str.strip()
Abbot_products.product_format = Abbot_products.product_format.str.strip()
Abbot_products.number_in_case = Abbot_products.number_in_case.str.strip()
Abbot_products.Form = Abbot_products.Form.str.strip()

# Send to CSV
Abbot_products.to_csv("../Data/Abbott/Abbot_products.csv")

# -------------------------------------------

# Set up table which shows all the ingredients for products vertically for analytics
Abbot_products_ingredients_item_type = Abbot_products_original

# Changed from Name to SKU ID "item_type"
Abbot_products_ingredients_item_type = Abbot_products_ingredients_item_type[pd.notnull(Abbot_products_ingredients_item_type['item_type'])]
Abbot_products_ingredients = Abbot_products_ingredients_item_type[['item_type','ingredients']]
Abbot_products_name = Abbot_products_ingredients_item_type['item_type']
Abbot_main_ingredients = pd.concat([Abbot_products_name,
                                    Abbot_products_ingredients['ingredients'].str.split(', ', expand=True)], axis=1)
Abbot_main_ingredients = pd.melt(Abbot_main_ingredients, id_vars = ["item_type"])
Abbot_main_ingredients.dropna(inplace=True)
Abbot_main_ingredients = Abbot_main_ingredients[(Abbot_main_ingredients['value'] != 0)]

Abbot_main_ingredients.rename(columns={'value' : 'ingredient'},inplace=True)
del Abbot_main_ingredients['variable']
Abbot_main_ingredients.head()
Abbot_main_ingredients.sort_values('item_type', inplace=True, ascending=True)
Abbot_main_ingredients.drop_duplicates(keep='first', inplace=True)
Abbot_main_ingredients


# Remove white space and "AND" 
Abbot_main_ingredients.ingredient = Abbot_main_ingredients.ingredient.str.strip()
Abbot_main_ingredients['ingredient'] = Abbot_main_ingredients['ingredient'].str.replace("and ", "", regex=False)
Abbot_main_ingredients['ingredient'] = Abbot_main_ingredients['ingredient'].str.replace(".", "", regex=False)

# Send to CSV
Abbot_main_ingredients.to_csv("../Data/Abbott/Abott_products_ingredients.csv")

# -----------

# Set up table which shows all the flavours for products vertically for analytics
# Changed name to SKU "item_type"

Abbot_product_flavours_item_type = Abbot_products_original
 #This could be replaced with output from other parser
    
Abbot_product_flavours_item_type = Abbot_product_flavours_item_type[pd.notnull(Abbot_product_flavours_item_type['item_type'])]
Abbot_products_name = Abbot_product_flavours_item_type['item_type']
Abbot_product_flavours = Abbot_product_flavours_item_type[['item_type','Flavours']]
Abbot_product_flavours = pd.concat([Abbot_products_name,
                                    Abbot_product_flavours['Flavours'].str.split(', ', expand=True)], axis=1)


Abbot_product_flavours = pd.melt(Abbot_product_flavours, id_vars = ["item_type"])
Abbot_product_flavours['value'] = Abbot_product_flavours['value'].astype(str)

Abbot_product_flavours['value'] = Abbot_product_flavours['value'].str.replace("]", "", regex=False)
Abbot_product_flavours['value'] = Abbot_product_flavours['value'].str.replace("[", "", regex = False)
Abbot_product_flavours['value'] = Abbot_product_flavours['value'].str.replace("'", "", regex=False)
Abbot_product_flavours.dropna(inplace=True)
Abbot_product_flavours = Abbot_product_flavours[(Abbot_product_flavours['value'] != 0)]
del Abbot_product_flavours['variable']
Abbot_product_flavours.rename(columns={'value' : 'Flavours'},inplace=True)

Abbot_product_flavours.sort_values('item_type', inplace=True, ascending=True)
Abbot_product_flavours.drop_duplicates(keep='first', inplace=True)
Abbot_product_flavours

Abbot_product_flavours.to_csv("../Data/Abbott/Abott_products_flavours.csv")

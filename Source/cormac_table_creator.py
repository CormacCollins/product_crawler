import pandas as pd
import numpy as np

# Create a Lookup Table to manually replace missing values in Abbot Product Table
# This can be mannually updated with research projects

construct = {'name': ["Carrying Case for FreeStyle InsuLinx System",
                   "Carrying Case for FreeStyle Precision Neo System",
                   "Data Cable and Charging Adapter for FreeStyle Libre 14 Day System",
                   "Data Cable For FreeStyle Precision Neo and FreeStyle Libre 14 day Systems",
                   "Ensure Enlive",
                   "Ensure Rapid Hydration Electrolyte Powder Packs",
                   "FreeStyle Carrying Case",
                   "FreeStyle Control Solution",
                   "FreeStyle Data Cable",
                   "FreeStyle Lancets",
                   "FreeStyle Lancing Device II",
                   "FreeStyle Log Books / 100 pack",
                   "FreeStyle Precision Neo Blood Glucose Monitoring System",
                   "Glucerna Mini Treats", 	"Glucerna Snack Bars",
                   "Meter Replacement Batteries",
                   "Pedialyte",
                   "Pedialyte",
                   "Pedialyte",
                   "Pedialyte",
                   "Pedialyte",
                   "Pedialyte AdvancedCare",
                   "Pedialyte AdvancedCare",
                   "Pedialyte AdvancedCare",
                   "Pedialyte AdvancedCare Plus",
                   "Pedialyte AdvancedCare Plus",
                   "Pedialyte AdvancedCare Plus Hydration Station Multipack",
                   "Pedialyte AdvancedCare Plus Powder Packs",
                   "Pedialyte AdvancedCare Plus Powder Packs",
                   "Pedialyte Hydration Station Multipack",
                   "Pedialyte Powder Packs",
                   "Pedialyte Powder Packs",
                   "Pedialyte Powder Packs",
                   "Pedialyte Powder Packs",
                   "Pedialyte Sparkling Rush Powder Packs",
                   "Pedialyte Sparkling Rush Powder Packs",
                   "Similac Breast Milk Storage Bottle Caps",
                   "Similac Human Milk Fortifier Powder",
                   "Similac Human Milk Fortifier Powder",
                   "Similac Volu-Feed Nurser",
                   "ZonePerfect Macros Bar",
                   "ZonePerfect Macros Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "ZonePerfect Nutrition Bar",
                   "Similac Slow Flow Nipple and Ring",
                   "Similac Infant Nipple and Ring",
                   "Similac Premature Nipple and Ring",
                   "Similac Orthodontic Nipple and Ring",
                   "Cooler Insert with 2 Freezable Ice Packs",
                   "FreeStyle Precision Neo Starter Pack",
                   "FreeStyle Precision Neo Blood Glucose Test Strips / 50 count",
                   "FreeStyle Precision Neo Blood Glucose Test Strips / 25 count",
                   "FreeStyle Log Books / 6 pack"],
          'item_type': ["SKU#:21372",
                        "SKU#:25189",
                        "SKU#:7161301",
                        "SKU#:213732",
                        "SKU#:64293",
                        "SKU#:67475",
                        "SKU#:7037301",
                        "SKU#:1400204",
                        "SKU#:7085102",
                        "SKU#:1300170",
                        "SKU#:7158201",
                        "SKU#:22309p100",
                        "SKU#:7517583",
                        "SKU#:66906",
                        "SKU#:66884",
                        "SKU#:7037401p5",
                        "SKU#:00365",
                        "SKU#:67461",
                        "SKU#:59892",
                        "SKU#:59892p4",
                        "SKU#:51752e",
                        "SKU#:64301",
                        "SKU#:63059",
                        "SKU#:64307e",
                        "SKU#:67434",
                        "SKU#:66645e",
                        "SKU#:67287p80",
                        "SKU#:67426p6",
                        "SKU#:67426",
                        "SKU#:67285p80",
                        "SKU#:64598",
                        "SKU#:56090",
                        "SKU#:56090p8",
                        "SKU#:64172p6",
                        "SKU#:67220p6",
                        "SKU#:67225",
                        "SKU#:54080",
                        "SKU#:54598p50",
                        "SKU#:54598",
                        "SKU#:00180",
                        "SKU#:67500",
                        "SKU#:67500p12",
                        "SKU#:63225p12",
                        "SKU#:63282p12",
                        "SKU#:63305",
                        "SKU#:63269",
                        "SKU#:66040p12",
                        "SKU#:63304",
                        "SKU#:63505",
                        "SKU#:66040",
                        "SKU#:53894p50",
                        "SKU#:00079p50",
                        "SKU#:00094",
                        "SKU#:53560",
                        "SKU#:53568",
                        "SKU#:FSMTS50",
                        "SKU#:7157975",
                        "SKU#:7157775",
                        "SKU#:22309p6"],
          "product_format": ["carrying case",
                             "carrying case",
                             "device",
                             "device",
                             "bottle",
                             "packets",
                             "carrying case",
                             "solution",
                             "device",
                             "lancet",
                             "device",
                             "log book",
                             "device",
                             "packets",
                             "bars",
                             "device",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "bottle",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "packets",
                             "bottle",
                             "packets",
                             "packets",
                             "bottle",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "bars",
                             "device",
                             "device",
                             "device",
                             "device",
                             "ice pack",
                             "device",
                             "strips",
                             "strips",
                             "log book"],
          "number_in_case": [1,
                             1,
                             1,
                             1,
                             16,
                             6,
                             1,
                             2,
                             1,
                             100,
                             1,
                             100,
                             1,
                             24,
                             20,
                             5,
                             8,
                             4,
                             48,
                             4,
                             1,
                             4,
                             8,
                             1,
                             4,
                             1,
                             80,
                             6,
                             6,
                             80,
                             6,
                             8,
                             8,
                             6,
                             6,
                             6,
                             250,
                             50,
                             150,
                             100,
                             36,
                             12,
                             12,
                             12,
                             30,
                             30,
                             12,
                             36,
                             36,
                             36,
                             np.nan,
                             np.nan,
                             np.nan,
                             np.nan,
                             2,
                             np.nan,
                             50,
                             25,
                             6],
          "product_weight_numeric": [np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     8,
                                     0.6,
                                     np.nan,
                                     4,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     0.7,
                                     1.4,
                                     np.nan,
                                     1,
                                     1,
                                     2,
                                     2,
                                     np.nan,
                                     1,
                                     1,
                                     np.nan,
                                     1,
                                     np.nan,
                                     0.6,
                                     0.6,
                                     0.6,
                                     0.6,
                                     0.6,
                                     0.3,
                                     0.3,
                                     0.6,
                                     0.6,
                                     0.6,
                                     np.nan,
                                     0.9,
                                     0.9,
                                     np.nan,
                                     1.76,
                                     1.76,
                                     1.58,
                                     1.76,
                                     1.58,
                                     1.76,
                                     1.41,
                                     1.76,
                                     1.58,
                                     1.41,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan,
                                     np.nan],
          "product_weight_metric": ["",
                                    "",
                                    "",
                                    "",
                                    "oz",
                                    "oz",
                                    "",
                                    "ml",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "oz",
                                    "oz",
                                    "",
                                    "L",
                                    "L",
                                    "oz",
                                    "oz",
                                    "",
                                    "L",
                                    "L",
                                    "",
                                    "L",
                                    "",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "",
                                    "g",
                                    "g",
                                    "",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "oz",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    ""]}

# Create a dataframe from constructed table above
lookup = pd.DataFrame(data=construct)
# Create an array from lookup table to help filter later on
lookup_filter = lookup["item_type"].array
lookup.drop(["name"], axis=1, inplace=True)
lookup = lookup.set_index("item_type")


# In[177]:



# ---------------------------- End of Lookup Table work ---------------------------------

# Create the Abbott product table

Abbot_products_original = pd.read_csv("../Data/Abbott/Abbott_scrape_data.csv", error_bad_lines=False) #This could be replaced with output from other parser
Abbot_products = Abbot_products_original



# --------------------------------
#I'm unsure of this for now
#Abbot_products = pd.concat([Abbot_products, lookup], sort=True)
# --------------------------------

#Abbot_products.set_index('item_type', inplace=True)
Abbot_products.drop(['Unnamed: 0'], axis=1, inplace=True)
Abbot_products[:3]
#print(list(Abbot_products.index.values))
#print(Abbot_products.columns)


# In[ ]:





# In[178]:



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
Abbot_products[:5]


# In[179]:


Abbot_products[pd.isnull(Abbot_products['product_format'])]
Abbot_products.iloc[236].url


# In[180]:


# Turn series into string so it can be used in joins below
Abbot_products['item_type'] = Abbot_products['item_type'].astype(str)

# Take out the SKUs with missing values
get_subset = Abbot_products[Abbot_products['item_type'].isin(lookup_filter)]

get_subset


# Delete the columns, because they will be replaced with the lookup table above
get_subset = get_subset.drop(["product_format", "number_in_case", "product_weight_numeric", "product_weight_metric"],
                            axis=1)


get_subset = get_subset.join(lookup, on="item_type")

# The ~ means it is NOT in - we are removing the SKUs with missing values first
Abbot_products = Abbot_products[~Abbot_products['item_type'].isin(lookup_filter)]

# Now re-adding it back in with a concat - join
Abbot_products = pd.concat([Abbot_products, get_subset])

# Clean any white space
Abbot_products.name = Abbot_products.name.str.strip()
Abbot_products.item_type = Abbot_products.item_type.str.strip()
Abbot_products.description = Abbot_products.description.str.strip()
Abbot_products.product_format = Abbot_products.product_format.str.strip()
Abbot_products.number_in_case = Abbot_products.number_in_case.str.strip()
Abbot_products.Form = Abbot_products.Form.str.strip()

# Send to CSV
Abbot_products.to_csv("../Data/Abbott/Abbot_products.csv")

# -----------


# In[204]:




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


# In[206]:




# -----------

# Set up table which shows all the flavours for products vertically for analytics
# Changed name to SKU "item_type"

Abbot_product_flavours_item_type = Abbot_products_original
 #This could be replaced with output from other parser
Abbot_product_flavours_item_type = Abbot_product_flavours_item_type[pd.notnull(Abbot_product_flavours_item_type['ID'])]
Abbot_products_name = Abbot_product_flavours_item_type[['ID', 'item_type']]
Abbot_product_flavours = Abbot_product_flavours_item_type[['ID','Flavours']]
Abbot_product_flavours = pd.concat([Abbot_products_name,
                                    Abbot_product_flavours['Flavours'].str.split(', ', expand=True)], axis=1)

Abbot_product_flavours = pd.melt(Abbot_product_flavours, id_vars = ["item_type"])
Abbot_product_flavours.dropna(inplace=True)
Abbot_product_flavours = Abbot_product_flavours[(Abbot_product_flavours['value'] != 0)]
Abbot_product_flavours.rename(columns={'value' : 'Flavours'},inplace=True)
Abbot_product_flavours.head()
Abbot_product_flavours = Abbot_product_flavours[['item_type', 'Flavours']]
Abbot_product_flavours.sort_values('item_type', inplace=True, ascending=True)
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

# Remove white space
Abbot_product_flavours.Flavours = Abbot_product_flavours.Flavours.str.strip() 

Abbot_product_flavours.to_csv("../Data/Abbott/Abott_products_flavours.csv")


# In[ ]:





# In[ ]:

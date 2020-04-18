
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


import warnings
warnings.simplefilter('ignore')


class Flavour_creations_crawler:
    def get_product_info(self, prod_url):
        
        PRODUCT_INFORMATION = {'url':[],
                               'category':[],
                               'sub_category':[],
                               'description':[],
                               'indications':[],
                               'ingredients':[]}
                                     
        for u in prod_url:
            
            
            PRODUCT_INFORMATION['url'].append(u)


            page = requests.get(u, verify=False)

            soup = BeautifulSoup(page.content, 'html.parser')
                                     
            
            try:
                #Get Category
                category = soup.find_all('span', class_ = 'category')
                category = category[0].text.strip()
                PRODUCT_INFORMATION['category'].append(category)
            except:
                PRODUCT_INFORMATION['category'].append("not found")
                                     
                                     
            try:
                #Get Sub-Category
                sub_category = soup.find_all('span', class_ = 'sub-category')
                sub_category = sub_category[0].text.strip()
                PRODUCT_INFORMATION['sub_category'].append(sub_category)
            except:
                PRODUCT_INFORMATION['sub_category'].append("not found")
                                     
            try:
                description = soup.find_all("div", class_ = 'columns medium-7')
                description = soup.find_all("p")
                description = description[3].text
                PRODUCT_INFORMATION['description'].append(description)
                                     
            except:
                PRODUCT_INFORMATION['description'].append("not found")
                                     
            try:
                #Get Indications
                indications = soup.find_all("div", class_ = 'columns medium-5')
                indications = soup.find_all("p")
                indications = indications[5].text
                PRODUCT_INFORMATION['indications'].append(indications)
            except:
                PRODUCT_INFORMATION['indications'].append("not found")
                                        
                                     
            try:
                #Get ingredients
                ingredients = soup.find_all("div", class_ = 'columns medium-5')
                ingredients = soup.find_all("p")
                ingredients = ingredients[10].text
                PRODUCT_INFORMATION['ingredients'].append(ingredients)
            except:
                PRODUCT_INFORMATION['ingredients'].append("not found")
                
                
        df = pd.DataFrame.from_dict(PRODUCT_INFORMATION)
        df.drop_duplicates(inplace=True)
                                     
        return df.to_csv("../Data/Flavour_Creations/flavour_creations_products.csv")



products = Flavour_creations_crawler()

links = pd.read_csv('../Data/Flavour_Creations/Flavour_Creation_Links.csv')
links_array = links["0"].values


products.get_product_info(links_array)
                                     
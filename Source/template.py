from bs4 import BeautifulSoup
import requests
import re
import string
from Source.crawler_interface import crawler_interface
import sys

class crawler_template(crawler_interface):

    def __init__(self):
        """ Implements crawler_interface
            Create instance of crawler loaded with list of links (link_list)
            Settings to be added as future change around potentially adding a small list of urls that need updating
        """
        pass
        

    
    # Gets upto 2 of the requested table - either vitamin, minerals, nutrients
    # needs to be tested as there may be unseen products with more than 2 tables
    def get_product_info(self, prod_url, store_name, path):
        
         #print(prod_url)

        PRODUCT_INFORMATION = {'url':'', 'name':'', 'price':'', 'size_or_weight':'','availability':'',	
                                'item_type':'',	'description':'', 'ingredients':'',	'allergin_info':'',	'serving_size_1':'', 
                                'serving_size_2':'', 'serving_size_3':'', 'serving_size_4':'', 'serving_size_5':'', 
                                'footnotes':'', 'nutrient_table_1': '', 'nutrient_table_2': '', 'nutrient_table_3': '', 
                                'nutrient_table_4': '', 'nutrient_table_5': '', 
                                'vitamin_table_1':'', 'vitamin_table_2':'', 'vitamin_table_3':'', 'vitamin_table_4':'', 'vitamin_table_5':'',	
                                'mineral_table_1':'', 'mineral_table_2':'', 'mineral_table_3':'', 'mineral_table_4':'', 'mineral_table_5':'', 
                                'Sizes':'', 'Form':'', 'Flavours':'', }

        PRODUCT_INFORMATION['url'] = prod_url
        
        try:
            page = requests.get(prod_url)
        except requests.exceptions.RequestException as e:
            #TODO: Better handling of error msgs
            print('failed to connect - please check url or connection')


        soup = BeautifulSoup(page.content, 'html.parser')    

        return PRODUCT_INFORMATION



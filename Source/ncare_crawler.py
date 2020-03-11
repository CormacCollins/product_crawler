from bs4 import BeautifulSoup
import requests
import re
import string
from Source.crawler_interface import crawler_interface
import sys

class Ncare_crawler(crawler_interface):

    def __init__(self):
        """ Implements crawler_interface
            Create instance of crawler loaded with list of links (link_list)
            Settings to be added as future change around potentially adding a small list of urls that need updating
        """
        pass

    #get information on 1 link
    def get_product_info(self, prod_url):

        PRODUCT_INFORMATION = {'url':'', 'name':'', 'price':'', 'size_or_weight':'','availability':'',	
                                'item_type':'',	'description':'', 'ingredients':'',	'allergin_info':'',	'serving_size_1':'', 
                                'serving_size_2':'', 'serving_size_3':'', 'serving_size_4':'', 'serving_size_5':'', 
                                'footnotes':'', 'nutrient_table_1': '', 'nutrient_table_2': '', 'nutrient_table_3': '', 
                                'nutrient_table_4': '', 'nutrient_table_5': '', 
                                'vitamin_table_1':'', 'vitamin_table_2':'', 'vitamin_table_3':'', 'vitamin_table_4':'', 'vitamin_table_5':'',	
                                'mineral_table_1':'', 'mineral_table_2':'', 'mineral_table_3':'', 'mineral_table_4':'', 'mineral_table_5':'', 
                                'Sizes':'', 'Form':'', 'Flavours':'', 'Usage':'', 'clinical indications': '', 'benefits':'' }

        PRODUCT_INFORMATION['url'] = prod_url
        
        try:
            page = requests.get(prod_url)
        except requests.exceptions.RequestException as e:
            #TODO: Better handling of error msgs
            print('failed to connect - please check url or connection')

        
        soup = BeautifulSoup(page.content, 'html.parser') 

        # get product name
        try:
            name = soup.find(class_ = 'product-name')
            PRODUCT_INFORMATION['name'] = name.text.strip('\n').lstrip()
        except:
            print("Could not add name category")

        # get product size
        try:
            size = soup.find(class_ = 'product-size')
            PRODUCT_INFORMATION['Sizes'] = size.text.strip('\n').lstrip()
        except:
            print("Could not add Sizes category")

        # get product features
        try:
            prod_feat = soup.find(class_ = 'product-features')
            PRODUCT_INFORMATION['description'] = prod_feat.text.strip('\n').lstrip()
        except:
            print("Could not add description (Features) category")

        # get product-info: Flavours, Unit of Measure, Product Code
        
        try:
            info = soup.find(class_ = 'product-info')

            values = info.find_all('td')
            col_num = len(info.find_all('tr'))

            pos_to_name_dict = {}
            for i in range(0, len(values[0:col_num])):
                pos_to_name_dict[i] = values[i].text

            flavours = list()
            units = list()
            product_codes = list()

            #print(pos_to_name_dict)
            for i in range(col_num, len(values)):

                if 'Flavour' in pos_to_name_dict[i%col_num]:
                    flavours.append(values[i].text)
                elif 'Unit' in pos_to_name_dict[i%col_num]:
                    units.append(values[i].text)
                elif 'Product' in pos_to_name_dict[i%col_num]:
                    product_codes.append(values[i].text)
            
            #keeping potential to related product code and flavours and units
            for i in range(0, len(product_codes)):
                product_codes[i] = product_codes[i] + ':' + flavours[i] + '|' + units[i]

            #these names might not look quite matching, but these are the best matching fields from the last crawl fields
            PRODUCT_INFORMATION['Flavours'] = list(set(flavours))
            PRODUCT_INFORMATION['Sizes'] = units
            PRODUCT_INFORMATION['item_type'] = product_codes
        except:
            print('Could not get product-info: Flavours, Unit of Measure, Product Code')

       # get ingredients
        try:
            ingredients = soup.find(id = 'ingridients')
            ingr = ingredients.find_all(text=True)
            PRODUCT_INFORMATION['ingredients'] = ''.join(ingr)
        except:
            print("Could not add ingredients category")

        # get usage
        try:
            usage = soup.find(id = 'usage')
            usa = ingredients.find_all(text=True)
            PRODUCT_INFORMATION['Usage'] = ''.join(usa)
        except:
            print("Could not add usage category")

        # get nutri_info
        try:
            nutri_info = soup.find(id = 'nutritional-information')
            trs = nutri_info.find('tbody').find_all('tr')
            row_list = list()
            for i in range(0, len(trs)):
                print(trs[i].text)
                

            print(row_list)
            return
            ni = ingredients.find_all('tr')
            print(ni)
            return
            PRODUCT_INFORMATION['nutrient_table_1'] = ''.join(ni)
        except:
            print("Could not add nutrient_table_1 category")



        print(PRODUCT_INFORMATION)
            
        return    
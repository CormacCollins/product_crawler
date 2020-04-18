from bs4 import BeautifulSoup
import requests
import re
import string
from Source.crawler_interface import crawler_interface
import sys
import Source.helper_functions as helper_functions

#pandas helper stuff
from IPython.display import display_html
import pandas as pd

class Ncare_crawler(crawler_interface):

    def __init__(self):
        """ Implements crawler_interface
            Create instance of crawler loaded with list of links (link_list)
            Settings to be added as future change around potentially adding a small list of urls that need updating
        """
        pass


    def write_html_table_to_csv(self, html_table, csv_name):
        """ Write a html table to csv for later analysis"""
        dfs = pd.read_html(str(html_table))
        df = dfs[0]
        df.to_csv(csv_name)


    #get information on 1 link
    def get_product_info(self, prod_url, store_name, path):


        PRODUCT_INFORMATION = {'url':'', 'name':'', 'price':'', 'size_or_weight':'','availability':'',	
                                'item_type':'',	'description':'', 'ingredients':'',	'allergin_info':'',	'serving_size_1':'', 
                                'serving_size_2':'', 'serving_size_3':'', 'serving_size_4':'', 'serving_size_5':'', 
                                'footnotes':'', 'nutrient_table_1': '', 'nutrient_table_2': '', 'nutrient_table_3': '', 
                                'nutrient_table_4': '', 'nutrient_table_5': '', 
                                'vitamin_table_1':'', 'vitamin_table_2':'', 'vitamin_table_3':'', 'vitamin_table_4':'', 'vitamin_table_5':'',	
                                'mineral_table_1':'', 'mineral_table_2':'', 'mineral_table_3':'', 'mineral_table_4':'', 'mineral_table_5':'', 
                                'Sizes':'', 'Form':'', 'Flavours':'', 'clinical indications': '', 'benefits':'' , 
                                'clinical_indications':'' ,'feature_table_rows':'', 'usage':'', 'entry_date':''}

        PRODUCT_INFORMATION['url'] = prod_url
        
        try:
            page = requests.get(prod_url)
        except requests.exceptions.RequestException as e:
            #TODO: Better handling of error msgs
            print('failed to connect - please check url or connection')

        
        soup = BeautifulSoup(page.content, 'html.parser') 

        # get product name & save for later file naming
        prod_name = ''
        try:
            name = soup.find(class_ = 'product-name')
            prod_name = helper_functions.remove_utf_charactars_and_strip(name.text)
            PRODUCT_INFORMATION['name'] = prod_name

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
            children = prod_feat.find_all('p')
            text = [i.text + '\n' for i in children]
            #print(text)
            PRODUCT_INFORMATION['description'] = ''.join(text)
        except:
            print("Could not add description (Features) category")



        # get product-info: Flavours, Unit of Measure, Product Code        
        try:
            
            info = soup.find(class_ = 'product-info')

            values = info.find_all('td')
            col_num = len(info.find_all('tr')[0].find_all('td'))
            pos_to_name_dict = {}
            for i in range(0, col_num):
                pos_to_name_dict[i] = values[i].text
            
            flavours = list()
            units = list()
            product_codes = list()

            #print(pos_to_name_dict)
            for i in range(col_num, len(values)):
                if 'Flavour' in pos_to_name_dict[i%col_num]:
                    flavours.append(values[i].text)
                elif 'Unit of Measure' in pos_to_name_dict[i%col_num]:
                    units.append(values[i].text)
                elif 'Product Code' in pos_to_name_dict[i%col_num]:
                    product_codes.append(values[i].text)

            #keeping potential to related product code and flavours and units
            for i in range(0, len(product_codes)):
                product_codes[i] = product_codes[i] + ':' + flavours[i] + '|' + units[i]

            #these names might not look quite matching, but these are the best matching fields from the last crawl fields
            PRODUCT_INFORMATION['Flavours'] = list(set(flavours))
            PRODUCT_INFORMATION['Sizes'] = list(set(units))
            PRODUCT_INFORMATION['item_type'] = product_codes
        except:
            print('Could not get product-info: Flavours, Unit of Measure, Product Code')

       # get ingredients
        try:
            ingredients = soup.find(id = 'ingridients')
            ingr = ingredients.find_all(text=True)
            PRODUCT_INFORMATION['ingredients'] = ''.join(ingr).lstrip()
        except:
            print("Could not add ingredients category")

        # get usage
        try:
            usage = soup.find(id = 'usage')
            usa = usage.find_all(text=True)
            PRODUCT_INFORMATION['usage'] = ''.join(usa).lstrip()
        except:
            print("Could not add usage category")

        # get nutri_info
        try:
            soup2 = BeautifulSoup(page.content,'lxml')
            nutri_info = soup2.find(id = 'nutritional-information')
            body = nutri_info.find('table')
        
            # Now writing tables straight to csv fr ease
            file_name = str(prod_name) + "_nutrition_table.csv"
            print(file_name)
            self.write_html_table_to_csv(body, csv_name= '{}{}{}'.format(path, 
            'Nutrition_tables/', file_name))
        except:
            print("Could not write nutrient table to csv file ")

        #get serving size from table
        try:
            nutri_info = soup.find(id = 'nutritional-information')
            body = nutri_info.find('table')
            #get Serving size
            heads = body.find_all('th')
            heads.pop(0) # remove name row
            serving_size = heads[0].text
            PRODUCT_INFORMATION['serving_size_1'] = serving_size
        except:
            print("could not get serving size")

    
        clinical_indications = None
        benefits = None
        features_table = list()
        
        try: 
            #clin_ind = soup.find("div", id = 'clinical-indications')
            clin_ind = soup.find(id="clinical-indications")
            #body = clin_ind.find('table') # get first child table

            ## Need to get the parent table and extract all children tables from it, avoid getting weird tables in addition
            

            #print(body)
            children_tbody = clin_ind.findAll("table", recursive=True)
            

            for tb in children_tbody:
                #print(tb.find('th').text)
                if tb.find('th').text == 'BENEFITS':    
                    benefits = [i.text.strip() for i in tb.find_all('td')]
                elif tb.find('th').text == 'CLINICAL INDICATIONS':                
                    clinical_indications = [i.text.strip() for i in tb.find_all('td')]
                elif tb.find('th').text == 'FEATURES': 
                    for row in tb.find_all('tr'):
                        print([ i.text.strip().strip('\r\n') for i in row.find_all('td')])
                        features_table.append([i.text.strip() for i in row.find_all('td')])

            PRODUCT_INFORMATION['feature_table_rows'] = helper_functions.remove_list_duplicates(features_table)
            PRODUCT_INFORMATION['benefits'] = helper_functions.remove_list_duplicates(benefits)
            PRODUCT_INFORMATION['clinical_indications'] = helper_functions.remove_list_duplicates(clinical_indications)

        except:
            missing_traits = ''
            if not clinical_indications:
                missing_traits = "Clinical indications "
            if not benefits:
                missing_traits += 'benefits '
            if not features_table:
                missing_traits += 'features_table '

            print("Could not fetch one of {}".format(''.join(missing_traits)))

        #helper_functions.print_dictionary_in_rows(PRODUCT_INFORMATION)
        return PRODUCT_INFORMATION    
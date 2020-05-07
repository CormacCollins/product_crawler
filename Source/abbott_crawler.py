from bs4 import BeautifulSoup
import requests
import re
import string
from Source.crawler_interface import crawler_interface
import sys
import Source.product_info_JSON
import pandas as pd
import Source.helper_functions as helper_functions

class AbbottStore_crawler(crawler_interface):

    def __init__(self):
        """ Implements crawler_interface
            Create instance of crawler loaded with list of links (link_list)
            Settings to be added as future change around potentially adding a small list of urls that need updating
        """
        pass
        

    
    # Gets upto 2 of the requested table - either vitamin, minerals, nutrients
    # needs to be tested as there may be unseen products with more than 2 tables
    def __get_prod_table_data(self, class_title_list, soup):
        dict_list = list()

        for tbl in class_title_list:
            new_dict = {}
            #nutrition data 1
            section_data = tbl.find(class_='section-data')
            rows = section_data.find_all(class_ = 'nutrition-name')
            row_data = section_data.find_all(class_ = 'nutrition-value amt')
            #sometimes the normal value is not there so at least we also get the daily % value

            # ------------------
            # have removed this because not necessary when providing serving size info
            #row_data_2 = section_data.find_all(class_ = 'nutrition-value dv')

            #print(section_data.text)
            #print([r.text for r in row_data])

            for i in range(0, len(rows)):
                new_dict[rows[i].text.strip()] = row_data[i].text.strip()

                # ------------------
                #have removed this because not necessary when providing serving size info
                #new_dict[rows[i].text.strip() + '(DV)'] = row_data_2[i].text.strip() + '%'

            dict_list.append(new_dict)

        return dict_list
    

    #get information on 1 link
    def get_product_info(self, prod_url, store_name, path):
        
        #print(prod_url)
        PRODUCT_INFORMATION = Source.product_info_JSON.PRODUCT_INFORMATION.copy()

        PRODUCT_INFORMATION['store'] = store_name
        PRODUCT_INFORMATION['url'] = prod_url
        
        try:
            page = requests.get(prod_url)
        except requests.exceptions.RequestException as e:
            #TODO: Better handling of error msgs
            print('failed to connect - please check url or connection')


        soup = BeautifulSoup(page.content, 'html.parser') 

        # get product name
        try:
            name = soup.find(class_ = 'pdp-info__title')
            nm = name.find_all(text=True)
            nm = ''.join(nm).lstrip().rstrip()
            PRODUCT_INFORMATION['name'] = nm
        except:
            print("Could not add name category")
        try:    
            price = soup.find(id = 'current-price')
            p = price.text
            PRODUCT_INFORMATION['price'] = p
        except:
            print("Could not add price category")

        try:
            size_weight = soup.find(class_ = 'pdp-info__pack-detail m-0')
            sw = size_weight.text.lstrip().rstrip()
            PRODUCT_INFORMATION['size_or_weight'] = sw
        except:
            print("Could not add size_or_weight category")

        # get availability info
        try:
            availability = soup.find(id = 'stock-status')
            a = availability.find_all(text=True)
            a = ''.join(a).strip('\n')
            PRODUCT_INFORMATION['availability'] = a
        except:
            print("Could not add availability category")

        try:
            item_attr = soup.find(id = 'pdp-sku')
            #it_type = item_attr.find(class_="type")
            it = item_attr.text
            #type_num = item_attr.find(class_= "value").text
            PRODUCT_INFORMATION['item_id'] = it.replace('SKU#:', '').lstrip()
        except:
            print("Could not add item_type category")

        try:
            prod_descr = soup.find(class_ = 'product-description')
            descr = prod_descr.find_all(text=True)
            info = ''.join(descr).lstrip().replace('_x000D_', '') #this will likely be fixed from the web devs at some point
            PRODUCT_INFORMATION['description'] = helper_functions.remove_utf_charactars_and_strip(info)
        except:
            print("Could not add name description")

        # data table additional-attributes ("More Information") section
        try:
            add_attr = soup.find(class_ = 'more-information').find('table')
            rows = add_attr.find_all('th')
            row_data = add_attr.find_all('td')   
            for i in range(0, len(rows)):
                info_title = rows[i].text.strip()

                #print('Info title {}'.format(info_title))
                #print(row_data[i].text.strip())
                # flavor will be a seperate dictionary of values added later
                if info_title != 'Flavor' or info_title != 'Flavors':
                    PRODUCT_INFORMATION[info_title] = row_data[i].text.strip()
        except:
            print("Could not add additional attributes categories")


        # flavour categories
        try:
            product_cart_form = soup.find(id = 'pdp-Flavors')
            #div_titles = product_cart_form.find_all(class_ = 'falvour-title')
            select_values = product_cart_form.find_all(text=True)
            flavors = [i for i in select_values if i != '\n']
            PRODUCT_INFORMATION['Flavours'] = flavors
        except:
            print("Could not add flavour categories")

        # All nutritional facts togethar, i.e. ingredients, allergin info...
        try:
            nutritionalinfo = soup.find_all(class_ = 'pdp-tab__nutri-info-text')
            #[print(i) for i in nutritionalinfo]
            n = len(nutritionalinfo)
            #ingredients
            try:    
                PRODUCT_INFORMATION['ingredients'] = nutritionalinfo[0].text.lstrip()
            except:
                print('Could not add ingredients')

            try:    
                PRODUCT_INFORMATION['allergin_info'] = nutritionalinfo[1].text.lstrip()
            except:
                print('Could not add allergin_info')

            try:    
                PRODUCT_INFORMATION['serving_size_1'] = nutritionalinfo[3].text.lstrip()
            except:
                print('Could not add serving_size_1')

            try:  
                print('Not adding footnotes currently')  
                #PRODUCT_INFORMATION['footnotes'] = nutritionalinfo[4].text.lstrip().rstrip()
            except:
                print('Could not add footnotes')

           
        except:
            print("Could not fetch nutritional facts")

        


        # --------------------------------------------------------------------------------------------------
        # there can be a special case where there are 2 nutrient datas - relative to 2 types of serving size

        unique_id = PRODUCT_INFORMATION['item_id'].strip()
        print(unique_id)        
        #Get up to 2 times nutrient table data
        try:
            tables = soup.find_all(class_ = 'pdp-tab__nutri-info-table')
            
            #attempt nutrient table
            try:            
                new_data_frame = pd.read_html(str(tables[0]))[0]
                #new_data_frame = pd.DataFrame(new_data_frame[0], index=[unique_id])
                path_ = path + 'Nutrition_tables'
                #print(path_)
                new_data_frame.to_csv(path_ + '/nutrient_table_' + unique_id + '.csv', index=False)
            except:
                print("Could not add nutrient_tables categories")

            #attempt vitamin table
            try:
                new_data_frame = pd.read_html(str(tables[1]))[0]
                path_ = path + 'Vitamin_tables'
                #print(path_)
                new_data_frame.to_csv(path_ + '/vitamin_table_' + unique_id + '.csv', index=False)
            except:
                print("Could not add vitamin_table categories")

            #attempt mineral tables
            try:
                new_data_frame = new_data_frame = pd.read_html(str(tables[2]))[0]
                path_ = path + 'Mineral_tables'
                new_data_frame.to_csv(path_ + '/mineral_table_' + unique_id + '.csv', index=False)
                    
            except:
                print("Could not add mineral_table categories")

        except:
            print("Could not any of nutrient, mineral or vitamin tables")
            #Get up to 2 times vitamin table data

        
        
        #for k,v in PRODUCT_INFORMATION.items():
         #   print('{}:{}'.format(k,v))

        

        #print(PRODUCT_INFORMATION['name'])
        return PRODUCT_INFORMATION



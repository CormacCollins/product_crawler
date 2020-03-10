from bs4 import BeautifulSoup
import requests
import re
import string
from Source.crawler_interface import crawler_interface
import sys

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

            for i in range(0, len(rows)):
                new_dict[rows[i].text.strip()] = row_data[i].text.strip()

            dict_list.append(new_dict)

        return dict_list
    

    #get information on 1 link
    def get_product_info(self, prod_url):
        
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

        # get product name
        try:
            name = soup.find(class_ = 'base')
            nm = name.find_all(text=True)
            nm = ''.join(nm)
            PRODUCT_INFORMATION['name'] = nm
        except:
            print("Could not add name category")
        try:    
            price = soup.find(class_ = 'price')
            p = price.text
            PRODUCT_INFORMATION['price'] = p
        except:
            print("Could not add price category")

        try:
            size_weight = soup.find(class_ = 'size-or-weight')
            sw = size_weight.text.lstrip()
            PRODUCT_INFORMATION['size_or_weight'] = sw
        except:
            print("Could not add size_or_weight category")

        # get availability info
        try:
            availability = soup.find(title = 'Availability')
            a = availability.find_all(text=True)
            a = ''.join(a).strip('\n')
            PRODUCT_INFORMATION['availability'] = a
        except:
            print("Could not add availability category")

        try:
            item_attr = soup.find(class_ = 'product attribute sku')
            it_type = item_attr.find(class_="type")
            it = it_type.text
            type_num = item_attr.find(class_= "value").text
            PRODUCT_INFORMATION['item_type'] = it + "#:" + type_num
        except:
            print("Could not add item_type category")

        try:
            prod_descr = soup.find(class_ = 'product attribute description')
            descr = prod_descr.find_all(text=True)
            info = ''.join(descr)
            PRODUCT_INFORMATION['description'] = info.lstrip()
        except:
            print("Could not add name description")

        # data table additional-attributes
        try:
            add_attr = soup.find(class_ = 'data table additional-attributes').find('tbody')
            rows = add_attr.find_all('th')
            row_data = add_attr.find_all('td')
            for i in range(0, len(rows)):
                info_title = rows[i].text.strip()
                # flavor will be a seperate dictionary of values added later
                if info_title != 'Flavor':
                    PRODUCT_INFORMATION[info_title] = row_data[i].text.strip()
        except:
            print("Could not add additional attributes categories")


        # flavour categories
        try:
            product_cart_form = soup.find(id = 'product_addtocart_form')
            div_titles = product_cart_form.find_all(class_ = 'falvour-title')
            select_values = product_cart_form.find_all('select')
            flavours = [select_values[i].text for i in range(0, len(div_titles)-1) if div_titles[i].text == 'Flavors']

            f = flavours[0].split('\n')
            #print(f)
            final_flavours = list()
            for i in f:
                #probably not very efficient!
                if any([c.isalpha() for c in i]):
                    #print(i)
                    final_flavours.append(i.strip().rstrip())
                    
            PRODUCT_INFORMATION['Flavours'] = final_flavours
        except:
            print("Could not add flavour categories")

        # nutrition-ingredient-value
        try:
            ingredients = soup.find(class_ = 'nutrition-ingredient-value')
            PRODUCT_INFORMATION['ingredients'] = ingredients.text.lstrip()
        except:
            print("Could not add ingredients category")

        try:
            allergin_info = soup.find(class_ = 'nutrition-AllergenStatement-value')
            PRODUCT_INFORMATION['allergin_info'] = allergin_info.text.lstrip()
        except:
            print("Could not add allergin_info category")

        #section serving-size
        try:
            serv_size = soup.find_all(class_ = 'section serving-size')
            for i in range(0, len(serv_size)):
                ss = serv_size[i].text
                PRODUCT_INFORMATION['serving_size_' + str(i+1)] = ss.lstrip().strip('Serving Size:').lstrip()
        except:
            print("Could not add serving size category")

        try:
            footnotes = soup.find_all(class_ = 'nutrition-footnote')
            f = ''
            for i in footnotes:
                f = f + " " + i.find(class_='footnote').text + '\n'
            PRODUCT_INFORMATION['footnotes'] = f
        except:
            print("Could not add footnote categories")



        # --------------------------------------------------------------------------------------------------
        # there can be a special case where there are 2 nutrient datas - relative to 2 types of serving size


        #Get up to 2 times nutrient table data
        try:
            add_attr = soup.find_all(class_ = 'section nutrient-data')
            #gets list of nutrient table data dictionaries and adds them
            count = 1
            for nutrient_dict in self.__get_prod_table_data(add_attr, soup):
                if count > 5:
                    print("Nutrient table number {} could not be added".format(count))
                #print('nutrient_table_' + str(count))
                PRODUCT_INFORMATION['nutrient_table_' + str(count)] = nutrient_dict
                count = count + 1
                                
        except:
            print("Could not add nutrient_tables categories")
        #Get up to 2 times vitamin table data
        try:
            add_attr = soup.find_all(class_ = 'section vitamin-data')
            count = 1
            for vitamin_dict in self.__get_prod_table_data(add_attr, soup):
                PRODUCT_INFORMATION['vitamin_table_' + str(count)] = vitamin_dict
                count = count + 1
        except:
            print("Could not add vitamin_table categories")
        #Get up to 2 times minerals table data
        try:
            add_attr = soup.find_all(class_ = 'section minerals-data')
            count = 1
            for minerals_dicts in self.__get_prod_table_data(add_attr, soup):
                PRODUCT_INFORMATION['mineral_table_' + str(count)] = minerals_dicts
                count = count + 1
        except:
            print("Could not add mineral_table categories")
        #for k,v in PRODUCT_INFORMATION.items():
        #    print('{}:{}'.format(k,v))

        return PRODUCT_INFORMATION



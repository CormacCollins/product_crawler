from bs4 import BeautifulSoup
import requests
import re
import csv
import string
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep


# get links for all the products displayed on that page
# recursive function that keeps getting moving to next page
# TODO: need safety mech for max recursive depth and memory
def get_products_from_product_page(prod_page_link, product_links):
    page = requests.get(prod_page_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    menu_list = soup.find_all('a', class_='product photo product-item-photo')
    for l in menu_list:
        product_links.append(l['href'])

    # then need to go to next link (i.e. press the arrow button at bottom of list to get next bunch of items)
    #returning 2 of same link at the moment
    #TODO: more accurate
    new_link = soup.find_all(class_ = "item pages-item-next")
    #Will be better way to do this, also could just append to the oriignal search string with ?p=2
    try:
        lk = re.search("(?P<url>https?://[^\s]+)", str(new_link[0])).group("url")
        #if another page of products keep scrapping, else end 
        if lk:
            print("Searching next page")
            print(lk)
            get_products_from_product_page(lk, product_links)
    
    except:
        print("End of product item range")

# Gets upto 2 of the requested table - either vitamin, minerals, nutrients
# needs to be tested as there may be unseen products with more than 2 tables
def get_prod_table_data(class_title_list, soup):
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
    '''
    if len(class_title_list) > 2: 
    # We do not expect this
        print('Must recode data model for more than 2 nutrition tables')
    elif len(class_title_list) == 2:

        #nutrition data 1
        section_data = class_title_list[0].find(class_='section-data')
        rows = section_data.find_all(class_ = 'nutrition-name')
        row_data = section_data.find_all(class_ = 'nutrition-value amt')

        for i in range(0, len(rows)):
            dict_1[rows[i].text.strip()] = row_data[i].text.strip()

        #nutrition data 2
        section_data = class_title_list[1].find(class_='section-data')
        rows = section_data.find_all(class_ = 'nutrition-name')
        row_data = section_data.find_all(class_ = 'nutrition-value amt')

        for i in range(0, len(rows)):
            dict_2[rows[i].text.strip()] = row_data[i].text.strip()

    else: #only 1
        #nutrition data 1
        section_data = class_title_list[0].find(class_='section-data')
        rows = section_data.find_all(class_ = 'nutrition-name')
        row_data = section_data.find_all(class_ = 'nutrition-value amt')    

        for i in range(0, len(rows)):
            dict_1[rows[i].text.strip()] = row_data[i].text.strip()

    return dict_1, dict_2
    '''

### RE_QUERY_PRODUCT_LINKS if all urls needed to be refreshed
### else will use csv file
def get_product_links(RE_QUERY_PRODUCT_LINKS = False):
    product_links = list()

    if RE_QUERY_PRODUCT_LINKS:

        site = "https://abbottstore.com/"

        # if query fails due to a connection error then sleep for 5 sec and retry again
        # up to 5 retries

        retry_requests = 5
        while retry_requests > 0:
            try:
                page = requests.get(site)
                retry_requests = 0
            except requests.exceptions.ConnectionError:
                retry_requests = retry_requests - 1
                if retry_requests == 0:
                    print("Could not connect after 5 attempts to:\n{}".format(site))
                print("Connection error - 5 second delay before re-request")                
                sleep(5)


        soup = BeautifulSoup(page.content, 'html.parser')

        #get menu with links
        menu_list = soup.find(class_='groupmenu')

        #get links in drop down for each product category
        menu_links = menu_list.find_all('a', class_='menu-link')

        links = list()
        names = list()
        #for each link go to new url and get items
        for l in menu_links:
            if 'menu-link' in l['class']:
                links.append(l['href'])
                names.append(l.find("span").text)

        #To note: the shop by brands link may have duplicates, but I havn't researched, it will be easier to remove duplicates later
        # Also does not continue crawling in shop by brand

        
        for link in links:
            n = names.pop(0)
            print('Searching brand range {}'.format(n))
            
            print(link)
            get_products_from_product_page(link, product_links)
            

        print("Prod num {}".format(len(product_links)))
        print(product_links[1:10])

        #write to csv for easier work during development:
        #just sotring the product links
        with open('product_links.csv', 'a', newline='') as csvfileWrite:
            writer = csv.writer(csvfileWrite, delimiter=',')
            for l in product_links:
                writer.writerow([l])

    else:
        
        with open('product_links.csv', 'r') as csvfileRead:
                reader = csv.reader(csvfileRead, delimiter=',', )
                for row in reader:
                    product_links.append(row[0])

    return product_links

#get information on 1 link
def get_product_info(prod_url):
    
    print(prod_url)

    PRODUCT_INFORMATION = {'url':'', 'name':'', 'price':'', 'size_or_weight':'','availability':'',	
                            'item_type':'',	'description':'', 'ingredients':'',	'allergin_info':'',	'serving_size_1':'', 
                            'serving_size_2':'', 'serving_size_3':'', 'serving_size_4':'', 'serving_size_5':'', 
                            'footnotes':'', 'nutrient_table_1': '', 'nutrient_table_2': '', 'nutrient_table_3': '', 
                            'nutrient_table_4': '', 'nutrient_table_5': '', 
                            'vitamin_table_1':'', 'vitamin_table_2':'', 'vitamin_table_3':'', 'vitamin_table_4':'', 'vitamin_table_5':'',	
                            'mineral_table_1':'', 'mineral_table_2':'', 'mineral_table_3':'', 'mineral_table_4':'', 'mineral_table_5':'', 
                            'more_info_1':'', 'more_info_2':'', 'more_info_3':'', 'more_info_4':''}

    PRODUCT_INFORMATION['url'] = prod_url
    
    
    page = requests.get(prod_url)
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
            PRODUCT_INFORMATION['more_info_' + str(i+1)] = row_data[i].text.strip()
    except:
        print("Could not add additional attributes categories")

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
            PRODUCT_INFORMATION['serving_size_' + str(i+1)] = ss.lstrip()
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
        for nutrient_dict in get_prod_table_data(add_attr, soup):
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
        for vitamin_dict in get_prod_table_data(add_attr, soup):
            PRODUCT_INFORMATION['vitamin_table_' + str(count)] = vitamin_dict
            count = count + 1
    except:
        print("Could not add vitamin_table categories")
    #Get up to 2 times minerals table data
    try:
        add_attr = soup.find_all(class_ = 'section minerals-data')
        count = 1
        for minerals_dicts in get_prod_table_data(add_attr, soup):
            PRODUCT_INFORMATION['mineral_table_' + str(count)] = minerals_dicts
            count = count + 1
    except:
        print("Could not add mineral_table categories")
    #for k,v in PRODUCT_INFORMATION.items():
    #    print('{}:{}'.format(k,v))

    return PRODUCT_INFORMATION



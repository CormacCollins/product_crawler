from bs4 import BeautifulSoup
import requests
import re
import csv
import string



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
    dict_1 = {}
    dict_2 = {}
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


### RE_QUERY_PRODUCT_LINKS if all urls needed to be refreshed
### else will use csv file
def get_product_links(RE_QUERY_PRODUCT_LINKS = False):
    product_links = list()

    if RE_QUERY_PRODUCT_LINKS:

        site = "https://abbottstore.com/"
        page = requests.get(site)
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
            #just for first product list
            #TODO: remove for getting full range!
            break

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
    
    PRODUCT_INFORMATION = {}

    PRODUCT_INFORMATION['url'] = prod_url
    print(prod_url)
    page = requests.get(prod_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    prod_descr = soup.find(class_ = 'product attribute description')
    descr = prod_descr.find_all(text=True)
    info = ''.join(descr)
    PRODUCT_INFORMATION['description'] = info

    # data table additional-attributes
    add_attr = soup.find(class_ = 'data table additional-attributes').find('tbody')
    rows = add_attr.find_all('th')
    row_data = add_attr.find_all('td')
    for i in range(0, len(rows)):
        PRODUCT_INFORMATION[rows[i].text.strip()] = row_data[i].text.strip()

    # nutrition-ingredient-value
    ingredients = soup.find(class_ = 'nutrition-ingredient-value').text
    PRODUCT_INFORMATION['ingredients'] = ingredients

    allergin_info = soup.find(class_ = 'nutrition-AllergenStatement-value').text
    PRODUCT_INFORMATION['allergin_info'] = allergin_info

    #section serving-size
    serv_size = soup.find_all(class_ = 'section serving-size')
    for i in range(0, len(serv_size)):
        ss = serv_size[i].text
        PRODUCT_INFORMATION['serving_size_' + str(i+1)] = ss

    footnotes = soup.find_all(class_ = 'nutrition-footnote')
    f = ''
    for i in footnotes:
        f = f + " " + i.find(class_='footnote').text + '\n'
    PRODUCT_INFORMATION['footnotes'] = f



    # --------------------------------------------------------------------------------------------------
    # there can be a special case where there are 2 nutrient datas - relative to 2 types of serving size


    #Get up to 2 times nutrient table data
    add_attr = soup.find_all(class_ = 'section nutrient-data')
    nutrient_dicts = get_prod_table_data(add_attr, soup)
    for i in range(0, len(nutrient_dicts)-1):
        PRODUCT_INFORMATION['nutrient_table_' + str(i+1)] = nutrient_dicts[i]

    #Get up to 2 times vitamin table data
    add_attr = soup.find_all(class_ = 'section vitamin-data')
    vitamin_dicts = get_prod_table_data(add_attr, soup)
    for i in range(0, len(vitamin_dicts)-1):
        PRODUCT_INFORMATION['vitamin_table_' + str(i+1)] = vitamin_dicts[i]

    #Get up to 2 times minerals table data
    add_attr = soup.find_all(class_ = 'section minerals-data')
    minerals_dicts = get_prod_table_data(add_attr, soup)
    for i in range(0, len(minerals_dicts)-1):
        PRODUCT_INFORMATION['mineral_table_' + str(i+1)] = minerals_dicts[i]

    return PRODUCT_INFORMATION



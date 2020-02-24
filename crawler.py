from bs4 import BeautifulSoup
import requests
import re
import csv


# get links for all the products displayed on that page
# recursive function that keeps getting moving to next page
# TODO: need safety mech for max recursive depth and memory
def get_products_from_product_page(prod_page_link, prod_list):
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
            get_products_from_product_page(lk, prod_list)
    
    except:
        print("End of product item range")
    
### -----------------------------------------------------
### ---------------- MAIN SCRIPT ------------------------
### -----------------------------------------------------
GET_PRODUCT_LINKS = False
product_links = list()


if GET_PRODUCT_LINKS:

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


#trial on one link
#Get 'Product description', 'More information' and Nutrition facts from product page

#product description
prod_url = product_links[0]
print(prod_url)
page = requests.get(prod_url)
soup = BeautifulSoup(page.content, 'html.parser')
prod_descr = soup.find(class_ = 'product attribute description')
descr = prod_descr.find_all(text=True)
print(descr)

# data table additional-attributes

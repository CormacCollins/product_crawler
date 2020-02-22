from bs4 import BeautifulSoup
import requests
import re


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
    #page = requests.get(prod_page_link)
    #soup = BeautifulSoup(page.content, 'html.parser')

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
    

### MAIN SCRIPT ###

site = "https://abbottstore.com/"
page = requests.get(site)
soup = BeautifulSoup(page.content, 'html.parser')

#get menu with links
menu_list = soup.find(class_='groupmenu')

#get links in drop down for each product category
menu_links = menu_list.find_all('a', class_='menu-link')

links = list()
#for each link go to new url and get items
for l in menu_links:
    if 'menu-link' in l['class']:
        links.append(l['href'])

#To note: the shop by brands link may have duplicates, but I havn't researched, it will be easier to remove duplicates later
# Also does not continue crawling in shop by brand

product_links = list()
for link in links:
    print(link)
    get_products_from_product_page(link, product_links)
    #just for first product list
    #break

print("Prod num {x}", len(product_links))
print(product_links[1:10])





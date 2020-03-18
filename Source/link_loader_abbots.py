from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import re

class Link_loader_abbotts:
    def __init__(self, abbots_file_name_csv):
        """ Gets links for crawler, either by initial crawl from website, or by getting 
            pre-stored links in csv file
            TODO: settings around not just overwritting urls but to modify etc.
        """
        self.abbots_file_name = abbots_file_name_csv


    def get_product_links_abbotstore(self, site, RE_QUERY_PRODUCT_LINKS = False):
        """ Returns list of url links for each product 
            Set RE_QUERY_PRODUCT_LINKS = True to get all links again, False will
            read from csv file
        """
        product_links = list()

        if RE_QUERY_PRODUCT_LINKS:

            # if query fails due to a connection error then sleep for 5 sec and retry again
            # up to 5 retries

            page = None
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

            if not page:
                print("Could now reach: {}".format(site))
                return {}

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
                self.__get_products_from_product_page(link, product_links)
                

            print("Prod num {}".format(len(product_links)))
            #print(product_links[1:10])

            #write to csv for easier work during development:
            #just sotring the product links
            with open(self.abbots_file_name, 'w', newline='') as csvfileWrite:
                writer = csv.writer(csvfileWrite, delimiter=',')
                for l in product_links:
                    writer.writerow([l])

        else:
            
            with open(self.abbots_file_name, 'r') as csvfileRead:
                    reader = csv.reader(csvfileRead, delimiter=',', )
                    for row in reader:
                        product_links.append(row[0])

        return product_links

        
    # get links for all the products displayed on that page
    # recursive function that keeps getting moving to next page
    # TODO: need safety mech for max recursive depth and memory

    def __get_products_from_product_page(self, prod_page_link, product_links):
        page = requests.get(prod_page_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        menu_list = soup.find_all('a', class_='product photo product-item-photo')
        count = 0
        for l in menu_list:
            count += 1
            product_links.append(l['href'])

        print("{} urls added".format(count))
        # then need to go to next link (i.e. press the arrow button at bottom of list to get next bunch of items)
        #returning 2 of same link at the moment
        #TODO: more accurate
        new_link = soup.find_all(class_ = "item pages-item-next")
        #Will be better way to do this, also could just append to the oriignal search string with ?p=2


        if new_link:
            lk = re.search("(?P<url>https?://[^\s]+)", str(new_link[0])).group("url")
            #if another page of products keep scrapping, else end 
            if lk:
                print("Searching next page")
                print(lk)
                self.__get_products_from_product_page(lk, product_links)
        else:
            print("End of product item range")

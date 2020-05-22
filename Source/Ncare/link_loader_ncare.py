from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import re
'''
Class that is given the base website for products and crawls to extract all product links
All will be custom build for specific sights, but act the same with inputs and outputs
'''

class Link_loader_ncare:
    def __init__(self, ncare_file_name_csv):
        """ Gets links for crawler, either by initial crawl from website, or by getting 
            pre-stored links in csv file
            TODO: settings around not just overwritting urls but to modify etc.
        """
        self.ncare_file_name = ncare_file_name_csv


    def get_product_links(self, site, RE_QUERY_PRODUCT_LINKS = False):
        """ Returns list of url links for each product 
            Set RE_QUERY_PRODUCT_LINKS = True to get all links again, False will
            read from csv file
        """
        product_links = list()

        if RE_QUERY_PRODUCT_LINKS:

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
            menu_list = soup.find(class_='block block-list')

            #get links in drop down for each product category
            menu_links = menu_list.find_all('a')
            #To note: the shop by brands link may have duplicates, but I havn't researched, it will be easier to remove duplicates later
            # Also does not continue crawling in shop by brand

            
            for link in menu_links:
                n = link.text
                print('Searching brand range {}'.format(n))                
                print(link['href'])
                l = list()
                l = self.__get_products_from_product_page(link['href'], l)
                product_links.extend(l)
                #[print(i) for i in product_links]
                
            #write to csv for easier work during development:
            #just sotring the product links
            with open(self.ncare_file_name, 'w', newline='') as csvfileWrite:
                writer = csv.writer(csvfileWrite, delimiter=',')
                for l in product_links:
                    writer.writerow([l])

        else:
            
            with open(self.ncare_file_name, 'r') as csvfileRead:
                    reader = csv.reader(csvfileRead, delimiter=',', )
                    for row in reader:
                        product_links.append(row[0])

        return product_links

        
    # Non-recursive
    # Passes argument to view all products in list on webpage
    # returns with duplicats
    def __get_products_from_product_page(self, prod_page_link, product_links):
        payload = {'limit':'all'}
        page = requests.get(prod_page_link, params=payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        m = soup.find(class_= 'products-grid')
        ls = m.find_all('a')
        for i in ls:
            product_links.append(i['href'])
        
        return set(product_links)

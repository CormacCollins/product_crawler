from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import re
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
'''
Class that is given the base website for products and crawls to extract all product links
All will be custom build for specific sights, but act the same with inputs and outputs
'''

SELENIUM_PATH = 'Drivers\chromedriver.exe'

class Link_loader_abbotts:
    def __init__(self, abbots_file_name_csv):
        """ Gets links for crawler, either by initial crawl from website, or by getting 
            pre-stored links in csv file
            TODO: settings around not just overwritting urls but to modify etc.
        """
        self.abbots_file_name = abbots_file_name_csv


    def get_product_links(self, site, RE_QUERY_PRODUCT_LINKS = False):
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
            menu_list = soup.find(class_='abbott-brands-nav d-none d-md-flex flex-column')

            #get links in drop down for each product category
            menu_links = menu_list.find_all('p', class_='list-comp__title')

            links = list()
            names = list()
            #for each link go to new url and get items
            for l in menu_links:
                #print(l.a['href'])
                if 'list-comp__title' in l['class']:
                    links.append(l.a['href'])
                    names.append(l.a.text)


            print(names) #['Similac', 'Ensure', 'PEDIASURE', 'FREE STYLE BRAND', 'PEDIALYTE', 'NEPRO', 'GLUCERNA', 'ZONEPERFECT', 'MORE BRANDS']
            #To note: the shop by brands link may have duplicates, but I havn't researched, it will be easier to remove duplicates later
            # Also does not continue crawling in shop by brand
            
            for link in links:
                n = names.pop(0)
                print('Searching brand range {}'.format(n))
                
                if n == 'MORE BRANDS':
                    print(link)
                    self.get_more_brands(link, product_links)
                    continue

                print(link)
                self.use_selenium_get_links(link, product_links)

            print("Total number of links fetched {}".format(len(product_links)))
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

    def elment_exists_selenium(self, driver, el_name):
        return (len(driver.find_elements_by_id(el_name)) > 0)

    def use_selenium_get_links(self, prod_page_link, product_links):

        #print(os.getcwd())

        print('searching: {}'.format(prod_page_link))
        page = None
        retries = 5
        DO_QUERY = True

        #TODO: will needs better erorr handling if fully automated
        while(DO_QUERY):
            try:
                page = requests.get(prod_page_link)
                DO_QUERY = False 
            except page.status_code == 429:
                #too many reuqests
                retry_after_time = int(page.headers["Retry-After"])
                print('Too many requests error. Retrying after {} seconds'.format(retry_after_time))
                sleep(retry_after_time)
                retries -= 1
                if retries < 1:
                    DO_QUERY = False
                print('{} retries remaining'.format(retries))
            except requests.exceptions.RequestException as e:
                #TODO: Better handling of error msgs
                retries -= 1
                if retries < 1:
                    DO_QUERY = False
                print('failed to connect - please check url or connection')
                print('{} retries remaining'.format(retries))

        if retries == 0:
            return


        soup = BeautifulSoup(page.content, 'html.parser')
        # Need to set the driver in the for loop, otherwise website blocks it
        driver =  webdriver.Chrome(SELENIUM_PATH)
        driver.set_page_load_timeout(500)

        # Initiate driver with url
        driver.get(prod_page_link)
        
        # Wait until page loads
        driver.implicitly_wait(30)


        # Click "I am a HCP"
        times = 1
        button_available = False

        try:
            button_available = driver.find_element_by_id("loadMore")
        except:
            print('Button not available - fetching available links')
            menu_list = driver.find_elements_by_class_name('search-page-product__card--figure')

            for item in menu_list: 
                product_links.append((item.get_attribute('href')))
            print('Obtained {} links'.format(len(menu_list)))
            return

        while self.elment_exists_selenium(driver, 'loadMore'):
            print('Pressing button {} times'.format(times))
            driver.find_element_by_id("loadMore").click()    
            driver.implicitly_wait(5)
            sleep(1.5)
            times += 1
            
        print('Button finished')


        menu_list = driver.find_elements_by_class_name('search-page-product__card--figure')

        for item in menu_list: 
            product_links.append((item.get_attribute('href')))
        print('Obtained {} links'.format(len(menu_list)))
        
        #Close browser
        driver.stop_client()
        driver.close()
        driver.quit()

    def get_more_brands(self, prod_page_link, product_links):
        page = requests.get(prod_page_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        #print(soup.prettify())
        menu_list = soup.find_all('a', class_='cmp-text')
        count = 0
        for l in menu_list:
            count += 1
            product_links.append(l['href'])

        print('More brands found: {}'.format(len(menu_list)))

    def __get_products_from_product_page(self, prod_page_link, product_links):
        page = requests.get(prod_page_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        #print(soup.prettify())
        menu_list = soup.find_all('a', class_='col-md-3 col-sm-4 col-6 search-page-product__card')
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

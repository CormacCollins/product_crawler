import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep



class Link_loader_nutricia():
    

    chromedriver = "../Drivers/chromedriver.exe"

    driver =  webdriver.Chrome(chromedriver)

    driver.set_page_load_timeout(300)


    def get_product_links_nutricia(self, url):

        mylist = []

        for u in url:
            # Initiate driver with url
            Link_loader_nutricia.driver.get(u)
            # Wait until page loads
            Link_loader_nutricia.driver.implicitly_wait(30)
            # Click "I am a HCP"
            try:
                Link_loader_nutricia.driver.find_element_by_xpath("//*[@id='HCPModal']/div/div/div/div/a[1]").click()
                Link_loader_nutricia.driver.implicitly_wait(5)
            except:
                pass
            
            try:
                # Click "I am from Mainland UK" - to get the most amount of products
                Link_loader_nutricia.driver.find_element_by_xpath("//*[@id='ctl00_head_CountrySwitcher_notLoggedInUK']").click()
                # Add sleep to allow for slow internet connections
                sleep(10)
                # Click view all to get all the products on the one page
            except:
                pass
            
            try:
                view_all = Link_loader_nutricia.driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_ViewAllButton']")
                view_all.click()
                # Allow javascript on page to load "view all"
                sleep(30)
            except:
                pass
            # Now that the whole page is showing in the chromedriver, we can scrape the whole thing
            soup = BeautifulSoup(Link_loader_nutricia.driver.page_source, "html.parser")
            # Get the products
            soup_pro_list = soup.find(class_='products-list')
            # Get all the a tags - links to products
            for link in soup_pro_list.find_all('a'):
                mylist.append("https://www.nutriciahcp.com"+link.get('href'))
            Link_loader_nutricia.driver.quit()
            sleep(30)


        df = pd.DataFrame(mylist)

        df.to_csv('../Data/Nutricia/nutricia_links.csv')
            


links = Link_loader_nutricia()

url = ["https://www.nutriciahcp.com/adult/products/#",
     "https://www.nutriciahcp.com/adult/products/paediatrics",
     "https://www.nutriciahcp.com/adult/products/metabolics"]

links.get_product_links_nutricia(url)




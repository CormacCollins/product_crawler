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
    
    # Can't put driver as a global variable as websites block it


    def get_product_links_nutricia(self, url):

        mylist = []

        for u in url:
            
            # Need to set the driver in the for loop, otherwise website blocks it
            driver =  webdriver.Chrome("../Drivers/chromedriver.exe")
            driver.set_page_load_timeout(500)
            sleep(10)
            
            # Initiate driver with url
            driver.get(u)
            
            # Wait until page loads
            driver.implicitly_wait(30)
            
            
            try:
                # Click "I am a HCP"
                driver.find_element_by_xpath("//*[@id='HCPModal']/div/div/div/div/a[1]").click()
                driver.implicitly_wait(10)
            except:
                pass
            
            try:
                # Click "I am from Mainland UK" - to get the most amount of products
                driver.find_element_by_xpath("//*[@id='ctl00_head_CountrySwitcher_notLoggedInUK']").click()
                
                # Add sleep to allow for slow internet connections
                sleep(10)   
                
            except:
                pass
            
            try:
                # Click view all to get all the products on the one page
                view_all = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_ViewAllButton']")
                view_all.click()
                
                # Allow javascript on page to load "view all"
                sleep(30)
                
            except:
                pass
            
            # Now that the whole page is showing in the chromedriver, we can scrape the whole thing
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Get the products
            soup_pro_list = soup.find(class_='products-list')
            
            # Get all the a tags - links to products
            for link in soup_pro_list.find_all('a'):
                mylist.append("https://www.nutriciahcp.com"+link.get('href'))
            
            # Completely close everything to make website believe it's a new handshake
            driver.close()    
            driver.quit()
            sleep(120)


        df = pd.DataFrame(mylist)

        return df.to_csv('../Data/Nutricia/nutricia_links.csv')

            


links = Link_loader_nutricia()

urls = ["https://www.nutriciahcp.com/adult/products/#",
       "https://www.nutriciahcp.com/adult/products/paediatrics",
       "https://www.nutriciahcp.com/adult/products/metabolics"]


links.get_product_links_nutricia(urls)
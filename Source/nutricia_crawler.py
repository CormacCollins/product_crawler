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

# TO DO - Create a proper object out of the code below


chromedriver = "../Drivers/chromedriver.exe"

driver =  webdriver.Chrome(chromedriver)

driver.set_page_load_timeout(150)

url = "https://www.nutriciahcp.com/adult/products/#"

driver.get(url)

# Wait until page loads
driver.implicitly_wait(30)
# Click "I am a HCP"
driver.find_element_by_xpath("//*[@id='HCPModal']/div/div/div/div/a[1]").click()
driver.implicitly_wait(5)
# Click "I am from Mainland UK" - to get the most amount of products
driver.find_element_by_xpath("//*[@id='ctl00_head_CountrySwitcher_notLoggedInUK']").click()

sleep(10)
# Click view all to get all the products on the one page
view_all = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_ViewAllButton']")
view_all.click()

sleep(30)

# Now that the whole page is showing in the chromedriver, we can scrape the whole thing
soup = BeautifulSoup(driver.page_source, "html.parser")

mylist = []


soup_pro_list = soup.find(class_='products-list')

# Get all the a tags - links to products

for link in soup_pro_list.find_all('a'):
    mylist.append("https://www.nutriciahcp.com"+link.get('href'))

df = pd.DataFrame(mylist)

df.to_csv('../Data/Nutricia/nutricia_links.csv')

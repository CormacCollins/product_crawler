import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


class Nutricia_crawler:



  def get_product_info(self, prod_url):
      
      PRODUCT_INFORMATION = {'url':[],
                      'name':[],
                      'category':[],
                      'brand':[],
                      'pack_size':[],
                      'case_size':[],
                      'indications':[],
                      'precautions':[],
                      'directions_for_use':[],
                      'shelf_life':[],
                    'flavours':[]}
      
      
      for u in prod_url:

          PRODUCT_INFORMATION['url'].append(u)


          page = requests.get(u)

          soup = BeautifulSoup(page.content, 'html.parser')
          
          try:
              #Get Name
              name = soup.find_all('h3')
              nm = name[0].text

              PRODUCT_INFORMATION['name'].append(nm)
              
          except:
              PRODUCT_INFORMATION['name'].append("not found")

          
          try:
              #Get Category
              category = soup.find_all('div', class_ = 'panel-body')
              category = category[1]
              category = category.find_all('div')
              category = category[1].text

              PRODUCT_INFORMATION['category'].append(category)
              
          except:
              PRODUCT_INFORMATION['category'].append("not found")
              
          try:
              #Get Brand
              brand = soup.find_all('div', class_ = 'panel-body')
              brand = brand[1]
              brand = brand.find_all('div')
              brand = brand[3].text

              PRODUCT_INFORMATION['brand'].append(brand)
              
          except:
              PRODUCT_INFORMATION['brand'].append("not found")


          try:
              #Get Pack Size
              pack_size = soup.find_all('div', class_ = 'panel-body')
              pack_size = pack_size[1]
              pack_size = pack_size.find_all('div')
              pack_size = pack_size[5].text

              PRODUCT_INFORMATION['pack_size'].append(pack_size)
              
          except:
              PRODUCT_INFORMATION['pack_size'].append("not found")

          
          try:
              #Get Case Size 
              case_size = soup.find_all('div', class_ = 'panel-body')
              case_size = case_size[1]
              case_size = case_size.find_all('div')
              case_size = case_size[7].text

              PRODUCT_INFORMATION['case_size'].append(case_size)
              
          except:
              PRODUCT_INFORMATION['case_size'].append("not found")
              
          try:
              #Get Indications
              indications = soup.find_all('div', class_ = 'directions-container')
              indications = indications[0]
              indications = indications.find_all('p')
              indications = indications[0].text

              PRODUCT_INFORMATION['indications'].append(indications)
              
          except:
              PRODUCT_INFORMATION['indications'].append("not found")
              
          try:
              #Get precautions
              precautions = soup.find_all('div', class_ = 'directions-container')
              precautions = precautions[0]
              precautions = precautions.find_all('p')
              precautions = precautions[1].text

              PRODUCT_INFORMATION['precautions'].append(precautions)
              
          except:
              PRODUCT_INFORMATION['precautions'].append("not found")


          try:
              #Get directions for use
              directions_for_use = soup.find_all('div', class_ = 'directions-container')
              directions_for_use = directions_for_use[0]
              directions_for_use = directions_for_use.find_all('p')
              directions_for_use = directions_for_use[2].text

              PRODUCT_INFORMATION['directions_for_use'].append(directions_for_use)
              
          except:
              PRODUCT_INFORMATION['directions_for_use'].append("not found")

              
          try:
              # Get Shelf Life
              shelf_life = soup.find_all('div', class_ = 'directions-container')
              shelf_life = shelf_life[0]
              shelf_life = shelf_life.find_all('p')
              shelf_life = shelf_life[3].text

              PRODUCT_INFORMATION['shelf_life'].append(shelf_life)
              
          except:
              PRODUCT_INFORMATION['shelf_life'].append("not found")

          try:
              # Get flavours
              flavours = soup.find(class_='accordion')
              flavours = flavours.find_all('div', class_='panel-body flavours-available')
              flavours = flavours[0]
              flavours = flavours.find_all('p', text=True)
              flavours = flavours[0].text

              PRODUCT_INFORMATION['flavours'].append(flavours)
              
          except:
              PRODUCT_INFORMATION['flavours'].append("not found")
      

      return pd.DataFrame.from_dict(PRODUCT_INFORMATION).to_csv("../Data/Nutricia/nutricia_products.csv")



products = Nutricia_crawler()

links = pd.read_csv('../Data/Nutricia/nutricia_links.csv')
links_array = links["0"].values


products.get_product_info(links_array)
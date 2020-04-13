from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import warnings
warnings.simplefilter('ignore')
import pandas as pd
import numpy as np


class Link_loader_flavour_creations():
    

    def get_product_links_flavour_creations(self, url):

      page = requests.get(url, verify=False)

      soup = BeautifulSoup(page.content, 'html.parser')

      parent_links = []
      child_links = []

      for link in soup.find_all('a', attrs={'href': re.compile("^https://www.flavourcreations.com.au/products/")}):
          parent_links.append(link.get('href'))          
          
      for x in parent_links:
          p = requests.get(x, verify=False)
          s = BeautifulSoup(p.content, 'html.parser')
          for t in s.find_all('a', attrs={'href': re.compile("^https://www.flavourcreations.com.au/products/")}):
              child_links.append(t.get('href'))

      df = pd.DataFrame(child_links)
      df.drop_duplicates(inplace=True)

      return df.to_csv("../Data/Flavour_Creations/Flavour_Creation_Links.csv", index=False)


links = Link_loader_flavour_creations()

url = "https://www.flavourcreations.com.au/products/"

links.get_product_links_flavour_creations(url)

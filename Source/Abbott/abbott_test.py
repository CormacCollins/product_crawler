import link_loader_abbots as link_loader_abbots
from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import re
import os


if os.path.exists(os.getcwd()):
    print(os.getcwd())



#store = 'https://abbottstore.com/'



#
#l_loader = link_loader_abbots.Link_loader_abbotts('test.csv')
#urls = l_loader.get_product_links('https://abbottstore.com/', True)
#for l in urls:
#    print(l)
from bs4 import BeautifulSoup
import requests
import re
import string
from Source.crawler_interface import crawler_interface
import sys

class Ncare_crawler(crawler_interface):

    def __init__(self):
        """ Implements crawler_interface
            Create instance of crawler loaded with list of links (link_list)
            Settings to be added as future change around potentially adding a small list of urls that need updating
        """
        pass

    #get information on 1 link
    def get_product_info(self, prod_url):
        pass    
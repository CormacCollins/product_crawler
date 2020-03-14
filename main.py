from Source.abbott_crawler import AbbottStore_crawler
from Source.ncare_crawler import Ncare_crawler

from Source.link_loader_abbots import Link_loader_abbotts
from Source.link_loader_ncare import Link_loader_ncare

import Source.write_customer_data_to_csv as writer
import sys
from pathlib import Path    



def main_ncare(stores_list, command_types, crawler):

    store = 'Ncare'

    #create sub folder for data files if it doesn't exist
    Path('Data/' + store).mkdir(parents=True, exist_ok=True)

    #for reading saved links list
    file_path = 'Data/' + store + '/'
    file_uri = file_path + store + '_product_links.csv'

    #Get links - pass true if you want to requery the product urls
    l_loader = Link_loader_ncare(file_uri)
    links = l_loader.get_product_links_abbotstore(stores_list[store], False)
    
    #get each ind prod info and write to db        
    for l in links:
        print("Getting product from url {}".format(l))
        info = crawler.get_product_info(l)
        writer.write(info, file_path + store + '_scrape_data.csv')


def main_abbott(stores_list, command_types, crawler):

    if len(sys.argv) <= 2:
        give_instructions(command_types, stores_list)
        return

    #get args
    store = sys.argv[1]
    command = sys.argv[2]

    if store not in stores_list.keys():
        print("Store does not exist in list")
        return

    #create sub folder for data files if it doesn't exist
    Path('Data/' + store).mkdir(parents=True, exist_ok=True)

    #for reading saved links list
    file_path = 'Data/' + store + '/'
    file_uri = file_path + store + '_product_links.csv'

    if command == 'scrape_stored':  

        #Get links - pass true if you want to requery the product urls
        l_loader = Link_loader_abbotts( file_uri)
        links = l_loader.get_product_links_abbotstore(stores_list[store], False)

        #get each ind prod info and write to db        
        for l in links:
            print("Getting product from url {}".format(l))
            info = crawler.get_product_info(l)
            writer.write(info, file_path + store + '_scrape_data.csv')

    elif command == 'full_scrape':

        #Get links - pass true if you want to requery the product urls
        l_loader = Link_loader_abbotts(file_uri)
        links = l_loader.get_product_links_abbotstore(stores_list[store], True)
        
        #get each ind prod info and write to db        
        for l in links:
            print("Getting product from url {}".format(l))
            info = crawler.get_product_info(l)
            writer.write(info, file_path + store + '_scrape_data.csv')

    elif 'single_url' in command:

        l = command.split('\\')[1]       
        print("Getting product from url {}".format(l))
        info = crawler.get_product_info(l)
        writer.write(info, file_path + store + '_scrape_data.csv')
        
    else:
        give_instructions(command_types, stores_list)

def give_instructions(command_types, stores_list):
    print("Give commands for product store and crawl type\n")
    print("Command types:")
    print("\n".join(command_types))
    print("\nCrawl stores include:") 
    print("\n".join(stores_list.keys()))
    print("\nE.g. main.py Abbott scrape_stored")


def ryan_main(stores_list, command_types, crawler):

    '''
    store = #'Nutricia'

    #create sub folder for data files if it doesn't exist
    Path('Data/' + store).mkdir(parents=True, exist_ok=True)

    #for reading saved links list
    file_path = 'Data/' + store + '/'
    file_uri = file_path + store + '_product_links.csv'
    
    #Get links - pass true if you want to requery the product urls
    l_loader = #Link_loader_ncare(file_uri)
    links = #l_loader.get_product_links_abbotstore(stores_list[store], False)
    
    #get each ind prod info and write to db        
    for l in links:
        print("Getting product from url {}".format(l))
        info = #crawler.get_product_info(l)
        writer.write(info, file_path + store + '_scrape_data.csv')
        '''


if __name__ == "__main__":

    command_types = ['scrape_stored', 'full_scrape', 'single_url\\url']    

    #TODO: Could be read from a xml file with all the currently operational stores
    stores_list = {'Abbott':'https://abbottstore.com/', 'Ncare':'https://www.ncare.net.au/nutrition-products', 'Nutricia':'https://www.nutriciahcp.com/adult/products/'}
    ryan_main(stores_list, command_types, Ncare_crawler())
    
    #main_ncare(stores_list, command_types, Ncare_crawler())

    #main_abbott(stores_list, command_types, AbbottStore_crawler())


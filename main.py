from Source.Abbott.abbott_crawler import AbbottStore_crawler
from Source.Ncare.ncare_crawler import Ncare_crawler

from Source.Abbott.link_loader_abbots import Link_loader_abbotts
from Source.Ncare.link_loader_ncare import Link_loader_ncare

import Source.write_customer_data_to_csv as writer
import sys
from pathlib import Path   
import time
import os
import Source.helper_functions as helper_functions

import Source.task_threader as task_threader  

def give_instructions(command_types, stores_list):
    print("Give commands for product store and crawl type\n")
    print("Command types:")
    print("\n".join(command_types))
    print("\nCrawl stores include:") 
    print("\n".join(stores_list.keys()))
    print("\nE.g. main.py Abbott scrape_stored")

        
def run_scrapper(stores_list, command_types, link_loader, crawler, command, store, file_path, file_uri, M_THREADING):

    #TODO: Have writer create new abbotts_data csv file to write new info to (instead of having to delete it before a re-run)
    if command == 'scrape_stored':  
        #remove old scrape data
        #if os.path.exists(file_path + store + '_scrape_data.csv'):
        #    os.remove(file_path + store + '_scrape_data.csv')

        start = time.time()
        #Get links - pass true if you want to requery the product urls
        links = l_loader.get_product_links(stores_list[store], False)

        #get each ind prod info and write to db 
        info_list = list()  
        count = 0
        
        if M_THREADING:
            while links:
                task_threader.thread_tasks(links, info_list, crawler, count, store, file_path)
                count += 1
        else:
            for l in links:
                print("Getting product from url {}".format(l))
                info = crawler.get_product_info(l, store_name=store, path=file_path)
                info_list.append(info)

        end = time.time()

        print('Crawl time: {}'.format(end - start))
        write_path = file_path + store + '_scrape_data.csv'
        if os.path.exists(write_path):
            os.remove(write_path) 
        for info in info_list:            
            writer.write(info, write_path)


        #write to csv seperately to avoid multiplae thread access    
        #for info in info_list:
         #   writer.write(info, file_path + store + '_scrape_data.csv')

    elif command == 'full_scrape':
        #remove old scrape data
        #if os.path.exists(file_path + store + '_scrape_data.csv'):
        #    os.remove(file_path + store + '_scrape_data.csv')

        #Get links - pass true if you want to requery the product urls
        links = l_loader.get_product_links(stores_list[store], True)

        start = time.time()

        #get each ind prod info and write to db 
        info_list = list()  
        count = 0

        if M_THREADING:
            print('Threading:')
            while links:
                task_threader.thread_tasks(links, info_list, crawler, count, store, file_path)
                count += 1  
        else:
            for l in links:
                print("Getting product from url {}".format(l))
                info = crawler.get_product_info(l, store_name=store, path=file_path)
                info_list.append(info)

        end = time.time()

        print('Crawl time: {}'.format(end - start))  
        write_path = file_path + store + '_scrape_data.csv'
        if os.path.exists(write_path):
            os.remove(write_path)
        for info in info_list:            
            writer.write(info, write_path)

    #currently using for test not writing
    elif 'single_url' in command:

        l = command.split('\\')[1]       
        print("Getting product from url {}".format(l))
        info = crawler.get_product_info(l, store_name=store, path=file_path)

        #writer.write(info, file_path + store + '_scrape_data.csv')
        helper_functions.print_dictionary_in_rows(info)
    else:
        give_instructions(command_types, stores_list)
    


if __name__ == "__main__":

    # ------------------ Get args --------------------------------------

    #Current commands available
    command_types = ['scrape_stored', 'full_scrape', 'single_url\\url']  
    #Stores with scrapers
    stores_list = {'Abbott':'https://abbottstore.com/', 'Ncare':'https://www.ncare.net.au/nutrition-products', 'Nutricia':'https://www.nutriciahcp.com/adult/products/'}


    #check for suitable commands
    if len(sys.argv) <= 2:
        give_instructions(command_types, stores_list)
        sys.exit()

    #get args
    store = sys.argv[1]
    command = sys.argv[2]

    if store not in stores_list.keys():
        print("Store does not exist in list")
        sys.exit()

    #create sub folders for data files if it doesn't exist
    Path('Data/' + store).mkdir(parents=True, exist_ok=True)
    Path('Data/' + store + '/Nutrition_tables').mkdir(parents=True, exist_ok=True)
    Path('Data/' + store + '/Vitamin_tables').mkdir(parents=True, exist_ok=True)
    Path('Data/' + store + '/Mineral_tables').mkdir(parents=True, exist_ok=True)
    Path('Data/' + store + '/Clinical_indications_tables').mkdir(parents=True, exist_ok=True)

    #for reading saved links list
    file_path = 'Data/' + store + '/'
    file_uri = file_path + store + '_product_links.csv'

    # -------------------- RUN CHOSEN CRAWLER WITH ARGS -----------------------------------

    if store == 'Abbott':
    #main_abbott(stores_list, command_types, AbbottStore_crawler(), command, store, file_path, file_uri)
        l_loader = Link_loader_abbotts( file_uri)
        abbott_crawler = AbbottStore_crawler()
        run_scrapper(stores_list, 
                    command_types, 
                    l_loader, 
                    abbott_crawler, 
                    command, 
                    store, 
                    file_path, 
                    file_uri,
                    M_THREADING=True)

    elif store == 'Ncare':
        l_loader = Link_loader_ncare( file_uri)
        ncare_crawler = Ncare_crawler()
        #threading not suited to the small amount of links and most likely writing to csv files
        run_scrapper(stores_list, 
                    command_types, 
                    l_loader, 
                    ncare_crawler, 
                    command, 
                    store, 
                    file_path, 
                    file_uri,
                    M_THREADING=False)
    











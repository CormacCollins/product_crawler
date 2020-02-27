import crawler
import write_customer_data_to_csv

def main():
    #Get links - pass true if you want to requery the product urls
    links = crawler.get_product_links(False)
    
    #get each ind prod info and write to db
    for l in links:
        info = crawler.get_product_info(l)
        write_customer_data_to_csv.write(info)
        



if __name__ == "__main__":
    main()


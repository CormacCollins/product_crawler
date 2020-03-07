from crawler import AbbotStore_crawler
from link_loader import Link_loader
import write_customer_data_to_csv

def main():
    #Get links - pass true if you want to requery the product urls
    l_loader = Link_loader('abbot_product_links.csv')
    links = l_loader.get_product_links_abbotstore('https://abbottstore.com/', False)
    crawler = AbbotStore_crawler()
    #get each ind prod info and write to db
    
    for l in links:
        print("Getting product from url {}".format(l))
        info = crawler.get_product_info(l)
        write_customer_data_to_csv.write(info)
        break
    


if __name__ == "__main__":
    main()


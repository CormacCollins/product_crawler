### NOTICE! - 29/4 changed for Abbott, Cormac fixing crawler currentlty


### General usage of crawler
 Call function  main.py by passing 2 arguments: 
 * A store name: eg. Abbott  
 * A query type currently: 
   - scrape_stored 
   - full_scrape 
   - single_url\url
   
 Examples of call types:
 ```
 main.py Abbott scrape_stored 
 main.py Abbott single_url\https://abbottstore.com/similac-advance-infant-formula-powder-1-45-lb-container-53359e.html
 ```
# program general structure
![Image description](https://github.com/CormacCollins/product_crawler/blob/master/Images/5.2%20structure%20chart%20(2).png)

# product_crawler

The objective of the project is to create a total product catalogue across 4 competitors in the Nutritional Health Care space.

_Ideally_ we would like to compare the following features across the competitors:

- Pack size (weight, volume)
- Pack format (bottle, can, container) 
- Flavours
- Pricing
- Number of products in pack
- Ingredients
- Nutrients
- Use of the product

We could also look at the following:

- Number of products by company for shared category
- Most used ingredients across all categories
- Total different flavours available
- Different disease states these companies set to manage

The competitors we will review will be the following:

- Abbott
- Fresenius
- Nutricia
- Nestle Health Science
- Flavour Creations

The information will be derived from the following sources

## Abbott

https://abbottstore.com/


## Fresenius

https://fresubin.com/au/product-catalogue

or

https://www.brightsky.com.au/epages/shop.sf/en_AU/?ObjectID=900311&ViewAction=ViewFaceted&FacetValue_CategoryID=900311&FacetValue_Manufacturer=Fresenius+Kabi&CurrencyID=AUD&CurrencyID=AUD&FacetRange_ListPrice=&FacetRange_ListPrice=

## Nutricia

https://www.nutriciahcp.com/adult/products/


## Nestle Health Science

https://www.ncare.net.au/nutrition-products


## Flavour Creations

https://www.flavourcreations.com.au/products/



## Final Product

A SQL database will be created in the end which can either become:

- A data product
- Deployed into a web app

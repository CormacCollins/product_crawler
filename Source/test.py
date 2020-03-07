


#print(prod_url)

from bs4 import BeautifulSoup
import requests
prod_url = 'https://abbottstore.com/pedialyte-advancedcare-plus-orange-breeze-1-liter-bottle-case-of-4-67434.\
html'
page = requests.get(prod_url)
soup = BeautifulSoup(page.content, 'html.parser') 


# flavour categories

product_cart_form = soup.find(id = 'product_addtocart_form')
div_titles = product_cart_form.find_all(class_ = 'falvour-title')
select_values = product_cart_form.find_all('select')
flavours = [select_values[i].text for i in range(0, len(div_titles)-1) if div_titles[i].text == 'Flavors']
#add dict of flavours - using first select option
#print(flavours[0].strip('\n').lsplit().splitlines())

f = flavours[0].split('\n')
#print(f)
final_flavours = list()
for i in f:
    #probably not very efficient!
    if any([c.isalpha() for c in i]):
        print(i)
        final_flavours.append(i.strip().rstrip())

print(final_flavours)

#text_flavs = "".join(flavours[0])



#flavs = text_flavs.split()


#print(flavs)

#print("Could not add flavour categories")
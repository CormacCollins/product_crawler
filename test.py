
import csv

product_links = ["Entry " + str(i) for i in range(10)]
with open('product_links.csv', 'a', newline='') as csvfileWrite:
    writer = csv.writer(csvfileWrite, delimiter=',')
    print(product_links)
    for l in product_links:
        writer.writerow([l])

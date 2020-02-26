import pandas as pd
import os.path
from os import path
import csv
#write data frame as a row to csv
#data needs to be cleaned more before entering

# Df is adding a zero in first column, for now I have just made it a new column

def create_sheet(data_dict):
    if not path.exists('data.csv'):
        print('making file')
        with open('data.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            l = list()
            l.append('ID')
            l.extend(list(data_dict))
            filewriter.writerow(l)
    
   #else file exists


def write(data_dict):
    create_sheet(data_dict)
    df = pd.DataFrame([data_dict])
    print(df.url)
    df.to_csv('data.csv', mode='a', header=False)
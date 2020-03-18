import pandas as pd
import os.path
from os import path
import csv
from datetime import datetime
#write data frame as a row to csv
#data needs to be cleaned more before entering

def __write_new(data_dict, file_name):
    print('{} does not exist - making file'.format(file_name))
    df = pd.DataFrame([data_dict])
    #df.drop([''], axis=1, inplace=True)
    df.to_csv(file_name, mode='w', header=True)
    

def write(data_dict, file_name):
 
    #add the time/date of scrape for this info
    now = datetime.now()
    d_time = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict['entry_date'] = d_time        

    # if it's a new csv file then create it and write it there, else write the new entry below
    if not path.exists(file_name): 
        __write_new(data_dict, file_name)
    else:
        df = pd.DataFrame([data_dict])
        df.to_csv(file_name, mode='a', header=False)    

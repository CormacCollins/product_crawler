import pandas as pd
import os.path
from os import path
import csv
#write data frame as a row to csv
#data needs to be cleaned more before entering

def write(data_dict, file_name):

    df = pd.DataFrame([data_dict])
    df.to_csv(file_name, mode='a', header=False)

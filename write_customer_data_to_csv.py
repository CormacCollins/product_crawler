import pandas as pd

#write data frame as a row to csv
#data needs to be cleaned more before entering

def write(data_dict, key):
    df = pd.DataFrame([data_dict])
    df.to_csv('my_csv.csv', mode='a', header=False)
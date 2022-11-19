import pandas as pd
import pdb

csv_file = '../Data/ATL_vs_NO_September112022.csv'
pd.read_csv(csv_file)
pdb.set_trace()

def check_data(csv_file:str):
    a = pd.read_csv(csv_file)
    return a.raw_time.values[-1] == "0:00 - 4th) "

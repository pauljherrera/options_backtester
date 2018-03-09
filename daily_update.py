import pandas as pd
import numpy as np
from config import config
from datadownloader import DataDownloader

downloader = DataDownloader()




def main():
   
    df =pd.read_csv('MRK-2016-01-01-2018-01-31.csv')
    df = df.sort_values(by= ['trade_date'])
    my_feeder.feed_data(strategy = strategy , data= df)

if __name__ == '__main__':
    main()
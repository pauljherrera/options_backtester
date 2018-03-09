import pandas as pd
import numpy as np
from tqdm import tqdm
from config import config
from datafeeder import DataFeeder
from strategys import CoveredCall


start_date = config['start_date']
end_date = config['end_date']
ticker = config['ticker']

my_feeder = DataFeeder()
strategy = CoveredCall()




def main():
   
    #df =pd.read_csv('MRK-2016-01-01-2018-01-31.csv')
    #df = df.sort_values(by= ['trade_date'])
    my_feeder.feed_data(strategy = strategy )

if __name__ == '__main__':
    main()
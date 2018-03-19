import pandas as pd
import numpy as np
from tqdm import tqdm
from config import config
from data.datafeeder import DataFeeder
from strategies.strategies import ProtectivePut,CoveredCall

strate = config['strategy']
start_date = config['start_date']
end_date = config['end_date']
ticker = config['ticker']

if strate == 'CoveredCall' :
    
    strategy = CoveredCall()
else:
    
    strategy = ProtectivePut()

my_feeder = DataFeeder()



def main():
   
    df =pd.read_csv('Historical Data/test_data/GOOGL-2016-01-01-2018-02-01.csv')
    df = df.sort_values(by= ['trade_date'])
    my_feeder.feed_data(strategy = strategy, data= df)

if __name__ == '__main__':
    main()
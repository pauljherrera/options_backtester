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
   
    my_feeder.feed_data(strategy = strategy)

if __name__ == '__main__':
    main()

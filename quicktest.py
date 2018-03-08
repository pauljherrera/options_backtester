import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
from tqdm import tqdm
from config import config
from datadownloader import DataDownloader
from datafeeder import DataFeeder
from strategys import CoveredCall


start_date = config['start_date']
end_date = config['end_date']
ticker = config['ticker']

feeder = DataFeeder()
#feeder.checker()



def main():
    my_feeder = DataFeeder()
    strategy = CoveredCall()
    #my_feeder.feed_data()
    #my_feeder.big_query_request(start_date,end_date,ticker)
    my_feeder.feed_data(strategy)
    #downloader = DataDownloader()
    
    #downloader.create_dataset('Creation','DataSet created from Script, First Test')
    #downloader.create_table()
    #downloader.load_data_from_file('Creation','First_Table_FromApi','Historical Data/OSMV-20151118.csv')
    #downloader.load_multiple_files(dataset = 'Creation',table = 'First_Table_FromApi')

if __name__ == '__main__':
    main()
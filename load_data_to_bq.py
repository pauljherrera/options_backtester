import pandas as pd
import numpy as np
from config import config
from datafeeder import DataFeeder
from datadownloader import  DataDownloader
start_date = config['start_date']
end_date = config['end_date']
ticker = config['ticker']

feeder = DataFeeder()
downloads = DataDownloader()



def main():
    #downloads.create_table()
    downloads.load_multiple_files('Options_backtester','OSMV_TABLES')
if __name__ == '__main__':
    main()
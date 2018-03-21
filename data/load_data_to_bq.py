import pandas as pd
import numpy as np
from config import config
from data.datafeeder import DataFeeder
from data.datadownloader import  DataDownloader
start_date = config['start_date']
end_date = config['end_date']
ticker = config['ticker']

feeder = DataFeeder()
downloads = DataDownloader()



def main():
    downloads.load_multiple_files('Options_backtester','OSMV_TABLES')
if __name__ == '__main__':
    main()
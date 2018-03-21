import pandas as pd
import numpy as np
from config import config
from data.datafeeder import DataDownloader

downloader = DataDownloader()




def main():
   
   downloader.load_multiple_files('options_backtester','OSMV_TABLES')

if __name__ == '__main__':
    main()
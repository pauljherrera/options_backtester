import pandas as pd
import numpy as np
from config import config
from data.datadownloader import DataDownloader

downloader = DataDownloader()




def main():
   """
   Function that download todays data from Quandl and upload it to GoogleBigQuery
   """
   downloader.daily_update()

if __name__ == '__main__':
    main()
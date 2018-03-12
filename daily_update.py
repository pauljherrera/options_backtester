import pandas as pd
import numpy as np
from config import config
from datadownloader import DataDownloader

downloader = DataDownloader()




def main():
   
    downloader.daily_update()

if __name__ == '__main__':
    main()

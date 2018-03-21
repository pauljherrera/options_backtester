import pandas as pd
import numpy as np
from config import config
from data.datafeeder import DataFeeder

downloader = DataFeeder()




def main():
   
   downloader.checker()

if __name__ == '__main__':
    main()
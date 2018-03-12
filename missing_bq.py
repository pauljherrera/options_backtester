import pandas as pd 
import os 
import re
from datadownloader import DataDownloader

downloader = DataDownloader()




def checker():  #Probaly deprecated on V2
        """Function to check wether a list of dates is available on the historical data
        """
        dates = os.listdir('Historical Data')
        dirs = []
        for date in dates:
            d = re.sub('[^0-9]+','',date)
            dirs.append(d)
        df = pd.read_csv('results-20180312-103311.csv')
        raw_list_bq = df['trade_date'].tolist()
        list_bq = []
        for item  in raw_list_bq:
            a = re.sub('[^0-9]+','',item)
            list_bq.append(a)

        difference = list(set(dirs) - set(list_bq))
        
        osmv_diff = []
        for date in difference:
            dif = 'OSMV-'+date+'.csv'
            osmv_diff.append(dif)

    
        return osmv_diff


if __name__ == '__main__':
    a = checker()
    print(a)
    print(len(a))
    downloader.load_multiple_files('Options_backtester','OSMV_TABLES',a)
    
    

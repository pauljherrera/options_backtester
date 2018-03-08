import pandas as pd 
import numpy as np 
from google.cloud import bigquery
from pandas.io import gbq
import os
import re

from config import config
from datadownloader import DataDownloader



ticker = config['ticker']
start_date = config['start_date']
end_date = config['end_date']


class DataFeeder():
    

    def __init__(self,*args,**kwargs):
        
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker


    def feed_data(self,strategy = None,**kwargs):
        
        data = self.big_query_request(self.start_date,self.end_date,self.ticker)
        trade_dates = self.range_dates()
        dates = data['trade_date'].drop_duplicates()

        for date in dates :
            daily_data = data[data['trade_date']==date]
            strategy.update(daily_data)

    def checker(self):  #Probaly deprecated on V2
        """Function to check wether a list of dates is available on the historical data
        """
        dates = os.listdir('Historical Data')
        dirs = []
        for date in dates:
            d = re.sub('[^0-9]+','',date)
            dirs.append(d)
        users_range = self.__range_dates()
        difference = list(set(users_range) - set(dirs))
        if not difference:
            print('All data available, proceeding to Backtest')
            Result = True
        else:
            print('Aditional data needed, proceeding to download followings dates :')
            print('\n'.join(map(str, difference)))
            donwloads.missing_dates(difference)
        

    def range_dates(self): 
        """Function to make a range between Start_date and end_date
        """

        my_dates = pd.bdate_range(start_date,end_date)
        duel = pd.DataFrame(my_dates)
        duel[0] = duel[0].dt.strftime('%Y-%m-%d')
        missing_dates = duel[0].tolist()
        return missing_dates


    def big_query_request(self,start_date,end_date,ticker):
        """Function that extract data from BigQuery

        :param start_date: Initial date of backteste
        :type start_date: String

        :param end_date: Initial date of backteste
        :type end_date: String 

        :param ticker: Ticker name
        :type ticker: String
        """
        query = """
                                SELECT ticker,stkPx,expirDate, strike, trade_date, yte
                                FROM  [advance-mantis-188120:Creation.First_Table_FromApi]
                                WHERE ticker = '%s' AND DATE(trade_date) BETWEEN ('%s') AND ('%s')
                                LIMIT
                                10000
                                """ %(ticker,start_date,end_date)

        projectid = 'advance-mantis-188120'
        data_frame = pd.read_gbq(query, projectid,private_key = 'Harvested Backtest Framework-c01b8a37c1fb.json')
        
        return data_frame
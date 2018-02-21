import pandas as pd 
import numpy as np 
import sqlite3
from sqlite3 import Error
from google.cloud import bigquery
from pandas.io import gbq
import os
import re

from config import config
from datadownloader import DataDownloader



ticker = config['ticker']
start_date = config['start_date']
end_date = config['end_date']

donwloads = DataDownloader()

class DataFeeder():
    

    def __init__(self,*args,**kwargs):
        
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        database = "options_backtester.db"

        # create a database connection                     #Test Purpose 
        db = self.create_connection(database)
        self.conn = db


    def feed_data(self,*args,**kwargs):
        
        data = self.data_scavenger(self.start_date,self.end_date,self.ticker)

        [print(row[1:])  for row in data.itertuples()]


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
        

    def __range_dates(self): 
        """Function to make a range between Start_date and end_date
        """

        my_dates = pd.date_range(start_date,end_date)
        duel = pd.DataFrame(my_dates)
        duel[0] = duel[0].dt.strftime('%Y%m%d')
        missing_dates = duel[0].tolist()
        return missing_dates

    def data_scavenger(self,start_date,end_date,ticker):     #Deprecated
        """ Simulation of BigQuery usage. The idea is to use the same parameters that we should 
        use with GBQ.  
        """
        query =  "SELECT ticker, stkPx, expirDate, strike, trade_date, yte from 'OSMV-20180213' where trade_date BETWEEN ? and ? AND ticKer = ? ;"
        start_date = config['start_date']
        end_date = config['end_date']
        ticker = config['ticker']
        conn = self.conn
        table = pd.read_sql_query(query, conn, params= (start_date,end_date,ticker))
        table = table.sort_values(by='trade_date')
        table = table.set_index('trade_date')
       
        table.index = pd.to_datetime(table.index,format = '%Y-%m-%d')
        return table

    
    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

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
                                FROM  [advance-mantis-188120:Options_backtester.First_Table]
                                WHERE ticker = '%s' AND DATE(trade_date) BETWEEN ('%s') AND ('%s')
                                LIMIT
                                1000
                                """ %(ticker,start_date,end_date)

        projectid = 'advance-mantis-188120'
        data_frame = pd.read_gbq(query, projectid,private_key = 'Harvested Backtest Framework-c01b8a37c1fb.json')
        print(data_frame)
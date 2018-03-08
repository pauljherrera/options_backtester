# -*- coding: utf-8 -*-

import pandas as pd
import datetime as dt



config = {
    # General config.
    'start_data': dt.datetime(2018, 1, 1),
    'end_date': dt.datetime(2018, 2, 1),

    # Strategy config.
    'ticker': 'GOOG',
}



class DataDownloader:
    def missingData(self,missinDates):
        for date in missingDates:
            self.download

        

    def dataDownload(date):
        download(date)
        extractzip()
        

class DataFeeder:
    def __init__(self, strategy=None, *args, **kwargs):
        self.strategy = strategy
        
        
    def feed_data():
        for i in self.data.values:
            # Filter data to be sent.
            
            # Updating the strategy.
            self.strategy.update(data)
    
    

        

class Strategy(StrategyBase):
    def update(data):
        # Strategy logic.
        pass
    

    
    
class OptionsTrader():
    def __init__(self, *args, **kwargs):
        # Creating dataframe for logging trades.
        columns = ['Ticker', 'Price', 'Side', 'Quantity'] # Date will be the index.
        self.asset_log = pd.DataFrame(columns=columns)

        columns = ['Ticker', 'Price', 'Side', 'Type', 'expirDate',
                   'strike', 'Quantity']                  # Date will be the index.  
        self.options_log = pd.DataFrame(columns=columns)
        
        
    def buy_asset():
        pass
    
    def sell_asset():
        pass
    
    def buy_call():
        pass
    
    def buy_put():
        pass
    
    def sell_call():
        pass
    
    def sell_put():
        pass
        



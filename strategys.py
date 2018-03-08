import pandas as pd 
import numpy as np 
from config import config
import matplotlib.pyplot as plt 
frecuency = config['frecuency']
OTM_high = config['%OTM'] + 1
OTM_low = config['%OTM'] - 1
pd.options.mode.chained_assignment = None
premiun = config['premiun']


class CoveredCall():
    """
    Abstract base class for strategies.
    """
    def load(self, data):
        dates = data['trade_date'].drop_duplicates()  #Extract list of dates to iterate over
        open_trade = True

        for date in dates :
            daily_data = data[data['trade_date']==date] #Only data for the current date

            if open_trade == True:   #Indicate entry opportunity

                entry = self.entry(daily_data)

                if entry.empty == False:     #If there is a value in the DataFrame
                    open_trade = False       #We won't take a position while this value is false
                    selected_option = entry.iloc[0]
                    stk_price1 = selected_option['stkPx']
                    strike_price = selected_option['strike']
                    expir_date = selected_option['expirDate']
                    option_trade = self.sell_call(10)
                    share_trade = self.buy_share(100)

            else:
                
                if date >= expir_date :
                    final_price = daily_data['stkPx'].iloc[0]
                    self.pnl(stk_price1,final_price,strike_price,share_trade)
                    open_trade = True
            

    def entry(self,data):
        
        data['%OTM'] =  ((data['strike'] * 100)/data['stkPx'] ) - 100 #Convert price to %OTM

        data['condition'] = np.where((data['yte'].between(0.03, 0.034)) & (data['%OTM'].between(OTM_low,OTM_high) ),True,False)
        true_values = data[data['condition']==True]
        return true_values
    def buy_share(self,value):
        shares = value
        return shares
    def sell_call(self,value):
        calls = value
        return calls

    def pnl(self,initial_stk_price,final_stk_price,strike,shares):
        
        shares_pnl = (final_stk_price-initial_stk_price) * shares

        short_call_pnl = np.where(final_stk_price > strike,(strike-final_stk_price ) + premiun, (premiun * shares))
        
        covered_call_pnl = np.where(final_stk_price>strike,
        ((strike-initial_stk_price)+premiun)*shares,((final_stk_price-initial_stk_price)+premiun)*shares)
       
        print(shares_pnl)
        print(short_call_pnl)
        print(covered_call_pnl)
    def expiration_date(self,data):
        pass
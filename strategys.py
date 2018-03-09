import pandas as pd 
import numpy as np 
from config import config
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set()
sns.axes_style('darkgrid')
frecuency = config['frecuency']
OTM_high = config['%OTM'] + 1
OTM_low = config['%OTM'] - 1
pd.options.mode.chained_assignment = None
premiun = config['premiun']
duration = config['duration']
config_shares = config['shares']
config_options = config['options']



class CoveredCall():
    """
    Abstract base class for strategies.
    """
    def load(self, data):
        dates = data['trade_date'].drop_duplicates()  #Extract list of dates to iterate over
        open_trade = True
        row_list = [] #List of rows to add to DataFrame

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
                    trade_date = selected_option['trade_date']
                    option_trade = self.sell_call(config_options)
                    share_trade = self.buy_share(config_shares)

            else:
                
                if date >= expir_date :
                    final_price = daily_data['stkPx'].iloc[0]
                    row = self.pnl(stk_price1,final_price,strike_price,share_trade,option_trade,trade_date)
                    row_list.append(row)
                    open_trade = True
        df = pd.DataFrame(row_list,columns = ['shares_pnl','sell_call_pnl','covered_call_pnl','strike','initial_stkPx','final_stkPX','trade_date'])
        self.stats_and_plot(df)

    def entry(self,data):
        
        data['%OTM'] =  ((data['strike'] * 100)/data['stkPx'] ) - 100 #Convert price to %OTM

        data['condition'] = np.where((data['yte'].between(duration, duration+0.02)) & (data['%OTM'].between(OTM_low,OTM_high) ),True,False)
        true_values = data[data['condition']==True]
        return true_values


    def buy_share(self,value):
        shares = value
        return shares


    def sell_call(self,value):
        calls = value
        return calls

    def pnl(self,initial_stkPx,final_stkPx,strike,shares,options,trade_date):
        
        shares_pnl = (final_stkPx-initial_stkPx) * shares

        sell_call_pnl = np.where(final_stkPx > strike,((strike-final_stkPx )+premiun)*100*options, (premiun * 100 * options))
        
        covered_call_pnl = shares_pnl + sell_call_pnl
        #covered_call_pnl = np.where(final_stkPx > strike,((strike - initial_stkPx) + premiun) * shares,(
            #(final_stkPx - initial_stkPx ) + premiun) * shares )
        
        dict_round = {
            'shares_pnl':shares_pnl,
            'sell_call_pnl':sell_call_pnl,
            'covered_call_pnl':covered_call_pnl,
            'strike':strike,
            'initial_stkPx':initial_stkPx,
            'final_stkPX': final_stkPx,
            'trade_date':trade_date
        } 

        return dict_round

    def stats_and_plot(self,dataFrame):
        
        df = dataFrame
        print(df)

        df['cumsum']= df['covered_call_pnl'].cumsum()
        df.set_index('trade_date')

        plt.plot(df['trade_date'],df['cumsum'] )
        plt.gcf().autofmt_xdate()
        plt.title('Accounting Curve')
        plt.ylabel('Profit')
        plt.xlabel('Date')
        plt.legend("Hola")
        
        std = df['covered_call_pnl'].std()
        mean = df['covered_call_pnl'].mean()
        sharpe_ratio = mean/std


        win_loss = pd.DataFrame(np.where(df['covered_call_pnl']>=0,1,0))
        win_ratio = (win_loss.sum()*100)/win_loss.count()
        loss_ratio = 100-win_ratio
        total_profit = df['cumsum'].iloc[-1]


        print("Win - Loss ratio is : %d %% WIN and  %d %% LOSS \nWith a SharpeRatio of : %f and a total Profit of %d $" 
        %(win_ratio,loss_ratio,sharpe_ratio,total_profit))

      


        plt.show()


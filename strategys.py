import pandas as pd 
import numpy as np 
from tqdm import tqdm
from config import config
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set()
sns.axes_style('darkgrid')

OTM_high = config['%OTM'] + 1
OTM_low = config['%OTM'] - 1
pd.options.mode.chained_assignment = None
premiun = config['premiun']
duration = config['duration']
config_shares = config['initial_position']
positionPercent = config['%ofPosition']
options = (positionPercent*100)/config_shares
exchange_comisions = config['exchange_comisions']
frec = config['frecuency']

class CoveredCall():
    """
    Abstract base class for strategies.
    """
    def load(self, data):
        dates = data['trade_date'].drop_duplicates()  #Extract list of dates to iterate over
        open_trade = True
        row_list = [] #List of rows to add to DataFrame
        acum = 1      #Acumu variable to handle frecuency change
        print('Procceding to Backtest:')
        print('\b')
        for date in tqdm(dates) :
            acum +=1
            daily_data = data[data['trade_date']==date] #Only data for the current date
            if open_trade == True:   #Indicate entry opportunity

                entry = self.entry(daily_data)

                if entry.empty == False:     
                    #If there is a value in the DataFrame
                    open_trade = False       
                    #We won't take a position while this value is false
                    selected_option = entry.iloc[0] 
                    #Select the first option, this can be improve to match exactly the parameters (Optimize)
                    stk_price1 = selected_option['stkPx']
                    strike_price = selected_option['strike']
                    expire_date = selected_option['expirDate']
                    trade_date = selected_option['trade_date']
                    option_trade = self.sell_call(options)   
                    #Sell Call
                    share_trade = self.buy_share(config_shares)
                    #Buy Shares

                    df_final_price = data[(data['trade_date'] >= expire_date)]         
                    # We look into the dataFrame the price when the trade date is equal Or bigger than trade_date       

                    if df_final_price.empty == False:     
                        final_price = df_final_price['stkPx'].iloc[0]   
                    #Now that we the prices we take de 0 position (it doesn´t matter order)

                        row = self.pnl(stk_price1,final_price,strike_price,share_trade,option_trade,trade_date,expire_date) 
                        #Calculate the P&L of the selected options, it returns a dict that we add to a list and then to a DF
                        row_list.append(row)
            else:
              
                if acum >= frec :
                    open_trade = True
                    #If the frecuency is reach, we open the trade to start looking for the next entry date.
                    acum=1
                    #Reset the dates

        df = pd.DataFrame(row_list,columns = ['trade_date','expire_date','shares_pnl','sell_call_pnl','covered_call_pnl','strike'])
    
        self.stats_and_plot(df)

    def entry(self,data):
        
        data['%OTM'] =  ((data['strike'] * 100)/data['stkPx'] ) - 100 #Convert price to %OTM

        data['condition'] = np.where((data['yte'].between(duration, duration+0.011)) & (data['%OTM'].between(OTM_low,OTM_high) ),True,False)
        true_values = data[data['condition']==True]
        return true_values


    def buy_share(self,value):
        shares = value
        return shares


    def sell_call(self,value):
        calls = value
        return calls

    def pnl(self,initial_stkPx,final_stkPx,strike,shares,options,trade_date,expire_date):
        
        shares_pnl = (final_stkPx-initial_stkPx) * shares

        sell_call_pnl = np.where(final_stkPx >= strike,(-(final_stkPx -strike )+ premiun) *100*options, (premiun * 100 * options))
        
        covered_call_pnl = shares_pnl + sell_call_pnl
        #covered_call_pnl = np.where(final_stkPx > strike,((strike - initial_stkPx) + premiun) * shares,(
            #(final_stkPx - initial_stkPx ) + premiun) * shares )
       
        dict_round = {
            'shares_pnl':shares_pnl,
            'sell_call_pnl':np.round(sell_call_pnl,2),
            'covered_call_pnl':covered_call_pnl,
            'strike':strike,
            'trade_date':trade_date,
            'expire_date':expire_date
        } 

        return dict_round

    def stats_and_plot(self,dataFrame):
        
        df = dataFrame
        
        df['cumsum_covered']= df['covered_call_pnl'].cumsum()
        df['cumsum_stock']= df['sell_call_pnl'].cumsum()
        df['cumsum_option']= df['shares_pnl'].cumsum()

        df = df.set_index('trade_date')
        print(df[['expire_date','shares_pnl','sell_call_pnl','covered_call_pnl']])

        std = df['covered_call_pnl'].std()
        mean = df['covered_call_pnl'].mean()
        sharpe_ratio = mean/std

        win_loss = pd.DataFrame(np.where(df['covered_call_pnl']>=0,1,0))
        win_ratio = (win_loss.sum()*100)/win_loss.count()
        loss_ratio = 100-win_ratio
        comisions = len(df.index) * exchange_comisions
        profit = df['cumsum_covered'].iloc[-1] 
        stocks_profit = df['cumsum_stock'].iloc[-1]
        option_profit = df['cumsum_option'].iloc[-1]
        total_profit = profit -  comisions
        
    
        print('\nNumbers of trade: {trades}.'.format(trades = len(df.index)),
              'Total profit: {profit} $.'.format(profit = round(total_profit)),
              'Options profit: {op} $.'.format(op=round(option_profit,2)),
              'Stock profit : {sp} $.'.format(sp=round(stocks_profit,2)),
              'Mean: {mean} $.'.format(mean = round(mean,2)),
              'Standard deviation : {std} $.'.format(std = round(std,2)),
              'Sharpe ratio: {sr} .'.format(sr = round(sharpe_ratio,2)),
              'Comision rate : {c}.'.format(c = comisions),
              sep='\n\n')
      
        plt.plot(df.index,df['cumsum_covered'] )
        plt.gcf().autofmt_xdate()
        plt.title('Accounting Curve')
        plt.ylabel('Profit')
        plt.xlabel('Date')
        plt.show()

class PutProtective():
    pass

if __name__ == '__main__':
    main()
    
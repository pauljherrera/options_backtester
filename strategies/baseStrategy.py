import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt #Style config for plots
import seaborn as sns
sns.set()
sns.axes_style('darkgrid')

from config import config
from tqdm import tqdm

pd.options.mode.chained_assignment = None

duration_days = config['duration']
duration = duration_days/365
OTM = config['%OTM']
OTM_high = config['%OTM'] + 1
OTM_low = config['%OTM'] - 1
rule_number = config['buy/sell stock']
exchange_comisions = config['exchange_comisions']
shares = config['initial_position']
positionPercent = config['%ofPosition']
start_date = config['start_date']
end_date = config['end_date']
ticker_ = config['ticker']
frec = config['frecuency']
fill_price = config['fillPrice']

class BaseStrategy():
    
    def backtest(self, data): 
        dates = data['trade_date'].drop_duplicates()  #Extract list of dates to iterate over
        open_trade = True
        row_list = [] #List of rows to add to DataFrame
        acum = 1      #Acumu variable to handle frecuency change
        print('Procceding to Backtest:')
        generator = self.buy_share()
        for date in tqdm(dates) :
            acum +=1
            daily_data = data[data['trade_date']==date] #Only data for the current date
            if open_trade == True:   #Indicate entry opportunity
               

                entry = self.entry(daily_data)
                
                if entry.empty == False:
                    open_trade = False     
                    row = self.extract_row(entry,generator,data)
                    if row is not None:
                        row_list.append(row)
            else:
              
                if acum >= frec :
                    open_trade = True
                    #If the frecuency is reach, we open the trade to start looking for the next entry date.
                    acum=1
                    #Reset the dates

        df = pd.DataFrame(row_list,columns = ['trade_date','expire_date','shares_pnl','options_pnl','strategy_pnl','strike','initial_stkPx','final_stkPx'])
    
        self.stats_and_plot(df)
    
    def entry(self,data):
            
        data['%OTM'] =  ((data['strike'] * 100)/data['stkPx'] ) - 100 #Convert price to %OTM

        data['condition'] = np.where((data['yte'].between(duration, duration+0.011)) & (data['%OTM'].between(OTM_low,OTM_high) ),True,False)
        true_values = data[data['condition']==True]
        best_choice = true_values.iloc[(true_values['%OTM']-OTM).abs().argsort()[:1]]
        return best_choice

    def buy_share(self):
        n = 0
        while True:
            yield rule_number*n
            n += 1

    def stats_and_plot(self,dataFrame):
            
        df = dataFrame
        
        df['cumsum_strategy']= df['strategy_pnl'].cumsum()
        df['cumsum_option']= df['options_pnl'].cumsum()
        df['cumsum_stock']= df['shares_pnl'].cumsum()

        df = df.set_index('trade_date')
        print(df[['expire_date','shares_pnl','options_pnl','strategy_pnl']])

        std = df['strategy_pnl'].std()
        mean = df['strategy_pnl'].mean()
        sharpe_ratio = mean/std

        win_loss = pd.DataFrame(np.where(df['strategy_pnl']>=0,1,0))
        win_ratio = (win_loss.sum()*100)/win_loss.count()
        loss_ratio = 100-win_ratio
        comisions = len(df.index) * exchange_comisions
        profit = df['cumsum_strategy'].iloc[-1] 
        stocks_profit = df['cumsum_stock'].iloc[-1]
        option_profit = df['cumsum_option'].iloc[-1]
        total_profit = profit -  comisions
        
    
        print('\nBacktest results of {tick} from {start} to {end}'.format(tick=ticker_,start=start_date,end=end_date),
              'Strategy: {s}'.format(s = self.name),
              'Numbers of trade: {trades}.'.format(trades = len(df.index)),
              'Total profit: {profit} $.'.format(profit = round(total_profit)),
              'Options profit: {op} $.'.format(op=round(option_profit,2)),
              'Stock profit : {sp} $.'.format(sp=round(stocks_profit,2)),
              'Percent of WIN : {w}% '.format(w = int(win_ratio)),
              'Percent of LOSS : {l}% '.format(l = int(loss_ratio)),
              'Mean: {mean} $.'.format(mean = round(mean,2)),
              'Standard deviation : {std} $.'.format(std = round(std,2)),
              'Sharpe ratio: {sr} .'.format(sr = round(sharpe_ratio,2)),
              'Comision rate : {c}.'.format(c = comisions),
              sep='\n\n')
      
        plt.plot(df.index,df['cumsum_strategy'] )
        plt.gcf().autofmt_xdate()
        plt.title('Accounting Curve')
        plt.ylabel('Profit')
        plt.xlabel('Date')
        plt.show()

    def pnl(self,initial_stkPx,final_stkPx,strike,shares,options,trade_date,expire_date,premiun,positive_rule,negative_rule):
        """Profit & Loss method, calculate the stats of the backtest. Rules must be strategy specific.
        :param initial_stkPx: Initial price of stock on the trade date. 
        :type initial_stkPx: int.

        :param final_stkPx: Final price of stock on the expiration date.
        :type final_stkPx: int.

        :param strike: strike price of the option on the trade date.
        :type final_stkPx: int.

        :param shares: Shares owned for a specific stock.
        :type shares: int.

        :param options: Options to buy , is calculated in proportion of the shares.
        :type options: int.

        :param trade_date: Trade date of the option.
        :type trade_date: date.

        :param expire_date: expiration date of the option.
        :type trade_date: date.

        :param positive_rule: Specific function to calculate what to do in case  final_stkPx is greater than strike
        :type positive_rule: int
        
        :param negative_rule: Specific function to calculate what to do in case final_stkPx is less than strike.

        """
        
        shares_pnl = (final_stkPx-initial_stkPx) * shares

        options_pnl = np.where(final_stkPx >= strike,positive_rule(strike,initial_stkPx,final_stkPx,premiun,options,shares),negative_rule(strike,initial_stkPx,final_stkPx,premiun,options,shares) )
        
        strategy_pnl = shares_pnl + options_pnl

        dict_round = {
            'shares_pnl':shares_pnl,
            'options_pnl':np.round(options_pnl,2),
            'strategy_pnl':strategy_pnl,
            'strike':strike,
            'trade_date':trade_date,
            'expire_date':expire_date,
            'initial_stkPx':initial_stkPx,
            'final_stkPx':final_stkPx
        } 

        return dict_round

    def positive_rule(self):
        pass

    def negative_rule(self):
        pass

    def extract_row(self,entry,generator,data):   
        
        selected_option = entry.iloc[0] 
        #Select the first option, this can be improve to match exactly the parameters (Optimize)
        stk_price1 = selected_option['stkPx']
        strike_price = selected_option['strike']
        expire_date = selected_option['expirDate']
        trade_date = selected_option['trade_date']
        if fill_price == 'Bid':
            option_premiun = selected_option['cBidPx']
        elif fill_price == 'Ask':
            option_premiun = selected_option['cBidPx']
        #depends on the strategy bid or ask for premiun 
                   
        share_trade =shares + next(generator)
        #Buy Shares
        option_trade = self.option_trade(positionPercent,share_trade)   
        #Sell Call
                    
                    
        df_final_price = data[(data['trade_date'] >= expire_date)]         
        # We look into the dataFrame the price when the trade date is equal Or bigger than trade_date       

        if df_final_price.empty == False:   

            final_price = df_final_price['stkPx'].iloc[0]   
            #Now that we the prices we take de 0 position (it doesn´t matter order)

            row = self.pnl(stk_price1,final_price,strike_price,share_trade,option_trade,trade_date,expire_date,option_premiun,self.positive_rule,self.negative_rule) 
            return row   

    def option_trade(self,postionPercent,shares_calc):
            calls = (positionPercent*100)/shares_calc
            return calls

import pandas as pd 
import numpy as np 
from config import config

frecuency = config['frecuency']
OTM_high = config['%OTM'] + 1
OTM_low = config['%OTM'] - 1
pd.options.mode.chained_assignment = None



class CoveredCall():
    """
    Abstract base class for strategies.
    """
    def update(self, data):
        inside = False

        if next_desired_expiration_date == True:
            print(self.entry(data))
               
    
    def entry(self,data):
        
        data['%OTM'] =  ((data['strike'] * 100)/data['stkPx'] ) - 100

        data['condition'] = np.where((data['yte'].between(0.08, 0.08219)) & (data['%OTM'].between(OTM_low,OTM_high) ),True,False)
        
        data1 = data[data['condition']==True]
        if data1.empty :
            inside = False
        else : 
            inside = True 
    
        return inside

    def buy(self,data):
        pass
    def sell(self,data):
        pass
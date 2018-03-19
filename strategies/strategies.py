import pandas as pd 
import numpy as np 
from config import config
from strategies.baseStrategy import BaseStrategy

import matplotlib.pyplot as plt #Style config for plots
import seaborn as sns
sns.set()
sns.axes_style('darkgrid')





positionPercent = config['%ofPosition']




class CoveredCall(BaseStrategy):
    """
    Covered call strategy.
    """
    def __init__(self):
        super().__init__()
        name = 'Covered Call '
        setattr(self,'name',name)

    def positive_rule(self,strike_price,initial_price,final_price,premiun,options,shares):
        result = (-(final_price - strike_price ) + premiun) * 100 * options
        return result

    def negative_rule(self,strike_price,initial_price,final_price,premiun,options,shares):
        result = premiun *100 * options
        return result




class ProtectivePut(BaseStrategy):
    """
    ProtectivePut strategy class
    """
    def __init__(self):
        super().__init__()
        name = 'Protective Put'
        setattr(self,'name',name)
    
    def positive_rule(self,strike_price,initial_price,final_price,premiun,options,shares):
        
        result = - (premiun)*shares
        return result 


    def negative_rule(self,strike_price,initial_price,final_price,premiun,options,shares):
        
        loss = (premiun)*shares + (strike_price - final_price)*shares
        return loss


if __name__ == '__main__':
    main()
    
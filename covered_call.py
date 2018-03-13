# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:22:15 2018

@author: paulj
"""
import numpy as np
from matplotlib import pyplot as plt


def covered_call(stock_quantity, strike_price, initial_price, 
                 final_price,  premium=0.15):
    price_diff = final_price - initial_price
    stock_pnl = price_diff * stock_quantity
#    print(stock_pnl)
    
    if final_price >= strike_price:
        options_diff = final_price - strike_price
        option_pnl = -options_diff * stock_quantity + premium * stock_quantity
    elif final_price < strike_price:
        option_pnl = premium * stock_quantity
#    print(option_pnl)
        
    pnl = stock_pnl + option_pnl
    print(pnl)
    return pnl

if __name__ == "__main__":
    stock_quantity = 1000
    strike_price = 125
    initial_price = 120
    final_price = np.linspace(100, 150)
    
    pnl = []
    for p in final_price:
        pnl.append(covered_call(stock_quantity, strike_price, 
                                initial_price, final_price=p))
        
    plt.figure(figsize=(10, 7))
    plt.scatter(final_price, pnl)
    plt.title("Covered call")
    plt.show()

    
    
    
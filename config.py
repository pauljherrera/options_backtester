import datetime as dt
config = {
    # General config.
    'start_date': '2018-03-16',
    'end_date': '2018-03-19',
    'api_key' : "7MA978mgAH8cTzL7CGa_",

    # Strategy config.
    'ticker': 'GOOGL',
    'strategy':'Protective Put',
    'fillPrice':'Bid', #Bid or Ask
    'premiun' : 0.5,
    '%OTM' : 2,
    'frecuency' : 30, #Expresed in days
    'duration' : 30, #Expresed in years
    'initial_position':1000,
    '%ofPosition':100,
    'exchange_comisions':1,
    'buy/sell stock':0 #Number of stocks bought for every trade
}



import datetime as dt
config = {
    # General config.
    'start_date': '2013-01-01',
    'end_date': '2018-02-31',
    'api_key' : "insertQuandlApiKey",

    # Strategy config.
    'ticker': 'GOOGL',
    'strategy':'Protective Put',
    'premiun' : 0.5,
    '%OTM' : -2,
    'frecuency' : 30, #Expresed in days
    'duration' : 0.08, #Expresed in years
    'initial_position':1000,
    '%ofPosition':100,
    'exchange_comisions':1,
    'buy/sell stock':0 #Number of stocks buyed for every trade
}



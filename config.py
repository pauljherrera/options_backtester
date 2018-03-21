import datetime as dt
config = {
    # General config.
<<<<<<< HEAD
    'start_date': '2015-01-01',
    'end_date': '2018-03-15',
    'api_key' : "7MA978mgAH8cTzL7CGa_",
=======
    'start_date': '2018-03-16',
    'end_date': '2018-03-19',
    'api_key' : "insertQuandlApiKey",
>>>>>>> eca72d90ff61c17324b98ab09ec48f476f38085d

    # Strategy config.
    'ticker': 'MRK',
    'strategy':'Protective Put',
    'fillPrice':'Bid', #Bid or Ask
    'premiun' : 0.5,
    '%OTM' : 2,
    'frecuency' : 30, #Expresed in days
    'duration' : 30, #Expresed in days
    'initial_position':1000,
    '%ofPosition':100,
    'exchange_comisions':1,
    'buy/sell stock': 0 #Number of stocks bought for every trade
}



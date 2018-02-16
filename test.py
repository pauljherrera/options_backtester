# -*- coding: utf-8 -*-
import quandl
import pandas as pd 
quandl.ApiConfig.api_key = "7MA978mgAH8cTzL7CGa_"
quandl.ApiConfig.page_limit=300

database_name = 'OSMV'
db = quandl.Database('OSMV')

counter = 1
full_list = []

flag = True
while flag:
    all_db = db.all(params={'page': 2 })


def load_data():
    return pd.read_csv('data/OSMV.csv')

df = load_data()

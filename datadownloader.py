import requests
from tqdm import tqdm
import zipfile
import os
from datetime import datetime, timedelta
from google.cloud import storage

from config import config

api_key = config['api_key']



class DataDownloader(object):
    """ Class to handle downloads from quandl
    """
    def __init__(self,*args,**kwargs):
        pass

    def __download(self,date):
        """This function downlad the data directly from quandl
        :param date: Trade Date of the data we want
        :type date: str
        """
        payload = {
    'download_type': date,
    'api_key' :  api_key         #Development mode.
    }
        r = requests.get("https://www.quandl.com/api/v3/databases/OSMV/download?",stream=True, params=payload,timeout=120)   
        total = int(r.headers.get('content-length'))
        with open("file.zip", "wb") as handle:
            for data in tqdm(r.iter_content(), total = total):
                handle.write(data)


        with zipfile.ZipFile("file.zip","r") as zip_ref:
            zip_ref.extractall("Historical Data")

    def missing_dates(self,missing_dates):
        """Function to download data acordding to days missing
        :param missing_dates: List with the missing days 
        :type missin_dates: List
        """
        for date in tqdm(missing_dates):
            try:
                self.__download(date)
                msg = date + " Finished download"
                tqdm.write(msg)
            except ConnectionError as identifier:
                print(indentifier)
                
    def daily_update(self):
        """Function to update Google Cloud Storage daily with data from Quandl (ORMSV options)
        """
        date = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d') 
        #Get yesterday date to download data. This method should run everyday.

        self.__download(date)
        
        client = storage.Client.from_service_account_json(
        'Harvested Backtest Framework-c01b8a37c1fb.json')
        
        bucket = client.get_bucket('1avanti_options')
        path_file = 'Historical Data/OSMV-' + date + '.csv'
        file_name = 'OSMV-'+date+'.csv'
        
        blob = bucket.blob(path_file)
        blob.upload_from_filename(path_file)


        

        
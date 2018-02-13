import requests
from tqdm import tqdm
import zipfile
import os
from config import config

api_key = config['api_key']



class DataDownloader(object):
    """ Class to handle downloads from quandl
    """
    def __init__(self,*args,**kwargs):
        pass

    def download(self,date):
        """This function downlad the data directly from quandl
        :param date: Trade Date of the data we want
        :type date: str
        """
        payload = {
    'download_type': date,
    'api_key' :  api_key         #Development mode.
    }
        r = requests.get("https://www.quandl.com/api/v3/databases/OSMV/download?",stream=True, params=payload,timeout=120)   

        with open("file.zip", "wb") as handle:
            for data in tqdm(r.iter_content()):
                handle.write(data)


        with zipfile.ZipFile("file.zip","r") as zip_ref:
            zip_ref.extractall("Historical Data")

    def download_missing_dates(self,missing_dates):
        """Function to download data acordding to days missing
        :param missing_dates: List with the missing days 
        :type missin_dates: List
        """
        for date in tqdm(missing_dates):
            try:
                self.download(date)
                msg = date + " Finished download"
                tqdm.write(msg)
            except ConnectionError as identifier:
                print(indentifier)
                
            
        

        
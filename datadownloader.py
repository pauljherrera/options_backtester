import requests
from tqdm import tqdm
import zipfile
import os
from datetime import datetime, timedelta
from google.cloud import storage, bigquery
from google.cloud.bigquery import Dataset
import multiprocessing.pool as mpool
import threading
import time
from config import config

api_key = config['api_key']



class DataDownloader(object):
    """ Class to handle downloads from quandl
    """
    def __init__(self,*args,**kwargs):
        self.client = bigquery.Client.from_service_account_json(
        'Harvested Backtest Framework-c01b8a37c1fb.json')
        self.SCHEMA = [
            bigquery.SchemaField('ticker', 'STRING', mode='NULLABLE'),
            bigquery.SchemaField('stkPx', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('expirDate', 'DATE', mode='NULLABLE'),
            bigquery.SchemaField('yte', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('strike', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('cVolu', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('cOi', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('pVolu', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('pOi', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('cBidPx', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('cValue', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('cAskPx', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('pBidPx', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('pValue', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('pAskPx', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('cBidIv', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('cMidIv', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('cAskIv', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('smoothSmvVol', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('pBidIv', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('pMidIv', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('pAskIv', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('iRate', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('divRate', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('residualRateData', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('delta', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('gamma', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('theta', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('vega', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('rho', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('phi', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('driftlessTheta', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('extVol', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('extCTheo', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('extPTheo', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('spot_px', 'STRING', mode='NULLABLE'),
            bigquery.SchemaField('trade_date', 'DATE', mode='NULLABLE'),


            ]
    def __download(self,date):
        """This function downlad the data directly from quandl
        :param date: Trade Date of the data we want
        :type date: str
        """
        payload = {
    'download_type': date,
    'api_key' :  api_key         #Development mode.
                 }
        try:
                r = requests.get("https://www.quandl.com/api/v3/databases/OSMV/download?",stream=True, params=payload,timeout=200)   
                total = int(r.headers.get('content-length'))
                with open("file.zip", "wb") as handle:
                    for data in r.iter_content(1024*5):
                        handle.write(data)


                with zipfile.ZipFile("file.zip","r") as zip_ref:
                    zip_ref.extractall("Historical Data")
                result = True
        except Exception as identifier:
            result = False
        return result
       
    def missing_dates(self,missing_dates):
        """Function to download data acordding to days missing
        :param missing_dates: List with the missing days 
        :type missin_dates: List
        """
        for date in tqdm(missing_dates):
            try:
                correct = self.__download(date)
                if correct == True:
                    
                    msg = date + " Finished download"
                    tqdm.write(msg)
                else:
                    msg = date + " download Failed"
                    tqdm.write(msg)
            except ConnectionError as identifier:
                print(indentifier)
                
    def daily_update(self):
        """Function to update Google Cloud Storage daily with data from Quandl (ORMSV options)
        """
        date = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d') 
        #Get yesterday date to download data. This method should run everyday.

        self.__download(date)
        

        
        bucket = self.client.get_bucket('1avanti_options')
        path_file = 'Historical Data/OSMV-' + date + '.csv'
        file_name = 'OSMV-'+date+'.csv'
        
        blob = bucket.blob(path_file)
        blob.upload_from_filename(path_file)

    
        
    def load_data_from_file(self,dataset_id,table_id, source_file_name):
        
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        with open(source_file_name, 'rb') as source_file:
            # This example uses CSV, but you can use other formats.
            job_config = bigquery.LoadJobConfig()
            job_config.schema = self.SCHEMA
            job_config.source_format = 'CSV'
            job_config.skip_leading_rows = 1
            job = self.client.load_table_from_file(
                source_file, table_ref, job_config=job_config)

        #job.result()  # Waits for job to complete

        print('Loaded {} rows into {}:{}.'.format(
            job.output_rows, dataset_id, table_id))

    def __create_dataset(self,data_set,data_set_description):
        dataset_ref = self.client.dataset(data_set)
        dataset = Dataset(dataset_ref)
        dataset.description = data_set_description
        dataset = self.client.create_dataset(dataset)  # API request

    def create_table(self):
        """Private method to create a table in a specific DataSet of BigQuery.  It should be used once.
        """
        
        #Schema of the data
        dataset = self.client.dataset('Options_backtester')  #Specific DataSet ID, it can be found on GBQ Dashboard
        table_ref = dataset.table('OSMV_TABLES') #Specific 
        table = bigquery.Table(table_ref, schema=self.SCHEMA)
        table = self.client.create_table(table)      # API request

    def load_multiple_files(self,dataset,table):

        files = os.listdir('Historical Data')
        for file in tqdm(files) :
            path_to_file = 'Historical Data/' + file
            
            self.load_data_from_file(dataset_id = dataset , table_id = table,source_file_name = path_to_file)
        
        
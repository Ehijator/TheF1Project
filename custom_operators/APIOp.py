import requests 
import pandas as pd
import airflow
import time
from airflow.sdk import dag, task, BaseOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import datetime

## Returns dataframes from selected api endpoints
class F1APIOperator(BaseOperator):
    url = 'https://api.openf1.org/v1/' 

    def __init__(self,start_date,end_date,**kwargs) -> None:
        super().__init__(**kwargs)
        self.start_date = start_date
        self.end_date = end_date
    
    # possible url keys = [sessions]
    def _DateStartToDateEndFilter(self,url_key:str='sessions'):
        url_tag = url_key + '?'
        date = F1APIOperator.url + url_tag + 'date_start' + '>=' + self.start_date + '&' + 'date_end' + '<=' + self.end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        try :
            return df
        except requests.exceptions.RequestException as e:
            raise SystemExit
        
    # possible url keys = [race_control, overtakes, position, weather]
    def _DateFilter(self,url_key:str): 
        url_tag = url_key + '?'
        date = F1APIOperator.url + url_tag + 'date' + '>=' + self.start_date + '&' + 'date' + '<=' + self.end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        try :
            return df
        except requests.exceptions.RequestException as e:
            raise SystemExit

    # possible url keys = [session_result, pit, drivers, stints]
    def _SessionKeyLoop(self,url_key:str): # session_result, pit, drivers, stints 
        url_tag = url_key + '?'
        sessionsdf = F1APIOperator(self.start_date,self.end_date).DateStartToDateEndFilter()
        sessionkeys = (sessionsdf["session_key"].unique())
        data = pd.DataFrame()
        for key in sessionkeys:
            time.sleep(1)
            x = requests.get(F1APIOperator.url + url_tag + 'session_key=' + str(key)).json()
            stage = pd.json_normalize(x)
            data = pd.concat([data,stage],ignore_index=True)
        try :
            return data
        except requests.exceptions.RequestException as e:
            raise SystemExit

    # possible url keys = [laps]
    def _DateStartToDateStart(self,url_key:str ='laps'): 
        url_tag = url_key + '?'
        date = F1APIOperator.url + url_tag + 'date_start' + '>=' + self.start_date + '&' + 'date_start' + '<=' + self.end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        try :
            return df
        except requests.exceptions.RequestException as e:
            raise SystemExit

    def execute(self,context):
        
date = F1APIOperator('2025-01-01','2025-12-31')
  
        
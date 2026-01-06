import requests 
import pandas as pd
import airflow
from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import datetime

## will refactor into a custom operator

@dag(
    dag_id='create_required_tables',
    start_date=datetime(2026,1,1),
    schedule=None,
    tags=['One-time']
)

def StagingTables():
    create_tabs = SQLExecuteQueryOperator(
        task_id = 'create_staging_tables',
        conn_id = 'postgres_localhost',
        sql = 'Sql/Staging_table_create.sql')

## Returns dataframes from selected api endpoints
class F1API:
    url = 'https://api.openf1.org/v1/' 

    def __init__(self,start_date,end_date):
        self.start_date = start_date
        self.end_date = end_date
    
    # returns session data as dataframe
    def sessionsdf(self):
        url_tag = 'sessions?'
        date = F1API.url + url_tag + 'date_start' + '>=' + self.start_date + '&' + 'date_end' + '<=' + self.end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        return df
        
    # takes in url key returns data as dataframe
    # possible url keys = [race_control, overtakes, position, weather]
    def date_filter(self,url_key): 
        url_tag = url_key + '?'
        date = F1API.url + url_tag + 'date' + '>=' + self.start_date + '&' + 'date' + '<=' + self.end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        return df

    # takes in url key returns data as dataframe
    # possible url keys = [session_result, pit, drivers, stints]
    def session_loop(self,url_key): # session_result, pit, drivers, stints 
        url_tag = url_key + '?'
        sessionsdf = F1API(self.start_date,self.end_date).sessionsdf()
        sessionkeys = (sessionsdf["session_key"].unique())
        #print(sessionkeys)
        data = pd.DataFrame()
        for key in sessionkeys:
            x = requests.get(F1API.url + url_tag + 'session_key=' + str(key)).json()
            stage = pd.json_normalize(x)
            data = pd.concat([data,stage],ignore_index=True)
        return data 

    #return laps data as dataframe
    def lapsdf(self,url_key): # laps 
        url_tag = url_key + '?'
        date = F1API.url + url_tag + 'date_start' + '>=' + self.start_date + '&' + 'date_start' + '<=' + self.end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        return df

#session = F1API('2025-01-01','2025-12-31').lapsdf('laps')
#print(F1API('2025-01-01','2025-05-31').session_loop('session_result'))   
        








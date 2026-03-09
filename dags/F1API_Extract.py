from airflow.sdk import dag, task, BaseOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import datetime

## will refactor into a custom operator

@dag(
    dag_id='back_date_load',
    start_date=datetime(2026,1,1),
    schedule=None,
    tags=['One-time']
)

## Returns dataframes from selected api endpoints

def F1Data(start_date,end_date):
    import requests 
    import pandas as pd
    import airflow
    import time
    url = 'https://api.openf1.org/v1/' 

    @task() # possible url keys = [sessions]
    def DateStartToDateEndFilter(url_key:str='sessions'):
        url_tag = url_key + '?'
        date = url + url_tag + 'date_start' + '>=' + start_date + '&' + 'date_end' + '<=' + end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        return df

        
    @task() # possible url keys = [race_control, overtakes, position, weather]
    def DateFilter(url_key:str): 
        url_tag = url_key + '?'
        date = url + url_tag + 'date' + '>=' + start_date + '&' + 'date' + '<=' + end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        return df


    @task() # possible url keys = [session_result, pit, drivers, stints]
    def SessionKeyLoop(url_key:str): # session_result, pit, drivers, stints 
        url_tag = url_key + '?'
        sessionsdf = DateStartToDateEndFilter()
        sessionkeys = (sessionsdf["session_key"].unique())
        data = pd.DataFrame()
        for key in sessionkeys:
            time.sleep(1)
            x = requests.get(url + url_tag + 'session_key=' + str(key)).json()
            stage = pd.json_normalize(x)
            data = pd.concat([data,stage],ignore_index=True)
        return data

    @task() # possible url keys = [laps]
    def DateStartToDateStart(url_key:str ='laps'): 
        url_tag = url_key + '?'
        date = url + url_tag + 'date_start' + '>=' + start_date + '&' + 'date_start' + '<=' + end_date 
        response = requests.get(date)
        json = response.json()
        df = pd.json_normalize(json)
        return df
    
    
    DateStartToDateEndFilter('sessions').to_csv('CSVs/sessions.csv',mode='w+')
    
    pghook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = pghook.getconn()
    cur = conn.cursor()
    with open('CSVs/sessions.csv', 'r') as file:
        cur.copy_expert(
            "COPY postgres FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
            file,
        )
    conn.commit()
    # time.sleep(2)
    # print(DateFilter('race_control'))
    # time.sleep(2)
    # print(DateFilter('overtakes'))
    # time.sleep(2)
    # print(DateFilter('position'))
    # time.sleep(2)
    # print(DateFilter('weather'))
    # time.sleep(2)
    # print(SessionKeyLoop('session_result'))
    # time.sleep(2)
    # print(SessionKeyLoop('pit'))
    # time.sleep(2)
    # print(SessionKeyLoop('drivers'))
    # time.sleep(2)
    # print(SessionKeyLoop('stints'))

F1Data('2025-01-01','2025-12-31')
#date.DateStartToDateEndFilter('sessions').to_sql() > time.sleep(1) > date.DateFilter('race_control')> time.sleep(1) > date.DateFilter('overtakes')> time.sleep(1)> date.DateFilter('position')> time.sleep(1)> date.DateFilter('weather')> time.sleep(1)> date.SessionKeyLoop('session_result')> time.sleep(1)> date.SessionKeyLoop('pit')> time.sleep(1)> date.SessionKeyLoop('drivers')> time.sleep(1)> date.SessionKeyLoop('stints')> time.sleep(1)> date.DateStartToDateStart('laps')
  








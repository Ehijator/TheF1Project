from airflow.sdk import dag, task
#from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

#potentially will be main dag for ETL

@dag(
    dag_id='create_required_tables',
    start_date= datetime(2026,1,1),
    schedule=None,
    tags=['One-time']
)

def StagingTables():
    create_tabs = SQLExecuteQueryOperator(
        task_id = 'create_staging_tables',
        conn_id = 'postgres_localhost',
        database = 'postgres',
        sql = 'Sql/Staging_table_create.sql'
            )
    
def Maintables():
    create_tabs = SQLExecuteQueryOperator(
        task_id = 'create_main_tables',
        conn_id = 'postgres_localhost',
        database = 'F1_Prod',
        sql = 'Sql/Main_table_create.sql'
    )

[StagingTables(), Maintables()]
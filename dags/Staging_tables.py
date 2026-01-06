from airflow.sdk import dag, task
#from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import datetime

#potentially will be main dag for ETL

@dag(
    dag_id='create_required_tables',
    start_date=datetime.datetime(2026,1,1),
    schedule=None,
    tags=['One-time']
)


def StagingTables():
    create_tabs = SQLExecuteQueryOperator(
        task_id = 'create_staging_tables',
        conn_id = 'postgres_localhost',
        sql = 'Sql/Staging_table_create.sql'
            )

StagingTables()
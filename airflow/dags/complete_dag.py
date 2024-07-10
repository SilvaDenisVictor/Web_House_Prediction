from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    'controle_dag',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False,
) as dag:
    
    wait_for_extraction = ExternalTaskSensor(
        task_id='wait_for_extraction',
        external_dag_id='web_scraping',
        mode='poke',
        timeout=600,
    )
    
    trigger_train_model = TriggerDagRunOperator(
        task_id='trigger_train_model ',
        trigger_dag_id='train_model',
    )
    
    wait_for_extraction >> trigger_train_model
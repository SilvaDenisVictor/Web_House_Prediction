from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.trigger_rule import TriggerRule

import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'web_scraping',
    default_args=default_args,
    description='Extracting data from the site',
    start_date=datetime(2024, 7, 3),
    schedule_interval= '59 15 * * *',
    catchup=False
)

start_selenium = BashOperator(
    task_id = 'start_selenium',
    bash_command= 'docker run --rm -d -p 4444:4444 --shm-size 2g --name selenium_service --network web_house_prediction_project_net selenium/standalone-chromium:latest',
    dag=dag,
)

build_image = BashOperator(
    task_id='build_data_extraction_image',
    bash_command='docker build -t data_extraction:latest /opt/data_extraction',
    dag=dag,
)

full_path_mount = 'C:\\Users\\Denis\\Documents\\GitHub\\Web_House_Prediction\\data_extraction'

execute_script = DockerOperator(
    task_id='run_script',
    image='data_extraction:latest',
    container_name = 'data_extraction',
    docker_url='unix://var/run/docker.sock',
    mounts=[Mount(source=full_path_mount, target='/app', type='bind', propagation='rshared', consistency='consistent')],
    network_mode="web_house_prediction_project_net",
    #auto_remove=True,
    dag=dag,
)

cleanup_selenium = BashOperator(
    task_id='cleanup_selenium',
    bash_command='docker rm -f selenium_service',
    trigger_rule=TriggerRule.ALL_DONE,
    dag=dag,
)

start_selenium >> build_image >> execute_script >> cleanup_selenium

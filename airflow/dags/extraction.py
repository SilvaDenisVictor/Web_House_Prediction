import datetime 
from airflow import DAG
from docker.types import Mount

from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.dagrun_operator import TriggerDagRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    'web_scraping',
    default_args= default_args,
    description= 'Extracting data from the site',
    start_date= datetime.datetime(2022, 1, 1, 19, 0),
    end_date= datetime.datetime(2025, 1, 1, 0, 0),
    schedule= "50 18 * * *",
    catchup= False
) as dag:
    
    close_api_server = BashOperator(
        task_id='close_api_server',
        bash_command='docker rm -f api_server',
        dag=dag,
    )

    start_selenium = BashOperator(
        task_id = 'start_selenium',
        bash_command= 'docker run --rm -d -p 4444:4444 --shm-size 2g --name selenium_service --network web_house_prediction_project_net selenium/standalone-chromium:latest',
        dag=dag,
    )

    build_image_extraction = BashOperator(
        task_id='build_data_extraction_image',
        bash_command='docker build -t data_extraction:latest /opt/data_extraction',
        dag=dag,
    )

    full_path_data_extraction = 'C:\\Users\\Denis\\Documents\\GitHub\\Web_House_Prediction\\data_extraction'


    execute_script = DockerOperator(
        task_id='run_script',
        image='data_extraction:latest',
        container_name = 'data_extraction',
        docker_url='unix://var/run/docker.sock',
        mounts=[Mount(source=full_path_data_extraction, target='/app', type='bind', propagation='rshared', consistency='consistent')],
        network_mode="web_house_prediction_project_net",
        auto_remove=True,
        dag=dag,
    )

    cleanup_selenium = BashOperator(
        task_id='cleanup_selenium',
        bash_command='docker rm -f selenium_service',
        trigger_rule=TriggerRule.ALL_DONE,
        dag=dag,
    )

    trigger_train_model = TriggerDagRunOperator(
        task_id='trigger_train_model',
        trigger_dag_id='train_model',
    )

    close_api_server >> start_selenium >> build_image_extraction >> execute_script >> cleanup_selenium >> trigger_train_model


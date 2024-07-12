import datetime
from airflow import DAG
from docker.types import Mount

from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

full_path_models = 'C:\\Users\\Denis\\Documents\\GitHub\\Web_House_Prediction\\models'
full_path_pre_processing = 'C:\\Users\\Denis\\Documents\\GitHub\\Web_House_Prediction\\pre_processing'

dic_path = 'C:/Users/Denis/Documents/GitHub/Web_House_Prediction/models/dict.cloudpickle:/app/dict.cloudpickle'
model_path = 'C:/Users/Denis/Documents/GitHub/Web_House_Prediction/models/model.cloudpickle:/app/model.cloudpickle'
best_model_path = 'C:/Users/Denis/Documents/GitHub/Web_House_Prediction/models/best_model.keras:/app/best_model.keras'
deep_model_path = 'C:/Users/Denis/Documents/GitHub/Web_House_Prediction/models/deep_model.py:/app/deep_model.py'
regression_model_path = 'C:/Users/Denis/Documents/GitHub/Web_House_Prediction/models\/regression_model.py:/app/regression_model.py'

with DAG(
    'train_model',
    default_args=default_args,
    description='Training the model with new data',
    start_date= datetime.datetime(2022, 1, 1, 19, 0),
    schedule= None,
    catchup=False
) as dag:

    close_api_server = BashOperator(
        task_id='close_api_server',
        bash_command='docker rm -f api_server',
        dag=dag,
    )

    build_image_train = BashOperator(
        task_id='build_train_image',
        bash_command='docker build -t model:latest /opt/models',
        dag=dag,
    )

    train_model = DockerOperator(
        task_id='train_model',
        image='model:latest',
        container_name = 'model',
        docker_url='unix://var/run/docker.sock',
        mounts=[
            Mount(source=full_path_models, target='/app/models', type='bind', propagation='rshared', consistency='consistent'),
            Mount(source=full_path_pre_processing, target='/app/pre_processing', type='bind', propagation='rshared', consistency='consistent')
            ],
        network_mode="web_house_prediction_project_net",
        auto_remove=True,
        dag=dag,
    )

    build_image_api_server = BashOperator(
        task_id='build_image_api_server',
        bash_command='docker build -t api_server:latest /opt/api_server',
        dag=dag,
    )

    start_api_server = BashOperator(
        task_id = 'start_api_server',
        bash_command= f'docker run -d -p 2020:2020 --name api_server --network web_house_prediction_project_net -v {dic_path} -v {model_path} -v {best_model_path} -v {deep_model_path} -v {regression_model_path}  api_server:latest',
        dag=dag,
    )

    close_api_server >> build_image_train >> train_model >> build_image_api_server >> start_api_server

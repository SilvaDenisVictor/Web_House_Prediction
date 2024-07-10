from fastapi import FastAPI
import uvicorn
import pandas as pd
import subprocess

from deep_model import get_saved_model as dm_saved, predict as dm_predict
from regression_model import get_saved_model as rm_saved, predict as rm_predict
import cloudpickle 


app = FastAPI()

@app.get('/')
def home():
    return {'function': 'Welcome'}

@app.get('/predict_regression')
def predict_regression(condominio:int, metro_quadrado:float, quarto:int, banheiro:int, garagem:int, regiao:int, vendedor:int) -> dict:
    #dic = joblib.load(open('/app/models/dict.pkl', 'rb'))
    result = subprocess.run(
            ["pip", "show", 'joblib'],
            capture_output=True,
            text=True,
            check=True
        )
    # Imprime a saída do comando
    print(result.stdout)

    regression_model = rm_saved()

    json = {
        'condominio': condominio,
        'metro_quadrado': metro_quadrado, 
        'quarto': quarto, 
        'banheiro': banheiro, 
        'garagem': garagem, 
        'regiao': regiao, 
        'com_profissional': int(vendedor == 1),
        'com_dono': int(vendedor == 0)
    }
    print('CHEGAMOS AQUI RAPAZ')
    print('CHEGAMOS AQUI RAPAZ')
    print('CHEGAMOS AQUI RAPAZ')
    print('CHEGAMOS AQUI RAPAZ')

    preco = rm_predict(regression_model, pd.DataFrame([json]))


    # /predict_deep?condominio=0&metro_quadrado=245.3&quarto=2&banheiro=1&garagem=1&regiao=1&vendedor=0
    response = {
        'function': 'regression_model',
        'preco': float(preco)
    }

    return response

@app.get('/predict_deep')
def predict_deep(condominio:float, metro_quadrado:float, quarto:int, banheiro:int, garagem:int, regiao:int, vendedor:int) -> dict:
    #dic = joblib.load(open('/app/models/dict.pkl', 'rb'))
    deep_model = dm_saved()

    json = {
        'condominio': condominio,
        'metro_quadrado': metro_quadrado, 
        'quarto': quarto, 
        'banheiro': banheiro, 
        'garagem': garagem, 
        'regiao': regiao, 
        'com_profissional': int(vendedor == 1),
        'com_dono': int(vendedor == 0)
    }
    #docker run -d -p 2020:2020 --name api_server --network web_house_prediction_project_net -v .\models\regression_model.py:/app/regression_model.py -v .\models\deep_model.py:/app/deep_model.py -v .\models\best_model.keras:/app/best_model.keras -v .\models\model.cloudpickle:/app/model.cloudpickle -v .\models\dict.cloudpickle:/app/dict.cloudpickle api_server:latest
    #-v .\models\dict.cloudpickle:/app/dict.cloudpickle
    #-v .\models\model.cloudpickle:/app/model.cloudpickle
    #-v .\models\deep_model.py:/app/deep_model.py
    #-v .\models\regression_model.py:/app/regression_model.py
    preco = dm_predict(deep_model, pd.DataFrame([json]))

    # /predict_deep?condominio=0&metro_quadrado=245.3&quarto=2&banheiro=1&garagem=1&regiao=1&vendedor=0
    response = {
        'function': 'deep_model',
        'preco': preco
    }
    return response

if __name__ == '__main__':
     uvicorn.run(app, port=2020, host='0.0.0.0')

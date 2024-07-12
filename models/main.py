import pandas as pd
import psycopg2

import cloudpickle
import subprocess

import deep_model as dm
import regression_model as rm

from pre_processing.pre_processing import processing_data
from sklearn.model_selection import train_test_split


def build_and_train_model():
    #EXTRAINDO DADOS DO BANCO
    coon =  psycopg2.connect(host='postgres', dbname='houses_db', user='postgres', password='postgres', port=5432)
    cur = coon.cursor()

    insert = """
    select * from House;
    """

    cur.execute(insert)

    casas = cur.fetchall()

    print('Tipo: ', type(casas))
    print('Quantidade de linhas: ', len(casas))
    print('Quantidade de colunas: ', len(casas[0]))

    # csv =  pd.read_csv('data_extraction/casas.csv', sep=';')
    # print('Tamanho csv: ', csv.shape)

    #DATA PROCESSING
    df = pd.DataFrame(casas, columns=['id', 'preco', 'iptu', 'condominio', 'metro_quadrado', 'quarto', 'banheiro', 'garagem', 'regiao', 'data', 'vendedor', 'descricao'])

    X, y, X_f, y_f, dic = processing_data(df)

    #SALVANDO DICIONARIO PARA PREDICAO DE DADOS
    with open('/app/models/dict.cloudpickle','wb') as f:
        cloudpickle.dump(dic, f)

    X_train, X_test, y_train, y_test = train_test_split(X_f, y_f, test_size=0.10, random_state = 15)

    #CREATING MODELS
    deep_model = dm.create_model(dic)
    regression_model = rm.create_model(dic)

    #TRAINING MODEL
    dm.get_train_model(deep_model, X_train, y_train, 50)
    # dm.get_train_model(deep_model, X, y, 20)

    rm.get_train_model(regression_model, X_train, y_train)

    #EVALUATING MODEL
    mean_squared_error, mean_absolute_error_dm = dm.evaluate(deep_model, X_f, y_f)
    mean_absolute_error_rm = rm.evaluate(regression_model, X_f, y_f)

    mean = y_f.mean()

    metrica_deep = 100 - mean_absolute_error_dm*100/mean
    metrica_regression = 100 - mean_absolute_error_rm*100/mean

    print('Mean:', mean)
    print('Métrica deep: ', mean_absolute_error_dm, '     Acerto em porcentagem: ', metrica_deep)
    print('Métrica regression: ', mean_absolute_error_rm, '     Acerto em porcentagem: ', metrica_regression)

    json = {
        'mean_y_test': mean,
        'mean_absolute_error_dm': mean_absolute_error_dm,
        'mean_absolute_error_rm': mean_absolute_error_rm,
        'metrica_deep': metrica_deep,
        'metrica_regression': metrica_regression
    }

    return json

if __name__ == '__main__':
    result = subprocess.run(
            ["pip", "show", 'cloudpickle'],
            capture_output=True,
            text=True,
            check=True
        )
    # Imprime a saída do comando
    print(result.stdout)
    
    build_and_train_model()

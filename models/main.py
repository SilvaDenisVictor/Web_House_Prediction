import pandas as pd
import numpy as np
import psycopg2

import deep_model as dm
import regression_model as rm
from pre_processing.pre_processing import processing_data

from sklearn.model_selection import train_test_split

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

#DATA PROCESSING
df = pd.DataFrame(casas, columns=['id', 'preco', 'iptu', 'condominio', 'metro_quadrado', 'quarto', 'banheiro', 'garagem', 'regiao', 'data', 'vendedor', 'descricao'])

X, y, dic = processing_data(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state = 15)

#CREATING MODELS
degree = 1
deep_model = dm.create_model(X, degree)
regression_model = rm.create_model(X)

#TRAINING MODEL
dm.get_train_model(deep_model, X_train, y_train, degree)
rm.get_train_model(regression_model, X_train, y_train)

#EVALUATING MODEL
mean_squared_error, mean_absolute_error_dm = dm.evaluate(deep_model, X_test, y_test, degree)
mean_absolute_error_rm = rm.evaluate(regression_model, X_test, y_test)

mean = y_test.mean()
print('Mean:', mean)
print('Métrica deep: ', mean_absolute_error_dm, '     Acerto em porcentagem: ', 100 - mean_absolute_error_dm*100/mean)
print('Métrica regression: ', mean_absolute_error_rm, '     Acerto em porcentagem: ', 100 - mean_absolute_error_rm*100/mean)


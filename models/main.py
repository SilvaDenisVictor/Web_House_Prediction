import pandas as pd
import numpy as np

import deep_model as dm
import regression_model as rm
from pre_processing.pre_processing import processing_data

from sklearn.model_selection import train_test_split

#DATA PROCESSING
df = pd.read_csv('data_extraction/casas.csv', sep=';')

X, y = processing_data(df)
X['regiao'] = X['regiao'].astype('category').cat.codes

#CREATING DICT OF REGIAO


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state = 9)

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


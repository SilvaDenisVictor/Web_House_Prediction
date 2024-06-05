import pandas as pd

import models.deep_model as dm
import models.regression_model as rm
from pre_processing.pre_processing import processing_data

from sklearn.model_selection import train_test_split

#DATA PROCESSING
df = pd.read_csv('data_extraction\\casas.csv', sep=';')

X, y = processing_data(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 9)


#CREATING MODELS
degree = 3
deep_model = dm.create_model(X, degree)
regression_model =  rm.create_model()

#TRAINING MODEL
dm.get_train_model(deep_model, X_train, X_test, y_train, y_test, degree)
rm.get_train_model(regression_model, X_train, X_test, y_train, y_test)

#EVALUATING MODEL
loss_value, metric_d = dm.evaluate(deep_model, X_test, y_test, degree)
metric_r = rm.evaluate(regression_model, X_test, y_test)

mean = y_test.mean()
print('Mean:', mean)
print('Métrica deep: ', metric_d, '     Erro em porcentagem: ', 100 - metric_d*100/mean)
print('Métrica regression: ', metric_r, '     Erro em porcentagem: ', 100 - metric_r*100/mean)

# print('train_score: ', regression_model.score(X_train, y_train))
# print('test_score: ', regression_model.score(X_test, y_test))

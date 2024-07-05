#TREINAMENTO DO MODELO
import pandas as pd
import numpy as np
import itertools as it
import pickle5 as pickle

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer, mean_absolute_error
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import SGDRegressor
# from sklearn.ensemble import GradientBoostingRegressor


class Polinomal(BaseEstimator, TransformerMixin):
    def __init__(self, degree):
        self.degree = degree

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_x = []
        if type(X) != pd.DataFrame:
            new_x = pd.DataFrame(X)
        else:
            new_x = X.copy()

        lista = [pd.DataFrame(np.full((new_x.shape[0], 1), 1))]

        for count in range(1, self.degree + 1):
          lista.append(new_x**count)

        new_x = pd.concat(lista, axis=1)

        return new_x

def create_model(X):

    # Definindo as colunas categóricas
    categorical_features = ['regiao']

    # Criando o ColumnTransformer
    one_hot_encoder = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
        ],
        remainder='passthrough'
    )

    pipe = Pipeline([
        ('one', one_hot_encoder),
        ('poly', Polinomal(degree=1)),#CustomTransformer(degree=1)
        ('scaler', StandardScaler()),
        ('regression', LinearRegression())
    ])

    par1 = {
        'poly__degree': [1,2,3,4,5,6],
        'scaler': [StandardScaler(), Normalizer()],
        'regression': [LinearRegression()]
    }

    par2 = {
        'poly__degree': [1,2,3,4,5,6],
        'scaler': [StandardScaler(), Normalizer()],
        'regression__alpha': [0.0001, 0.001, 0.01, 0.01, 0.1, 2],
        'regression': [SGDRegressor(max_iter=10000)]
    }

    # par3 = {
    #     'regression__min_samples_split': [2,3,4,5,6],
    #     'regression__min_samples_leaf': [1,2,3,4,5],
    #     'regression__max_depth': [3,4,5,6],
    #     'regression': [GradientBoostingRegressor()]
    # }

    parm = [par1, par2]#, par3

    scorer = make_scorer(mean_squared_error, greater_is_better=False)#make_scorer(mean_absolute_error, greater_is_better=False),
    model = GridSearchCV(pipe, parm, scoring=scorer, cv=20,  n_jobs=-1)
    
    return model

def get_train_model(regression_model, X_train, y_train):
    regression_model.fit(X_train, y_train)
    print(regression_model.best_estimator_)

    with open('model.pkl','wb') as f:
        pickle.dump(regression_model, f)

def get_saved_model():
    return pickle.load(open('model.pkl', 'rb'))

def evaluate(regression_model, X_test, y_test):
    return mean_absolute_error(regression_model.predict(X_test), y_test)
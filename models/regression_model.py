#TREINAMENTO DO MODELO
import pandas as pd
import numpy as np
import pickle

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer, mean_absolute_error
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import SGDRegressor


class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, degree):
        self.degree = degree

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_x = pd.DataFrame(X.values)

        lista = [pd.DataFrame(np.full((new_x.shape[0], 1), 1))]

        for count in range(1, self.degree + 1):
          lista.append(new_x**count)

        new_x = pd.concat(lista, axis=1)

        return new_x

def create_model():
    pipe = Pipeline([
        ('poly', CustomTransformer(degree=1)),#CustomTransformer(degree=1)
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
        'regression': [SGDRegressor(max_iter=5000)]
    }

    parm = [par1, par2]

    scorer = make_scorer(mean_squared_error, greater_is_better=False)#make_scorer(mean_absolute_error, greater_is_better=False),
    model = GridSearchCV(pipe, parm, scoring=scorer, cv=10, n_jobs=2)
    
    return model

def get_train_model(regression_model, X_train, X_test, y_train, y_test):
    regression_model.fit(X_train, y_train)
    print(regression_model.best_estimator_)

    with open('models\\model.pkl','wb') as f:
        pickle.dump(regression_model, f)

def get_saved_model():
    return pickle.load(open('models\\model.pkl', 'rb'))

def evaluate(regression_model, X_test, y_test):
    return mean_absolute_error(regression_model.predict(X_test), y_test)
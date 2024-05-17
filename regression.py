import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt


#LENDO ARQUIVO
df = pd.read_csv('casas.csv', sep=';')


#TRATANDO ARQUIVO
df = df.drop(['iptu', 'descricao'], axis='columns')

df = df.loc[(df['metro_quadrado'] > df['metro_quadrado'].quantile(0.05)) & (df['metro_quadrado'] < df['metro_quadrado'].quantile(0.95))]
df = df.loc[(df['preco'] > df['preco'].quantile(0.05)) & (df['preco'] < df['preco'].quantile(0.99))]

df = df.fillna({
    'condominio': 0,
    'quarto': 0,
    'banheiro': 0,
    'garagem': 0,
})

df = df.dropna() 

df = pd.get_dummies(df, columns=['vendedor', 'regiao'], dtype='int')


def map_func(str):
    map = {
        "jan": "january",
        "fev": "february",
        "mar": "march",
        "abr": "april",
        "mai": "may",
        "jun": "june",
        "jul": "july",
        "ago": "august",
        "set": "september",
        "out": "october",
        "nov": "november",
        "dez": "december"
    }

    new_str = str

    for name, value in map.items():
        new_str = new_str.replace(name, value)

    return new_str

df.loc[df['data'].apply(lambda x: 'de' in x), 'data'] = df.loc[df['data'].apply(lambda x: 'de' in x), 'data'].apply(map_func)

for index, row in df.iterrows():
    if 'de' in row['data']:
        data = datetime.datetime.now()

        df.loc[index, 'data'] = pd.to_datetime(row['data'], format='%d de %B-%H:%M')
        df.loc[index, 'data'] = df.loc[index, 'data'].replace(year=data.year)
    else:
        df.loc[index, 'data'] = pd.to_datetime(row['data'], format='%d/%m/%y-%H:%M')

data_inicial = datetime.datetime(2000, 1, 1)

df['data'] = df['data'].apply(lambda x: (x - data_inicial).days)

df = df.astype({
    'quarto': 'int32',
    'banheiro': 'int32',
    'garagem': 'int32',
})

print(df.corr()['preco'].sort_values(ascending=False).head(15))
#print(df[['regiao', 'preco']].groupby(['regiao']).mean().sort_values(by='preco', ascending=False))

#TREINAMENTO DO MODELO
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
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

lista = list(df.columns)
lista.remove('preco')

X = df[lista]
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state= 125)

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
    'regression': [SGDRegressor(max_iter=3000)]
}

parm = [par1, par2]

model = GridSearchCV(pipe, parm, cv=10)

model.fit(X_train, y_train)

print('train_score: ', model.score(X_train, y_train))
print('test_score: ', model.score(X_test, y_test))

print(model.best_params_)
    
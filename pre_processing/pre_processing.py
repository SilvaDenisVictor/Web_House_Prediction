import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

def processing_data(df):
    #TRATANDO ARQUIVO
    df = df.drop(['iptu', 'descricao'], axis='columns')
    df = df.loc[(df['metro_quadrado'] > df['metro_quadrado'].quantile(0.05)) & (df['metro_quadrado'] < df['metro_quadrado'].quantile(0.95))]
    df = df.loc[(df['preco'] > df['preco'].quantile(0.05)) & (df['preco'] < df['preco'].quantile(0.98))]

    df = df.fillna({
        'condominio': 0,
        'garagem': 0,
    })

    df = df.dropna() 

    # plt.figure()
    # plt.boxplot(df['preco'])
    # plt.figure()
    # plt.boxplot(df['metro_quadrado'])
    # plt.show()

    df = pd.get_dummies(df, columns=['vendedor', 'regiao'], dtype='int')

    data_inicial = datetime.datetime(2000, 1, 1)

    df['data'] = pd.to_datetime(df['data'])
    df['data'] = df['data'].apply(lambda x: (x - data_inicial).days)

    df = df.astype({
        'quarto': 'int32',
        'banheiro': 'int32',
        'garagem': 'int32',
    })

    print(df.corr()['preco'].sort_values(ascending=False).head(15))

    lista = list(df.columns)
    lista.remove('preco')

    X = df[lista]
    y = df['preco']

    return X, y

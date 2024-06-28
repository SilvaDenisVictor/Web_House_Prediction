import pandas as pd
import numpy as np
import datetime
# import matplotlib.pyplot as plt

def processing_data(df):
    #TRATANDO ARQUIVO
    df = df.drop(['iptu', 'descricao'], axis='columns')
    li_mq, ls_mq, li_pr, ls_pr = (0.02, 0.9900000000000001, 0.0, 0.9)#best_li()

    df = df.loc[(df['metro_quadrado'] > df['metro_quadrado'].quantile(li_mq)) & (df['metro_quadrado'] < df['metro_quadrado'].quantile(ls_mq))]
    df = df.loc[(df['preco'] > df['preco'].quantile(li_pr)) & (df['preco'] < df['preco'].quantile(ls_pr))]

    df = df.fillna({
        'garagem': 0,
    })

    df = df.dropna()

    df = pd.get_dummies(df, columns=['vendedor'], dtype=np.int8)

    data_inicial = datetime.datetime(2000, 1, 1)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['data'] = df['data'].apply(lambda x: (x - data_inicial).days)

    df = df.astype({
        'quarto': 'int32',
        'banheiro': 'int32',
        'garagem': 'int32',
    })

    # print(df.corr()['preco'].sort_values(ascending=False).head(15))

    lista = list(df.columns)
    lista.remove('preco')

    X = df[lista]
    y = df['preco']

    return X, y

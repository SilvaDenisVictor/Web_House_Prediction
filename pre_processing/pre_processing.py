import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer

def processing_data(df):
    #REMOVENDO COLUNAS
    df = df.drop(['id', 'iptu', 'descricao'], axis='columns')
    
    #TROCANDO VALORES NULOS 
    df = df.fillna({
        'garagem': 0,
    })

    #SALVANDO DADOS NO DICIONARIO
    dic = list(df['regiao'].unique())
    df['regiao'] = df['regiao'].apply(lambda x: x if x == np.nan else dic.index(x))

    #TRATANDO DATA
    data_inicial = datetime.datetime(2000, 1, 1)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['data'] = df['data'].apply(lambda x: (x - data_inicial).days)

    #CONVERTENDO DUMIES
    df = pd.get_dummies(df, columns=['vendedor'], dtype=np.int8)

    #APLICANDO KNNIMPUTER
    imputer = KNNImputer(n_neighbors=30)
    df = pd.DataFrame(imputer.fit_transform(df), columns=['preco', 'condominio', 'metro_quadrado', 'quarto', 'banheiro', 'garagem', 'regiao', 'data', 'com vendedor', 'com dono']) 

    #TROCANDO TIPOS, REMOVENDO LINHAS, 
    print('Shape then: ', df.shape)

    df = df.dropna()

    df = df.astype({
        'preco': 'float64',
        'condominio': 'float64',
        'metro_quadrado': 'float64',
        'quarto': 'int8',
        'banheiro': 'int8',
        'garagem': 'int8',
        'regiao': 'int16'
    })
    
    print('Shape now: ', df.shape)
    #REMOVENDO BORDAS
    li_mq, ls_mq, li_pr, ls_pr = (0.02, 0.9900000000000001, 0.0, 0.9)# (0.02, 0.9900000000000001, 0.0, 0.9)
    df = df.loc[(df['metro_quadrado'] > df['metro_quadrado'].quantile(li_mq)) & (df['metro_quadrado'] < df['metro_quadrado'].quantile(ls_mq))]
    df = df.loc[(df['preco'] > df['preco'].quantile(li_pr)) & (df['preco'] < df['preco'].quantile(ls_pr))]

    #DIVIDINDO ARQUIVO EM X E Y
    lista = list(df.columns)
    lista.remove('preco')

    X = df[lista]
    y = df['preco']

    
    print('VALORE ÚNICOS REGIOES: ', len(X['regiao'].unique()))
    print('SADISDJIAJSD\n\n\n')
    print(X['regiao'].unique().shape[0])
    print('\n\n\n')
    return X, y, dic

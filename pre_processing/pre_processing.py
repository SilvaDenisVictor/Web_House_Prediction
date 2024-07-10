import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer

def processing_data(df):
    #REMOVENDO COLUNAS, EMBARALHANDO LINHAS
    df = df.drop(['id', 'iptu', 'descricao', 'data'], axis='columns')

    #TROCANDO VALORES NULOS 
    df = df.fillna({
        'garagem': 0,
    })

    #SALVANDO DADOS NO DICIONARIO
    df.dropna(subset=['regiao'], inplace=True)

    dic = list(df['regiao'].unique())
    df['regiao'] = df['regiao'].apply(lambda x: dic.index(x) if x != '' else x)
    df.reset_index(inplace=True, drop=True)

    #TRATANDO DATA
    # data_inicial = datetime.datetime(2000, 1, 1)

    # df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    # df['data'] = df['data'].apply(lambda x: (x - data_inicial).days)

    #CONVERTENDO DUMIES
    df['vendedor'] = df['vendedor'].apply(lambda x: x.strip())

    df = pd.get_dummies(df, columns=['vendedor'], prefix=None, dtype=np.int8) 
    df.rename(columns={'vendedor_Direto com o dono': 'com_dono', 'vendedor_Profissional': 'com_profissional'}, inplace=True)
    
    df = df.sample(frac=1)

    #SEPARANDO DADOS COMPLETOS E REMOVENDO DOS DATAFRAME INICIAL
    df_full = df.dropna()

    df_full = df_full.astype({
        'preco': 'float64',
        'condominio': 'float64',
        'metro_quadrado': 'float64',
        'quarto': 'int8',
        'banheiro': 'int8',
        'garagem': 'int8',
        'regiao': 'int16'
    })

    X_f, y_f = df_full.loc[:, df_full.columns != 'preco'], df_full['preco']

    df = df.loc[df.index.delete(df_full.index)]

    #APLICANDO KNNIMPUTER
    imputer = KNNImputer(n_neighbors=30)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns) 

    #TROCANDO TIPOS, REMOVENDO LINHAS, 
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
    
    #REMOVENDO BORDAS
    li_mq, ls_mq, li_pr, ls_pr = (0.02, 0.9900000000000001, 0.00, 0.9)# (0.02, 0.9900000000000001, 0.0, 0.9)
    df = df.loc[(df['metro_quadrado'] > df['metro_quadrado'].quantile(li_mq)) & (df['metro_quadrado'] < df['metro_quadrado'].quantile(ls_mq))]
    df = df.loc[(df['preco'] > df['preco'].quantile(li_pr)) & (df['preco'] < df['preco'].quantile(ls_pr))]

    #DIVIDINDO ARQUIVO EM X E Y

    X = df.loc[:, df.columns != 'preco']
    y = df['preco']

    print('data do treino:\n')
    print(X.info())
    print()
    print()
    print('data do test:\n')
    print(X_f.info())

    return X, y, X_f, y_f, dic

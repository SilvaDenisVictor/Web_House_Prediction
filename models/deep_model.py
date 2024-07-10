import pandas as pd
import numpy as np

import tensorflow as tf
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, Normalization, Input
from keras.optimizers import Adam, SGD
from keras.losses import MeanAbsolutePercentageError
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, load_model

def transform(X, degree):
    new_x = pd.DataFrame(X.values)

    lista = [pd.DataFrame(np.full((new_x.shape[0], 1), 1))]

    for count in range(1, degree + 1):
        lista.append(new_x**count)

    new_x = pd.concat(lista, axis=1)

    return new_x

def create_model(dic, degree):
    from keras.models import Model, Sequential
    from keras.layers import Input, Embedding, Flatten, Dense, Concatenate

    #CRIANDO INPUTS
    input_regiao = Input(shape=(1,))
    input_numerico = Input(shape=(7,))


    #TRATANDO REGIAO

    regiao = Embedding(input_dim=len(dic), output_dim=30, name='embedding_regiao')(input_regiao)
    regiao = Flatten()(regiao)
    regiao = Model(inputs=input_regiao, outputs=regiao)

    #TRATANDO DADOS NUMERICOS
    numerico = Dense(32, activation='relu')(input_numerico)
    numerico = Dense(64, activation='relu')(numerico)
    numerico = Model(inputs=input_numerico, outputs=numerico)

    #JUNTANDO AS DUAS ENTRADAS
    combined = Concatenate()([numerico.output, regiao.output])

    #FINAL
    final = Dense(32, activation='relu')(combined)
    final = Dense(1, activation='relu')(final)

    #FINAL MODEL
    model = Model(inputs=[numerico.input, regiao.input], outputs=final)
  
    # normalizer = Normalization(axis=-1)
    # normalizer.adapt(transform(X, degree).values)

    # model = Sequential([
    #     normalizer,
    #     Dense(128, activation='relu'),
    #     Dense(512, activation='relu'),
    #     Dense(256, activation='relu'),
    #     Dense(64, activation='relu'),
    #     Dense(1)  # Camada de saída para regressão
    # ])
    #Adam(learning_rate=0.009, beta_1=0.8, beta_2=0.991, epsilon=1e-07)
    model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mean_absolute_error'])
    
    return model

def get_train_model(deep_model, X_train, y_train, degree):
    checkpoint_callback = ModelCheckpoint(
        filepath='/app/models/best_model.keras', 
        save_best_only=True, 
        monitor='val_loss', 
        mode='min', 
        verbose=1
    )
    
    X_train_prep = [X_train.loc[:, X_train.columns != 'regiao'], X_train['regiao']]

    # print(X_train_prep[0].info())
    # print(X_train_prep[1].info(), '\n\n\n')
    
    #validation_data=(X_test_prep, y_test)
    deep_model.fit(X_train_prep, y_train, validation_split=0.05, epochs=20, batch_size=1, callbacks=[checkpoint_callback])

def evaluate(deep_model, X_test, y_test, degree):
    X_test_prep = [X_test.loc[:, X_test.columns != 'regiao'], X_test['regiao']]

    loss_value, metric_value = deep_model.evaluate(X_test_prep, y_test)

    return loss_value, metric_value

def get_saved_model():
    return load_model('/app/best_model.keras')

def predict(deep_model, df):
    predicted_price = deep_model.predict([df.loc[:, df.columns != 'regiao'], df['regiao']])
    
    return float(predicted_price[0,0])

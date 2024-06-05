import pandas as pd
import numpy as np

import tensorflow as tf
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, Normalization, Input
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, load_model

tf.config.threading.set_intra_op_parallelism_threads(2)

def transform(X, degree):
    new_x = pd.DataFrame(X.values)

    lista = [pd.DataFrame(np.full((new_x.shape[0], 1), 1))]

    for count in range(1, degree + 1):
        lista.append(new_x**count)

    new_x = pd.concat(lista, axis=1)

    return new_x

def create_model(X, degree):
   
    normalizer = Normalization(axis=-1)
    normalizer.adapt(transform(X, degree).values)

    model = Sequential([
        normalizer,
        Dense(512, activation='relu'),
        Dense(256, activation='relu'),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(1)  # Camada de saída para regressão
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

    return model

def get_train_model(deep_model, X_train, X_test, y_train, y_test, degree):
    checkpoint_callback = ModelCheckpoint(
        filepath='models\\best_model.keras', 
        save_best_only=True, 
        monitor='val_loss', 
        mode='min', 
        verbose=1
    )

    deep_model.fit(transform(X_train, degree), y_train, validation_data=(transform(X_test, degree), y_test), epochs=15, batch_size=1, callbacks=[checkpoint_callback])

def evaluate(deep_model, X_test, y_test, degree):
    loss_value, metric_value = deep_model.evaluate(transform(X_test, degree), y_test)

    return loss_value, metric_value

def get_saved_model():
    return load_model('models\\best_model.keras')

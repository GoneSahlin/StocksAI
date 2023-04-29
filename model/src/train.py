import tensorflow as tf

from src import utils
from dataset_generator import DatasetGenerator


def train():
    train_dfs, val_dfs, test_dfs = utils.load_and_setup_data()

    wide_window = DatasetGenerator(train_dfs, val_dfs, test_dfs,  10, 10, 1, ['Adj Close'])

    lstm_model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(4, return_sequences=True),
        tf.keras.layers.Dense(units=1)
    ])

    lstm_model.compile(loss=tf.keras.losses.MeanSquaredError(),
                   optimizer=tf.keras.optimizers.Adam(),
                   metrics=[tf.keras.metrics.MeanAbsoluteError()])
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                  patience=2,
                                                  mode='min')

    history = lstm_model.fit(wide_window.train, epochs=20,
                         validation_data=wide_window.val,
                         callbacks=[early_stopping])

    val_performance_lstm = lstm_model.evaluate(wide_window.val)
    performance_lstm = lstm_model.evaluate(wide_window.test, verbose=0)

    print(lstm_model.metrics_names)
    print(val_performance_lstm)
    print(performance_lstm)

    wide_window.windows[0].plot(lstm_model)


if __name__ == '__main__':
    train()

import tensorflow as tf

from src import utils
from dataset_generator import DatasetGenerator


def train():
    price_dfs = utils.load_data('prices')
    quarterly_financials_dfs = utils.load_data('quarterly_financials')

    dfs = []
    for (price_df, quarterly_financials_df) in zip(price_dfs, quarterly_financials_dfs):
        price_df = utils.clean_price_df(price_df)
        quarterly_financials_df = utils.clean_quarterly_financials_df(quarterly_financials_df)

        df = utils.join_quarterly_financials_df(price_df, quarterly_financials_df)

        df = df.drop(["Date", "end_date"])

        dfs.append(df)

    train_dfs, val_dfs, test_dfs = utils.setup_data(dfs, .7, .2)

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

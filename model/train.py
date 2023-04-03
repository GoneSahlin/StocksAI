import tensorflow as tf

import utils
from dataset_generator import DatasetGenerator


def train():
    price_dfs = utils.load_data('prices')
    revenue_dfs = utils.load_data('revenues')

    dfs = []
    for (price_df, revenue_df) in zip(price_dfs, revenue_dfs):
        price_df = utils.clean_price_df(price_df)
        revenue_df = utils.clean_revenue_df(revenue_df)

        df = utils.join_revenue_df(price_df, revenue_df)

        df = df.drop(["Date", "end_date"])

        dfs.append(df)

    train_dfs, val_dfs, test_dfs = utils.setup_data(dfs, .7, .2)

    dataset_generator = DatasetGenerator(train_dfs, val_dfs, test_dfs)

    dataset_generator.make_windows(5, 5, 5, ['Price'])
    dataset_generator.make_datasets()

    lstm_model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(32, return_sequences=True),
        tf.keras.layers.Dense(units=1)
    ])

    lstm_model.compile(loss=tf.keras.losses.MeanSquaredError(),
                   optimizer=tf.keras.optimizers.Adam(),
                   metrics=[tf.keras.metrics.MeanAbsoluteError()])
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                  patience=2,
                                                  mode='min')

    history = lstm_model.fit(dataset_generator.train, epochs=20,
                         validation_data=dataset_generator.val,
                         callbacks=[])

    val_performance_lstm = lstm_model.evaluate(dataset_generator.val)
    performance_lstm = lstm_model.evaluate(dataset_generator.test, verbose=0)

    print(lstm_model.metrics_names)
    print(val_performance_lstm)
    print(performance_lstm)

    dataset_generator.windows[0].plot(lstm_model)


if __name__ == '__main__':
    train()

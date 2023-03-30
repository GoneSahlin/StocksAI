import polars as pl
import tensorflow as tf

from window_generator import WindowGenerator


def load_data():
    prices_df = pl.read_parquet("data/F_prices.parquet")

    return prices_df


def train():
    df = load_data()

    # split data
    n = len(df)
    train_df = df[0:int(n*0.7)]
    val_df = df[int(n*0.7):int(n*0.9)]
    test_df = df[int(n*0.9):]


    # TODO normalize data


    # create windows
    # window = WindowGenerator(input_width=)

    # lstm_model = tf.keras.models.Sequential([
    # # Shape [batch, time, features] => [batch, time, lstm_units]
    # tf.keras.layers.LSTM(32, return_sequences=True),
    # # Shape => [batch, time, features]
    # tf.keras.layers.Dense(units=1)])

    # optimizer = tf.keras.optimizers.SGD(learning_rate=1e-8, momentum=0.9)
    # lstm_model.compile(loss=tf.keras.losses.Huber(),
    #           optimizer=optimizer,
    #           metrics=["mae"])



if __name__ == '__main__':
    train()

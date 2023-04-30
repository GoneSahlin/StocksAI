import tensorflow as tf
import s3fs
import tempfile
import os
import zipfile
import numpy as np
import polars as pl

from utils import utils
from utils.window_generator import WindowGenerator


def load_model():
    with tempfile.TemporaryDirectory() as tempdir:
        temp_path = os.path.join(tempdir, "model")
        temp_zip_path = temp_path + ".zip"

        fs = s3fs.S3FileSystem()
        s3_path = "s3://sahlin.stocksai/model.zip"
        fs.get(s3_path, temp_zip_path)

        with zipfile.ZipFile(temp_zip_path) as zip_ref:
            zip_ref.extractall(temp_path)

            model = tf.keras.models.load_model(temp_path)

            return model


def load_data():
    dfs, _, _, tickers = utils.load_and_setup_data(train_percent=1, val_percent=0, get_tickers=True)
    
    return dfs, tickers


def make_inputs(dfs):
    inputs = []
    for df in dfs:
        # get last 10 rows
        df = df[-10:]

        # add extra row of zeros to not mess up the window generator trying to get the next label
        df = pl.concat([df, pl.DataFrame([[0] for _ in range(len(df.columns))], schema=df.schema)])

        window = WindowGenerator(10, 10, 1, label_columns=['Adj Close'], train_df=df, val_df=pl.DataFrame(), test_df=pl.DataFrame())

        input = next(window.train.as_numpy_iterator())[0]

        inputs.append(input)

    return inputs


def make_predictions(model: tf.keras.Model, inputs):
    predictions = []
    for input in inputs:
        output = model.predict(input)

        prediction = output[0][0][-1]
        
        predictions.append(prediction)

    return predictions


def predict():
    model = load_model()
    dfs, tickers = load_data()

    inputs = make_inputs(dfs)

    predictions = make_predictions(model, inputs)

    predictions_df = pl.DataFrame({"Ticker": tickers, "Predicted Percent Increase": predictions})

    return predictions_df


if __name__ == "__main__":
    predict()




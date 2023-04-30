import tensorflow as tf
import s3fs
import tempfile
import os
import zipfile
import polars as pl

import utils
from window_generator import WindowGenerator


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
    dfs, _, _, tickers, means, stds = utils.load_and_setup_data(train_percent=1, val_percent=0, get_tickers=True, get_mean_and_std=True)
    
    return dfs, tickers, means, stds


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


def denormalize_predictions(df: pl.DataFrame, tickers, means_dfs, stds_dfs):
    means = [means_df.select(pl.col("Adj Close")).item() for means_df in means_dfs]
    stds = [stds_df.select(pl.col("Adj Close")).item() for stds_df in stds_dfs]

    means_dict = {ticker: mean for ticker, mean in zip(tickers, means)}
    stds_dict = {ticker: std for ticker, std in zip(tickers, stds)}

    print(means_dict)
    print(stds_dict)
    print(df)

    
    df = df.with_columns((((pl.col("Predicted Percent Increase") * pl.col("Ticker").map_dict(stds_dict) + pl.col("Ticker").map_dict(means_dict)) - 1) * 100).alias("Predicted Percent Increase"))

    return df


def predict():
    model = load_model()
    dfs, tickers, means, stds = load_data()

    inputs = make_inputs(dfs)

    predictions = make_predictions(model, inputs)

    predictions_df = pl.DataFrame({"Ticker": tickers, "Predicted Percent Increase": predictions})

    predictions_df = denormalize_predictions(predictions_df, tickers, means, stds)

    return predictions_df

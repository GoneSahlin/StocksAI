import tensorflow as tf
import s3fs
import os
import tempfile
import zipfile

from utils import utils
from dataset_generator import DatasetGenerator


def train():
    train_dfs, val_dfs, test_dfs = utils.load_and_setup_data(train_percent=.8, val_percent=.2)


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

    return lstm_model


def zipdir(path, ziph):
  # Zipfile hook to zip up model folders
  length = len(path)
  for root, dirs, files in os.walk(path):
    folder = root[length:] # Stop zipping parent folders
    for file in files:
      ziph.write(os.path.join(root, file), os.path.join(folder, file))


def save_model(model):
    with tempfile.TemporaryDirectory() as tempdir:
        temp_path = os.path.join(tempdir, "model")

        model.save(temp_path)

        temp_zip_path = temp_path + ".zip"

        zipf = zipfile.ZipFile(temp_zip_path, "w", zipfile.ZIP_STORED)
        zipdir(temp_path, zipf)
        zipf.close()

        fs = s3fs.S3FileSystem()
        s3_path = "s3://sahlin.stocksai/model.zip"

        fs.put(temp_zip_path, s3_path)


if __name__ == '__main__':
    model = train()

    save_model(model)

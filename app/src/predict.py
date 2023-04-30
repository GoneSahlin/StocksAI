import tensorflow as tf
import s3fs
import tempfile
import os
import zipfile

from utils import utils


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
    dfs, _, _ = utils.load_and_setup_data(train_percent=1, val_percent=0)

    # just one df for now
    df = dfs[0]
    
    return df


if __name__ == "__main__":
    model = load_model()

    print(model)
    # df = load_data()

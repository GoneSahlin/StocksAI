import numpy as np
import polars as pl
import tensorflow as tf

from utils.window_generator import WindowGenerator
from utils import utils


def create_df():
    df = pl.DataFrame({'x': range(100), 'y': range(100, 200)})

    return df


def test_init():
    df = create_df()
    train_df, val_df, test_df = utils.split_train_val_test(df, .7, .2)

    window = WindowGenerator(input_width=5, label_width=5, shift=1, label_columns=['x'], train_df=train_df, val_df=val_df, test_df=test_df)

    assert window.total_window_size == 6
    assert np.array_equal(window.input_indices, range(5))
    assert np.array_equal(window.label_indices, range(1,6))
    assert window.label_columns == ['x']


def test_split_window():
    df = create_df()
    train_df, val_df, test_df = utils.split_train_val_test(df, .7, .2)

    window = WindowGenerator(input_width=5, label_width=5, shift=1, label_columns=['x'], train_df=train_df, val_df=val_df, test_df=test_df)
    example_window = tf.stack([train_df[:window.total_window_size].to_numpy(),
                                train_df[20:20+window.total_window_size].to_numpy(),
                                train_df[50:50+window.total_window_size].to_numpy()])
    

    example_inputs, example_labels = window.split_window(example_window)

    assert example_window.shape == (3, 6, 2)
    assert example_inputs.shape == (3, 5, 2)
    assert example_labels.shape == (3, 5, 1)


def test_make_dataset():
    df = create_df()
    train_df, val_df, test_df = utils.split_train_val_test(df, .7, .2)
    window = WindowGenerator(input_width=5, label_width=5, shift=1, label_columns=['x'], train_df=train_df, val_df=val_df, test_df=test_df)

    ds = window.make_dataset(window.train_df)

    for inputs, labels in ds.take(1):
        assert inputs.shape == (32, 5, 2)
        assert labels.shape == (32, 5, 1)

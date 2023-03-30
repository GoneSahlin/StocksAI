import pandas as pd

from model import utils


def create_df():
    df = pd.DataFrame({'x': range(100), 'y': range(100, 200)})

    return df


def test_split_train_val_test():
    df = create_df()

    train_df, val_df, test_df = utils.split_train_val_test(df, .7, .2)

    assert len(train_df) + len(val_df) + len(test_df) == len(df)

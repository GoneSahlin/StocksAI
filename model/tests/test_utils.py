import polars as pl

from model import utils


def create_df():
    df = pl.DataFrame({'x': range(100), 'y': range(100, 200)})

    return df


def create_dfs():
    df1 = pl.DataFrame({'x': range(100), 'y': range(100, 200)})
    df2 = pl.DataFrame({'x': range(200, 250), 'y': range(250, 300)})

    dfs = [df1, df2]

    return dfs


def test_split_train_val_test():
    df = create_df()

    train_df, val_df, test_df = utils.split_train_val_test(df, .7, .2)

    assert len(train_df) + len(val_df) + len(test_df) == len(df)


def test_split_dfs():
    dfs = create_dfs()
    train_dfs, val_dfs, test_dfs = utils.split_dfs(dfs, .7, .2)

    assert len(train_dfs) == len(val_dfs) == len(test_dfs) == 2
    for i in range(len(dfs)):
        assert len(train_dfs[i]) + len(val_dfs[i]) + len(test_dfs[i]) == len(dfs[i])

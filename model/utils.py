import polars as pl
import os


def split_train_val_test(df, train_percent, val_percent):
    n = len(df)
    train_df = df[0:int(n*train_percent)]
    val_df = df[int(n*train_percent):int(n*(train_percent + val_percent))]
    test_df = df[int(n*(train_percent + val_percent)):]

    return train_df, val_df, test_df


def split_dfs(dfs, train_percent, val_percent):
    train_dfs = []
    val_dfs = []
    test_dfs = []
    for df in dfs:
        train_df, val_df, test_df = split_train_val_test(df, train_percent, val_percent)

        train_dfs.append(train_df)
        val_dfs.append(val_df)
        test_dfs.append(test_df)

    return train_dfs, val_dfs, test_dfs


def load_data(folder):
    filenames = os.listdir(os.path.join("data", folder))
    
    dfs = []
    for filename in filenames:
        filepath = os.path.join("data", folder, filename)

        df = pl.read_csv(filepath)

        dfs.append(df)

    return dfs


def setup_data(dfs, train_percent, val_percent):
    train_dfs = []
    val_dfs = []
    test_dfs = []
    for df in dfs:
        # drop columns
        df.drop_in_place('Date')

        # split data
        train_df, val_df, test_df = split_train_val_test(df, train_percent, val_percent)

        # normalize data
        train_mean = train_df.mean()
        train_std = train_df.std()

        train_df = train_df.with_columns([
            (pl.col(label) - train_mean[label]) / train_std[label] for label in train_mean.columns
        ])

        val_df = val_df.with_columns([
            (pl.col(label) - train_mean[label]) / train_std[label] for label in train_mean.columns
        ])

        test_df = test_df.with_columns([
            (pl.col(label) - train_mean[label]) / train_std[label] for label in train_mean.columns
        ])

        # store dfs
        train_dfs.append(train_df)
        val_dfs.append(val_df)
        test_dfs.append(test_df)

    return train_dfs, val_dfs, test_dfs


def join_revenue(price_df: pl.DataFrame, revenue_df: pl.DataFrame):
    revenue_df = revenue_df.sort(by="end_date")
    df = price_df.join_asof(revenue_df, left_on="Date", right_on="end_date", strategy="backward")

    return df

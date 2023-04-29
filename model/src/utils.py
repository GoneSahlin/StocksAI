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


def load_data(folder, return_filenames=False):
    filenames = os.listdir(os.path.join("data", folder))

    filenames.sort()
    
    dfs = []
    for filename in filenames:
        filepath = os.path.join("data", folder, filename)

        df = pl.read_csv(filepath)

        dfs.append(df)

    if return_filenames:
        return dfs, filenames
    return dfs


def setup_data(dfs, train_percent, val_percent):
    train_dfs = []
    val_dfs = []
    test_dfs = []
    for df in dfs:
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


def clean_price_df(df: pl.DataFrame):
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))

    df = df.with_columns([(pl.col(label) / pl.col(label).shift()) for label in df.columns[1:-1]])

    # remove top row
    df = df[1:]

    return df


def clean_quarterly_financials_df(df: pl.DataFrame):
    df = df.with_columns(pl.col("end_date").str.strptime(pl.Date, format="%Y-%m-%d"))

    return df


def join_quarterly_financials_df(price_df: pl.DataFrame, quarterly_financials_df: pl.DataFrame):
    quarterly_financials_df = quarterly_financials_df.sort(by="end_date")
    earliest_date = quarterly_financials_df.select("end_date").min(0)[0,0]
    df = price_df.filter(pl.col("Date") >= earliest_date).join_asof(quarterly_financials_df, left_on="Date", right_on="end_date", strategy="backward")

    return df


def clean_index_df(df: pl.DataFrame, ticker):
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))

    df = df.with_columns(pl.col(ticker) / pl.col(ticker).shift())

    return df


def combine_index_dfs():
    index_dfs, index_tickers = load_data('indexes', return_filenames=True)

    index_tickers = [ticker[:-4] for ticker in index_tickers] # remove .csv from filenames
    for i, index_df in enumerate(index_dfs):
        index_df = clean_index_df(index_df, index_tickers[i])

    indexes_df: pl.DataFrame = index_dfs[0]
    for index_df in index_dfs[1:]:
        indexes_df = indexes_df.join(index_df, on="Date")

    return indexes_df


def load_and_setup_data():
    price_dfs = load_data('prices')
    quarterly_financials_dfs = load_data('quarterly_financials')


    dfs = []
    for (price_df, quarterly_financials_df) in zip(price_dfs, quarterly_financials_dfs):
        price_df = clean_price_df(price_df)
        quarterly_financials_df = clean_quarterly_financials_df(quarterly_financials_df)
        
        df = join_quarterly_financials_df(price_df, quarterly_financials_df)

        df = df.drop(["Date", "end_date"])

        dfs.append(df)

    train_dfs, val_dfs, test_dfs = setup_data(dfs, .7, .2)

    return train_dfs, val_dfs, test_dfs

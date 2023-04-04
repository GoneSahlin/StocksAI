import polars as pl
import datetime

from model import utils
from model.dataset_generator import DatasetGenerator


def create_df():
    df = pl.DataFrame({'x': range(100), 'y': range(100, 200)})

    return df


def create_dfs():
    df1 = pl.DataFrame({'x': range(100), 'y': range(100, 200)})
    df2 = pl.DataFrame({'x': range(200, 250), 'y': range(250, 300)})

    dfs = [df1, df2]

    return dfs


def create_example_price_df():
    price_df = pl.DataFrame({"Date": ["2022-05-06", "2022-06-01", "2022-07-12", "2022-08-11", "2022-09-15", "2022-10-10", "2022-11-10", "2022-12-19", "2023-01-04", "2023-02-21", "2023-03-20"],
                             "Price": [13.098385, 12.490015, 10.655688, 14.737184, 13.862077, 10.575768, 13.201092, 10.996746, 11.29777, 12.2, 11.18],
                             "Volume": [66622200, 50726200, 58414500, 61567000, 61377000, 115548900, 75638500, 88062500, 53429700, 77724200, 74975100]})

    return price_df

def create_example_revenue_df():
    revenue_df = pl.DataFrame({"end_date": ["2022-12-31", "2022-09-30", "2022-06-30", "2022-03-31", "2021-12-31"],
                               "revenue": [43999000000, 39392000000, 40190000000, 34476000000, 37678000000]})

    return revenue_df


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


def test_load_data():
    dfs = utils.load_data('prices')

    assert dfs


def test_setup_data():
    dfs = utils.load_data('prices')

    for df in dfs:
        df.drop_in_place("Date")

    train_dfs, val_dfs, test_dfs = utils.setup_data(dfs, .7, .2)

    assert train_dfs
    assert val_dfs
    assert test_dfs


def test_clean_price_df():
    price_df = create_example_price_df()
    price_df = utils.clean_price_df(price_df)

    assert type(price_df[0,0]) == datetime.date


def test_clean_quarterly_financials_df():
    revenue_df = create_example_revenue_df()
    revenue_df = utils.clean_quarterly_financials_df(revenue_df)

    assert type(revenue_df[0,0]) == datetime.date


def test_join_quarterly_financials_df():
    price_df = create_example_price_df()
    price_df = utils.clean_price_df(price_df)

    revenue_df = create_example_revenue_df()
    revenue_df = utils.clean_quarterly_financials_df(revenue_df)

    df = utils.join_quarterly_financials_df(price_df, revenue_df)
    
    assert df.filter(pl.col("Date") == datetime.datetime(2022, 5, 6)).get_column("revenue")[0] == 34476000000
    assert df.filter(pl.col("Date") == datetime.datetime(2022, 12, 19)).get_column("revenue")[0] == 39392000000

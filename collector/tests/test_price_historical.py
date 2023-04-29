import polars as pl

from src import price_historical


def test_get_download_link():
    link = price_historical.get_download_link('F')

    correct_link_start = "https://query1.finance.yahoo.com/v7/finance/download/F"

    assert link[:len(correct_link_start)] == correct_link_start


def test_get_data():
    link = price_historical.get_download_link('F')
    data = price_historical.get_data(link)
    assert type(data) == str

    link = price_historical.get_download_link('^GSPC')
    data = price_historical.get_data(link)
    assert type(data) == str


def test_clean_data():
    link = price_historical.get_download_link('F')
    data = price_historical.get_data(link)

    df = price_historical.clean_data(data)

    assert type(df) == pl.DataFrame
    assert df.columns == ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

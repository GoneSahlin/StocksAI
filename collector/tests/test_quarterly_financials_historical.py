import polars as pl
from datetime import date

from collector import quarterly_financials_historical

def test_get_macrotrends_url():
    url = quarterly_financials_historical.get_macrotrends_url('F')

    assert url == "https://www.macrotrends.net/stocks/charts/F/ford-motor/"


def test_get_macrotrends_data():
    url = quarterly_financials_historical.get_macrotrends_url('F')
    df = quarterly_financials_historical.get_macrotrends_data(url, "eps", "eps-earnings-per-share-diluted", unit_multiplier=1, value_dtype=float)

    assert df.columns == ['end_date', 'eps']
    assert not df.is_empty()
    
    assert df.filter(pl.col("end_date") == date(2022, 12, 31))['eps'][0] == 0.34

    df = quarterly_financials_historical.get_macrotrends_data(url, "revenue", "revenue")

    assert df.columns == ['end_date', 'revenue']
    assert not df.is_empty()
    
    assert df.filter(pl.col("end_date") == date(2022, 12, 31))['revenue'][0] == 43999000000

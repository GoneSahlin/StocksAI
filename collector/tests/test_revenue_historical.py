from datetime import date
import polars as pl

from collector import revenue_historical


def test_get_url():
    url = revenue_historical.get_url('F')

    assert url == "https://www.macrotrends.net/stocks/charts/F/ford-motor/revenue"
    

def test_get_data():
    url = revenue_historical.get_url('F')
    df = revenue_historical.get_data(url)

    assert df.columns == ['end_date', 'revenue']
    assert not df.is_empty()
    
    assert df.filter(pl.col("end_date") == date(2022, 12, 31))['revenue'][0] == 43999000000

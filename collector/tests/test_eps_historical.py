from datetime import date
import polars as pl

from collector import eps_historical


def test_get_url():
    url = eps_historical.get_url('F')

    assert url == "https://www.macrotrends.net/stocks/charts/F/ford-motor/eps-earnings-per-share-diluted"
    

def test_get_data():
    url = eps_historical.get_url('F')
    df = eps_historical.get_data(url)

    assert df.columns == ['end_date', 'eps']
    assert not df.is_empty()
    
    assert df.filter(pl.col("end_date") == date(2022, 12, 31))['eps'][0] == 0.34

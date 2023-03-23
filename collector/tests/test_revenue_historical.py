import revenue_historical


def test_get_url():
    url = revenue_historical.get_url('F')

    assert url == "https://www.macrotrends.net/stocks/charts/F/ford-motor/revenue"
    

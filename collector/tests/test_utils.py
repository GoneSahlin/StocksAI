from collector import utils


def test_get_macrotrends_url():
    url = utils.get_macrotrends_url('F')

    assert url == "https://www.macrotrends.net/stocks/charts/F/ford-motor/"

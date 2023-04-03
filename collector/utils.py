import requests


def get_macrotrends_url(ticker):
    url = "https://www.macrotrends.net/stocks/charts/" + ticker

    # requesting adds the name of the company to the end of the url
    response = requests.get(url)
    url = response.url

    return url
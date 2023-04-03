import requests
from bs4 import BeautifulSoup, Tag
import polars as pl
from datetime import date
import os

from collector import utils


def get_url(ticker):
    url = utils.get_macrotrends_url(ticker)

    url += "eps-earnings-per-share-diluted"

    return url


def get_data(url):
    df = utils.get_macrotrends_data(url, 1, "eps", float)
        
    return df


def collect_eps_historical(ticker):
    url = get_url(ticker)
    df = get_data(url)

    filepath = os.path.join("data", "eps", ticker + "_eps.csv")
    df.write_csv(filepath)


def main():
    collect_eps_historical("F")
    collect_eps_historical("AAPL")


if __name__ == "__main__":
    main()

import requests
import polars as pl
from io import StringIO
import os


def get_download_link(ticker):
    period_1 = "1"
    period_2 = "9999999999"
    
    link = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + period_1 + "&period2=" + period_2 + "&interval=1d&events=history&includeAdjustedClose=true"

    return link


def get_data(link):
    try:
        response = requests.get(link, headers={'User-agent': 'Mozilla/5.0'})
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        print(e.response.text)


def clean_data(data: str) -> pl.DataFrame:
    df = pl.read_csv(StringIO(data))
    # df = df.drop(["Open","High","Low","Close"])

    # df = df.rename({"Adj Close": "Price"})

    return df


def collect_price_historical(ticker):
    link = get_download_link(ticker)
    data = get_data(link)
    df = clean_data(data)

    return df


def save_price_historical(df, ticker, fs, s3_prefix):
    filepath = os.path.join(s3_prefix, "prices", ticker + "_prices.csv")
    with fs.open(filepath, 'wb') as outfile:
        df.write_csv(outfile)
    

def collect_index_historical(ticker):
    link = get_download_link(ticker)
    data = get_data(link)
    df = clean_data(data)

    df = df.select(pl.col(["Date", "Adj Close"]))
    df = df.rename({"Adj Close": ticker})

    return df


def save_index_historical(df, ticker, fs, s3_prefix):
    filepath = os.path.join(s3_prefix, "indexes", ticker + ".csv")
    with fs.open(filepath, 'wb') as outfile:
        df.write_csv(outfile)


def main():
    df = collect_price_historical("F")
    # collect_price_historical("AAPL")


if __name__ == "__main__":
    main()

import requests
import polars as pl
from io import StringIO


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
    df = df.drop(["Open","High","Low","Close"])

    return df


def save_to_csv(ticker, df: pl.DataFrame):
    filepath = "../data/" + ticker + ".csv"
    
    df.write_csv(filepath)


def save_to_parquet(ticker, df: pl.DataFrame):
    filepath = "../data/" + ticker + "_prices.parquet"

    df.write_parquet(filepath)


def main():
    link = get_download_link("F")
    # get_download(driver, "AAPL")

    data = get_data(link)
    data = clean_data(data)
    save_to_parquet("F", data)


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup, Tag
import polars as pl
from datetime import date
import os


def get_url(ticker):
    url = "https://www.macrotrends.net/stocks/charts/" + ticker

    # requesting adds the name of the company to the end of the url
    response = requests.get(url)
    url = response.url

    url += "revenue"

    return url


def get_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find_all("table", class_="historical_data_table table")[1]

        end_dates = []
        revenues = []
        for child in table.tbody.children:
            if isinstance(child, Tag):
                end_date = date.fromisoformat(child.td.text)
                revenue_str: str = child.contents[3].text
                revenue = int(revenue_str.replace("$", "").replace(",", "")) * 1000000

                end_dates.append(end_date)
                revenues.append(revenue)
                
        df = pl.DataFrame({"end_date": end_dates, "revenue": revenues})
        
        return df


def collect_revenue_historical(ticker):
    url = get_url(ticker)
    df = get_data(url)

    filepath = os.path.join("data", "revenues", ticker + "_revenues.parquet")
    df.write_parquet(filepath)


def main():
    collect_revenue_historical("F")
    collect_revenue_historical("AAPL")


if __name__ == "__main__":
    main()

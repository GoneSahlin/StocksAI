import requests
from bs4 import BeautifulSoup, Tag
from datetime import date
import polars as pl


def get_macrotrends_url(ticker):
    url = "https://www.macrotrends.net/stocks/charts/" + ticker

    # requesting adds the name of the company to the end of the url
    response = requests.get(url)
    url = response.url

    return url


def get_macrotrends_data(url, unit_multiplier, value_name, value_dtype=int):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find_all("table", class_="historical_data_table table")[1]

        end_dates = []
        values = []
        for child in table.tbody.children:
            if isinstance(child, Tag):
                end_date = date.fromisoformat(child.td.text)
                value_str: str = child.contents[3].text
                value = value_dtype(value_str.replace("$", "").replace(",", "")) * unit_multiplier

                end_dates.append(end_date)
                values.append(value)
                
        df = pl.DataFrame({"end_date": end_dates, value_name: values})
        
        return df

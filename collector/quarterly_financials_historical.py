import requests
import polars as pl
from bs4 import BeautifulSoup, Tag
from datetime import date
import os


def get_macrotrends_url(ticker):
    url = "https://www.macrotrends.net/stocks/charts/" + ticker

    # requesting adds the name of the company to the end of the url
    response = requests.get(url)
    url = response.url

    return url


def get_macrotrends_data(url, value_name, url_extension, unit_multiplier=1_000_000, value_dtype=int):
    response = requests.get(url + url_extension)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find_all("table", class_="historical_data_table table")[1]

        end_dates = []
        values = []
        for child in table.tbody.children:
            if isinstance(child, Tag):
                end_date = date.fromisoformat(child.td.text)
                value_str: str = child.contents[3].text
                value_str = value_str.replace("$", "").replace(",", "")
                if value_str != '':
                    value = value_dtype(value_str) * unit_multiplier
                else:
                    value = 0

                end_dates.append(end_date)
                values.append(value)
                
        df = pl.DataFrame({"end_date": end_dates, value_name: values})
        
        return df



def collect_quarterly_historical(ticker):
    macrotrends_url = get_macrotrends_url(ticker)

    # get data
    revenue_df = get_macrotrends_data(macrotrends_url, "revenue", "revenue")
    gross_profit_df = get_macrotrends_data(macrotrends_url, "gross_profit", "gross-profit")
    operating_income_df = get_macrotrends_data(macrotrends_url, "operating_income", "operating-income")
    ebitda_df = get_macrotrends_data(macrotrends_url, "ebitda", "ebitda")
    net_income_df = get_macrotrends_data(macrotrends_url, "net_income", "net-income")
    eps_df = get_macrotrends_data(macrotrends_url, "eps", "eps-earnings-per-share-diluted", unit_multiplier=1, value_dtype=float)
    shares_outstanding_df = get_macrotrends_data(macrotrends_url, "shares_outstanding", "shares-outstanding")

    # combine dfs
    df = revenue_df.with_columns(gross_profit_df.get_column("gross_profit"),
                                 operating_income_df.get_column("operating_income"),
                                 ebitda_df.get_column("ebitda"),
                                 net_income_df.get_column("net_income"),
                                 eps_df.get_column("eps"),
                                 shares_outstanding_df.get_column("shares_outstanding"))

    # save df
    filepath = os.path.join("data", "quarterly_financials", ticker + "_quarterly_financials.csv")
    df.write_csv(filepath)


if __name__ == "__main__":
    collect_quarterly_historical('F')
    collect_quarterly_historical('AAPL')


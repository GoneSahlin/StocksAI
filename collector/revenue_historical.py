import os

from collector import utils


def get_url(ticker):
    url = utils.get_macrotrends_url(ticker)

    url += "revenue"

    return url


def get_data(url):
    df = utils.get_macrotrends_data(url, 1_000_000, "revenue")
        
    return df


def collect_revenue_historical(ticker):
    url = get_url(ticker)
    df = get_data(url)

    filepath = os.path.join("data", "revenues", ticker + "_revenues.csv")
    df.write_csv(filepath)


def main():
    collect_revenue_historical("F")
    collect_revenue_historical("AAPL")


if __name__ == "__main__":
    main()

import requests


def get_url(ticker):
    url = "https://www.macrotrends.net/stocks/charts/" + ticker

    # requesting adds the name of the company to the end of the url
    response = requests.get(url)
    url = response.url

    url += "revenue"

    return url


def get_page():
    pass



def collect_revenue_historical(ticker):
    pass


def main():
    collect_revenue_historical("F")


if __name__ == "__main__":
    main()

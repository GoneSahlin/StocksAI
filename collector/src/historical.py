import os

from src import price_historical, quarterly_financials_historical


def collect_historical(ticker):
    try:
        price_historical.collect_price_historical(ticker)
        print(ticker, "price")
        quarterly_financials_historical.collect_quarterly_historical(ticker)
        print(ticker, "quarterly")
    except:
        print("failed to collect", ticker)
        paths = []
        paths.append(os.path.join("data", "prices", ticker + "_prices.csv"))
        paths.append(os.path.join("data", "quarterly_financials", ticker + "_quarterly_financials.csv"))
        for path in paths:
            if os.path.exists(path):
                os.remove(path)


def main():
    filepath = os.path.join('data', 'tickers.txt')
    
    with open(filepath, 'r') as infile:
        tickers = infile.read().splitlines()

        for ticker in tickers:
            collect_historical(ticker)


if __name__ == '__main__':
    main()

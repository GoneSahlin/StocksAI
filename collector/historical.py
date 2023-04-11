from collector import price_historical, quarterly_financials_historical


def main():
    ticker = 'TSLA'
    price_historical.collect_price_historical(ticker)
    quarterly_financials_historical.collect_quarterly_historical(ticker)


if __name__ == '__main__':
    main()
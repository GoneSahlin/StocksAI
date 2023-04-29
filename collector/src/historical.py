import os
import s3fs

from src import price_historical, quarterly_financials_historical


s3_prefix = "s3://sahlin.stocksai"

def collect_historical(ticker, fs):
    try:
        price_df = price_historical.collect_price_historical(ticker)
        print(ticker, "price")
        quarterly_financials_df = quarterly_financials_historical.collect_quarterly_historical(ticker)
        print(ticker, "quarterly")
        
        price_historical.save_price_historical(price_df, ticker, fs, s3_prefix)
        quarterly_financials_historical.save_quarterly_historical(quarterly_financials_df, ticker, fs, s3_prefix)
    except:
        print("failed to collect", ticker)
        paths = []
        paths.append(os.path.join(s3_prefix, "prices", ticker + "_prices.csv"))
        paths.append(os.path.join(s3_prefix, "quarterly_financials", ticker + "_quarterly_financials.csv"))
        for path in paths:
            if os.path.exists(path):
                os.remove(path)


def collect_indexes(fs):
    filepath = os.path.join(s3_prefix, 'indexes.txt')
    
    with fs.open(filepath, 'r') as infile:
        tickers = infile.read().splitlines()

        for ticker in tickers:
            try:
                index_df = price_historical.collect_index_historical(ticker)
                price_historical.save_index_historical(index_df, ticker, fs, s3_prefix)
                print(ticker)
            except Exception as e:
                print(e)
                print("failed to collect", ticker)


def main():
    fs = s3fs.S3FileSystem()

    filepath = os.path.join(s3_prefix, 'tickers.txt')

    with fs.open(filepath, 'r') as infile:
        tickers = infile.read().splitlines()

        for ticker in tickers:
            collect_historical(ticker, fs)

    collect_indexes(fs)


if __name__ == '__main__':
    main()

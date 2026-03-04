import csv
import time
import random
import requests_cache
import yfinance as yf

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(2, Duration.SECOND * 5)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

EDGAR_BASE_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="


def create_full_list(list_of_symbols, name, sector):
    print("Retrieving stock data from Yahoo Finance...")
    # Initialize an empty list to store stock data
    stock_data = []

    # Loop over each stock symbol
    for idx, symbol in enumerate(list_of_symbols):
        stock = yf.Ticker(symbol, session=session)
        info = {}
        try:
            info = stock.info or {}
        except Exception as exc:
            print(f"Warning: failed to fetch data for {symbol}: {exc}")

        data = {
            "Symbol": symbol,
            "Name": name[idx],
            "Sector": sector[idx],
            "Price": info.get("currentPrice"),
            "Price/Earnings": info.get("trailingPE"),
            "Dividend Yield": info.get("dividendYield"),
            "Earnings/Share": info.get("trailingEps"),
            "52 Week Low": info.get("fiftyTwoWeekLow"),
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "Market Cap": info.get("marketCap"),
            "EBITDA": info.get("ebitda"),
            "Price/Sales": info.get("priceToSalesTrailing12Months"),
            "Price/Book": info.get("priceToBook"),
            "SEC Filings": f"{EDGAR_BASE_URL}{symbol}",
        }

        stock_data.append(data)

        # Delay
        time.sleep(1)

    if not stock_data:
        raise RuntimeError("No stock data could be retrieved")

    with open("../data/constituents-financials.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=stock_data[0].keys())
        writer.writeheader()
        writer.writerows(stock_data)
    print("Data has been written to constituents-financials.csv")


def process():
    print("Processing...")
    # List down all the symbols from the constituents.csv file
    with open("../data/constituents.csv") as f:
        reader = csv.reader(f)
        read_symbols = list(reader)

    list_of_symbols = [symbol[0] for symbol in read_symbols[1:]]
    name = [symbol[1] for symbol in read_symbols[1:]]
    sector = [symbol[2] for symbol in read_symbols[1:]]

    create_full_list(list_of_symbols, name, sector)
    print("Done!")


if __name__ == "__main__":
    process()

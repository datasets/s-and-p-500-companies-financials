import csv
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
    limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

EDGAR_BASE_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="

def create_full_list(list_of_symbols, name, sector):
    print("Retrieving stock data from Yahoo Finance...")
    # Initialize an empty list to store stock data
    stock_data = []
    
    # Loop over each stock symbol
    for symbol in list_of_symbols:
        stock = yf.Ticker(symbol, session=session)
        
        # Get the necessary data
        data = {
            "Symbol": symbol,
            "Name": name[list_of_symbols.index(symbol)],
            "Sector": sector[list_of_symbols.index(symbol)],
            "Price": stock.info.get('currentPrice'),
            "Price/Earnings": stock.info.get('trailingPE'),
            "Dividend Yield": stock.info.get('dividendYield'),
            "Earnings/Share": stock.info.get('trailingEps'),
            "52 Week Low": stock.info.get('fiftyTwoWeekLow'),
            "52 Week High": stock.info.get('fiftyTwoWeekHigh'),
            "Market Cap": stock.info.get('marketCap'),
            "EBITDA": stock.info.get('ebitda'),
            "Price/Sales": stock.info.get('priceToSalesTrailing12Months'),
            "Price/Book": stock.info.get('priceToBook'),
            'SEC Filings': f"{EDGAR_BASE_URL}{symbol}"
        }
        
        # Append the stock's data to the list
        stock_data.append(data)

    with open('../data/constituents-financials.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=stock_data[0].keys())
        writer.writeheader()
        writer.writerows(stock_data)
    print("Data has been written to constituents-financials.csv")

def process():
    print("Processing...")
    # List down all the symbols from the constituents.csv file
    with open('../data/constituents.csv') as f:
        reader = csv.reader(f)
        read_symbols = list(reader)

    list_of_symbols = [symbol[0] for symbol in read_symbols[1:]]
    name = [symbol[1] for symbol in read_symbols[1:]]
    sector = [symbol[2] for symbol in read_symbols[1:]]

    create_full_list(list_of_symbols, name, sector)
    print("Done!")
    

if __name__ == '__main__':
    process()

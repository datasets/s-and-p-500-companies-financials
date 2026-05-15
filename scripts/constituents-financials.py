import csv
import time
import yfinance as yf

EDGAR_BASE_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="


def create_full_list(list_of_symbols, name, sector):
    print("Retrieving stock data from Yahoo Finance...")
    stock_data = []

    for idx, symbol in enumerate(list_of_symbols):
        info = {}
        try:
            info = yf.Ticker(symbol).info or {}
        except Exception as exc:
            print(f"Warning: failed to fetch data for {symbol}: {exc}")

        # yfinance >=1.0 returns dividendYield as a percentage (e.g. 2.1 = 2.1%);
        # store as a decimal (e.g. 0.021) to match the declared schema format.
        div_yield = info.get("dividendYield")
        if div_yield is not None:
            div_yield = round(div_yield / 100, 6)

        data = {
            "Symbol": symbol,
            "Name": name[idx],
            "Sector": sector[idx],
            "Price": info.get("currentPrice"),
            "Price/Earnings": info.get("trailingPE"),
            "Dividend Yield": div_yield,
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
        time.sleep(0.5)

    if not stock_data:
        raise RuntimeError("No stock data could be retrieved")

    with open("../data/constituents-financials.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=stock_data[0].keys())
        writer.writeheader()
        writer.writerows(stock_data)
    print("Data has been written to constituents-financials.csv")


def process():
    print("Processing...")
    with open("../data/constituents.csv") as f:
        reader = csv.reader(f)
        read_symbols = list(reader)

    list_of_symbols = [row[0] for row in read_symbols[1:]]
    name = [row[1] for row in read_symbols[1:]]
    sector = [row[2] for row in read_symbols[1:]]

    create_full_list(list_of_symbols, name, sector)
    print("Done!")


if __name__ == "__main__":
    process()

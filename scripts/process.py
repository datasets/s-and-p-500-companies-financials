"""
    Retrieves stock market data and financials for the S&P 500
    Reads ..data/constituents.csv and writes ../data/constiuents-financials.csv

    Stock API are come and go.
    Presently, this uses the IEX Trading API by IEX Group, Inc.
    Data provided for free by IEX. https://iextrading.com/developer
"""

from dataflows import Flow, PackageWrapper, ResourceWrapper, validate
from dataflows import add_metadata, dump_to_path, load, set_type, printer
from collections import OrderedDict
from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import csv


EDGAR_BASE_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="

IEX_NUMBER_OF_SYMBOLS_PER_REQUEST = 100
IEX_BASE_URL = "https://api.iextrading.com/1.0/stock/market/batch"
IEX_TYPES_FIELDNAMES_TITLES = OrderedDict({
    "quote": [
        ["close", "Price"],
        ["peRatio", "Price/Earnings"]
    ],
    "stats": [
        ["dividendYield", "Dividend Yield"],
        ["latestEPS", "Earnings/Share"],
        ["week52high", "52 Week Low"],
        ["week52low", "52 Week High"],
        ["marketcap", "Market Cap"],
        ["EBITDA", "EBITDA"],
        ["priceToSales", "Price/Sales"],
        ["priceToBook", "Price/Book"]
    ]
})


def rename(package: PackageWrapper):
    package.pkg.descriptor['resources'][0]['name'] = 's-p-constituents'
    package.pkg.descriptor['resources'][0]['path'] = 'data/constituents.csv'
    package.pkg.descriptor['resources'][1]['name'] = 'constiuents-financials'
    package.pkg.descriptor['resources'][1]['path'] = 'data/constiuents-financials.csv'
    yield package.pkg
    res_iter = iter(package)
    for res in res_iter:
        yield res.it
    yield from package


def extract_constituents(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class": "wikitable sortable"})
    # Fail now if we haven't found the right table
    header = table.findAll('th')
    if header[0].string != "Ticker symbol" or header[1].string != "Security":
        raise Exception("Can't parse wikipedia's table!")

    # Retreive the values in the table
    rows = table.findAll('tr')
    for row in rows:
        fields = row.findAll('td')
        if fields:
            yield {
                'Symbol': fields[0].text,
                'Name': fields[1].text,
                'Sector': fields[3].text
            }


# helper function to append column data for each iex type and field pair
def append_column_data(rows, row_number, data_dict):
    for iex_type, field in IEX_TYPES_FIELDNAMES_TITLES.items():
        for field_name in field:
            rows[row_number].append(data_dict[iex_type][field_name[0]])


def extract_financial_data():
    # get constituents data
    reader = csv.reader(open('data/constituents.csv'))

    # gather field titles and IEX field names
    iex_fieldnames = []
    field_titles = []
    for iex_type in sorted(IEX_TYPES_FIELDNAMES_TITLES.values()):
        iex_fieldnames += [field[0] for field in iex_type]
        field_titles += [field[1] for field in iex_type]

    outrows = [row for row in reader]
    # add new column titles to outfile
    outrows[0] += field_titles + ['SEC Filings']
    # gather symbols
    symbols = [row[0] for row in outrows[1:]]
    # gather IEX "types"
    iex_types = IEX_TYPES_FIELDNAMES_TITLES.keys()
    # build first part of url, IEX uses comma delimiters between values
    url = IEX_BASE_URL + '?'
    url += 'types=' + ','.join(iex_types)
    url += '&filter=' + ','.join(iex_fieldnames)
    url += '&symbols='

    # make requests in chunks of symbols at a time
    # store response data in outrows
    for index in range(0, len(symbols), IEX_NUMBER_OF_SYMBOLS_PER_REQUEST):
        query = url + ','.join(symbols[index:index + IEX_NUMBER_OF_SYMBOLS_PER_REQUEST])
        results = requests.get(query).json()
        # loop over chunk results and store respective fields into outrows
        for count, stock in enumerate(results):
            outrows_index = index + count + 1
            # make sure we're updating the correct row
            assert(outrows[outrows_index][0] == stock)
            # append column data in order of IEX types and field_names
            append_column_data(outrows, outrows_index, results[stock])
            # append edgar url
            outrows[outrows_index].append(EDGAR_BASE_URL + stock)
            yield {
                'Symbol': outrows[outrows_index][0],
                'Name': outrows[outrows_index][1],
                'Sector': outrows[outrows_index][2],
                'Price': outrows[outrows_index][3],
                'Price/Earnings': outrows[outrows_index][4],
                'Dividend Yield': outrows[outrows_index][5],
                'Earnings/Share': outrows[outrows_index][6],
                '52 Week Low': outrows[outrows_index][7],
                '52 Week High': outrows[outrows_index][8],
                'Market Cap': outrows[outrows_index][0],
                'EBITDA': outrows[outrows_index][10],
                'Price/Sales': outrows[outrows_index][11],
                'Price/Book': outrows[outrows_index][12],
                'SEC Filings': outrows[outrows_index][13]
            }


html = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").read()
financial_data_flow = Flow(
    add_metadata(
        name="s-p-500-financial-data",
        title="S&P 500 Financial data",
        homepage='http://www.sec.gov',
        licenses=[
            {
                "id": "odc-pddl",
                "name": "public_domain_dedication_and_license",
                "version": "1.0",
                "url": "http://opendatacommons.org/licenses/pddl/1.0/"
            }
        ],
        version="0.2.0"
    ),
    extract_constituents(html),
    extract_financial_data(),
    rename,
    validate(),
    dump_to_path(),
)
financial_data_flow.process()

"""
    Retrieves stock market data and financials for the S&P 500
    Reads ..data/constituents.csv and writes ../data/constiuents-financials.csv

    Stock API are come and go.
    Presently, this uses the IEX Trading API by IEX Group, Inc.
    Data provided for free by IEX. https://iextrading.com/developer
"""

import urllib.request
from collections import OrderedDict
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

# get constituents data
reader = csv.reader(open('../data/constituents.csv'))

# gather field titles and IEX field names
iex_fieldnames = []
field_titles = []
for iex_type in sorted(IEX_TYPES_FIELDNAMES_TITLES.values()):
    iex_fieldnames += [ field[0] for field in iex_type ]
    field_titles += [ field[1] for field in iex_type ]

# start constructing output "outrows" using constituents file as a base
outrows = [ row for row in reader ]

# add new column titles to outfile
outrows[0] += field_titles + ['SEC Filings']

# gather symbols
symbols = [ row[0] for row in outrows[1:] ]

# gather IEX "types"
iex_types = IEX_TYPES_FIELDNAMES_TITLES.keys()

# build first part of url, IEX uses comma delimiters between values
url = IEX_BASE_URL + '?'
url += 'types=' + ','.join(iex_types)
url += '&filter=' + ','.join(iex_fieldnames)
url += '&symbols='

# helper function to append column data for each iex type and field pair
def append_column_data(row_number, data_dict):
    for iex_type, field in IEX_TYPES_FIELDNAMES_TITLES.items():
        for field_name in field:
            outrows[row_number].append(data_dict[iex_type][field_name[0]])

# make requests in chunks of symbols at a time
# store response data in outrows
for index in range(0, len(symbols), IEX_NUMBER_OF_SYMBOLS_PER_REQUEST):
    query = url + ','.join(symbols[index:index + IEX_NUMBER_OF_SYMBOLS_PER_REQUEST])
    resp = urllib.request.urlopen(query)
    # use ordered dict to keep results sorted in original order
    results = (json.loads(resp.readline().decode('utf-8'), object_pairs_hook=OrderedDict))

    # loop over chunk results and store respective fields into outrows
    for count, stock in enumerate(results):
        outrows_index = index + count + 1;
        # make sure we're updating the correct row
        assert(outrows[outrows_index][0] == stock)
        # append column data in order of IEX types and field_names 
        append_column_data(outrows_index, results[stock])
        # append edgar url
        outrows[outrows_index].append(EDGAR_BASE_URL + stock)

fo = open('../data/constituents-financials.csv', 'w')
writer = csv.writer(fo, lineterminator='\n')
writer.writerows(outrows)
fo.close()
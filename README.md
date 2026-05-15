<a className="gh-badge" href="https://datahub.io/core/s-and-p-500-companies-financials"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

List of companies in the S&P 500 (Standard and Poor's 500). The S&P 500 is a
free-float, capitalization-weighted index of the top 500 publicly listed stocks
in the US (top 500 by market cap). The dataset includes a list of all the
stocks contained therein and associated key financials such as price, market
capitalization, earnings, price/earnings ratio, price to book etc.

## Data

Information on S&P 500 index used to be available on the [official S&P website][sp-home]
but until they publish it back, Wikipedia is the best up-to-date and open data source.

* Index listing - see `data/constituents.csv` extracted from Wikipedia's [List of S&P 500 companies][sp-list]
* Constituent financials - see `data/constituents-financials.csv` (source via Yahoo Finance)
* Scatter plot data - see `data/scatter-data.csv` (derived from `constituents-financials.csv`; companies with positive P/E ≤ 100, market cap in USD billions)

Notes:

* In `constituents-financials.csv`, Market Cap and EBITDA are in raw USD (e.g. `83294183424` ≈ $83.3 billion). In `scatter-data.csv`, the `market_cap_b` column is in USD billions.
* Some financial fields (e.g. Dividend Yield, Earnings/Share, Price/Book) may be absent for certain companies where Yahoo Finance does not report a value.

[sp-home]: https://www.spindices.com/indices/equity/sp-500
[sp-list]: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies

*Note*: For aggregate S&P 500 data (dividends, earnings, etc), see the [Standard and Poor's 500 Dataset][shiller].

[shiller]: https://datahub.io/core/s-and-p-500

### Preparation

You can run the script yourself to update the data and publish them to GitHub: see [scripts README](https://github.com/datasets/s-and-p-500-companies-financials/blob/master/scripts/README.md).

## General Financial Notes

Publicly listed US companies are obliged to file various reports on a regular basis
with the SEC. Of these 2 types are of especial interest to investors and others
interested in their finances and business. These are:

* 10-K = Annual Report
* 10-Q = Quarterly report

## License

All data is licensed under the [Open Data Commons Public Domain Dedication and
License][pddl]. All code is licensed under the MIT/BSD license.

Note that while no credit is formally required, a link back or credit to [Rufus
Pollock](https://rufuspollock.com/) and the [Open Knowledge Foundation][okfn] is much appreciated.

[pddl]: http://opendatacommons.org/licenses/pddl/1.0/
[okfn]: https://okfn.org/

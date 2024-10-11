These **Linux** scripts scrape data from Wikipedia page about S&P500, computes a datapackage augmented with yahoo webservices 
then it publishes back on the very same git repository.

Data for `data/constituents-financials.csv` is parsed using yfinance library with the appropriate rate limiters.

They run with [github-actions](https://github.com/datasets/s-and-p-500-companies-financials/actions) every day or at each commit to update the data.


# Run the scripts

## Install the dependencies
The scripts work with some python and shell scripts glued together with a Makefile.

Install the required python libraries :

    cd scripts
    pip install -r requirements.txt

You can also work on a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) .

## Make the package and publish it
The purpose of the project is to compute the datapackage, to test it and to publish it to a git repository :

	make

## Only make the package locally and test it
If you work on the code, you might want to skip to publish step :

	make valid.txt

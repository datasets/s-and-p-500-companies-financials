import csv

from os import mkdir
from bs4 import BeautifulSoup
from os.path import exists, join

datadir = join('..', 'data')

if not exists(datadir):
    mkdir(datadir)
source_page = open('List_of_S%26P_500_companies.html').read()
soup = BeautifulSoup(source_page, 'html.parser')
table = soup.find("table", { "id" : "constituents" })

# Fail now if we haven't found the right table
header = [value.text.strip('\n') for value  in table.findAll('th')]

if header[0] != "Symbol" or header[1] != "Security":
    raise Exception("Can't parse wikipedia's table!")

# Retreive the values in the table
records = []
rows = table.findAll('tr')
for row in rows:
    fields = row.findAll('td')
    if fields:
        symbol = fields[0].text
        name = fields[1].text
        sector = fields[3].text
        records.append([symbol.strip('\n'), name, sector])

header = ['Symbol', 'Name', 'Sector']
records.sort(key=lambda s: s[1].lower())

with open('../data/constituents.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(records) 

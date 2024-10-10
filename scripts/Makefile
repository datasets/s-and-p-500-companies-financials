all: valid.txt

List_of_S%26P_500_companies.html:
	curl -o List_of_S%26P_500_companies.html "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

../data:
	mkdir ../data    
    
../data/constituents.csv: ../data List_of_S%26P_500_companies.html constituents.py
	python constituents.py

../data/constituents-financials.csv: ../data ../data/constituents.csv constituents-financials.py
	python constituents-financials.py

valid.txt: ../data/constituents.csv ../data/constituents-financials.csv ../datapackage.json validate.py
	python validate.py
	echo "Datapackage is valid" > valid.txt

.PHONY: all
# MCC-MNC-Parser

This is a parser which creates a CSV file containing the information
about the MCC and MNC as provided by the Wikipedia
page at https://en.wikipedia.org/wiki/Mobile_country_code.

The parser was inspired by https://github.com/pbakondy/mcc-mnc-list,
but was rewritten in python.

## Installation and Usage

The script itself doesn't need to be installed at all.
However the following python packages have to be installed on the machine:

* argparse
* argcomplete
* beautifulsoup4

### Usage:
```bash
# show help
./parse-mcc.py -h

# create the csv
./parse-mcc.py -o /some/where/mcc-mnc-list.csv

# create the csv with a header
./parse-mcc.py -o /some/where/mcc-mnc-list.csv --csv-header
```

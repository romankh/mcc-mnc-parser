#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argcomplete
import argparse
import csv
import urllib2
from bs4 import BeautifulSoup

wiki_url = "https://en.wikipedia.org/wiki/Mobile_country_code"
csv_header_data = ["MCC", "MNC", "Country", "Country Code", "Brand", "Operator", "Status", "Bands", "Note"]


def handle_h2(mode):
    if mode == "":
        return "testnetworks", "Test Networks", ""
    elif mode == "testnetworks":
        return "nationaloperators", "", ""
    else:
        return "internationaloperators", "International Operators", ""


def parse_h3_tag(country_tag):
    country_parts = country_tag["id"]
    country_parts = country_parts.replace("_", " ")
    country_parts = country_parts.replace(".27", "'").replace(".28", "(").replace(".29", ")")
    country_parts = country_parts.replace(".2C", ",").replace(".2F", "/")
    country_parts = country_parts.split("-", 1)

    country = country_parts[0].strip().encode("UTF-8")
    if len(country_parts) > 1:
        country_code = country_parts[1].strip().encode("UTF-8")
    else:
        country_code = ""
    return country, country_code


def parse_table(element):
    rows = element.find_all("tr")
    row_entries = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            mcc = parse_td(cells[0]).encode("UTF-8")
            mnc = parse_td(cells[1]).encode("UTF-8")
            if len(mcc) > 0 and len(mnc) > 0:
                brand = parse_td(cells[2]).encode("UTF-8")
                operator = parse_td(cells[3]).encode("UTF-8")
                status = parse_td(cells[4]).encode("UTF-8")
                bands = parse_td(cells[5]).encode("UTF-8")
                note = parse_td(cells[6]).encode("UTF-8")
                row_entries.append([mcc, mnc, country, country_code, brand, operator, status, bands, note])
    return row_entries


def parse_td(td):
    [sup.extract() for sup in td.find_all("sup")]

    anchor = td.find("a")
    if anchor is not None:
        return anchor.string
    elif td.string is not None:
        return td.string
    else:
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch MCC and MNC from wikipedia to a csv file.")
    parser.add_argument('-o', action="store", dest="csv_file", help="Output file in csv format.",
                        type=argparse.FileType("w"), default="/tmp/mcc-mnc.csv")
    parser.add_argument('--csv-header', action="store_true", dest="write_header", help="Write header to csv file.",
                        default=False)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    csv_file = args.csv_file
    write_header = args.write_header

    print("Fetching wikipedia page...")
    response = urllib2.urlopen(wiki_url)
    html = response.read()

    print("Processing...")
    html_soup = BeautifulSoup(html, "lxml")
    content_container = html_soup.find(id="mw-content-text")
    content = content_container.find("div", {"class" : "mw-parser-output"})

    mode = ""
    country = ""
    country_code = ""

    counter = 0
    try:
        writer = csv.writer(csv_file, delimiter=";")
        if write_header:
            writer.writerow(csv_header_data)

        for element in content:
            if element.name == "h2":
                mode, country, country_code = handle_h2(mode)
            elif element.name == "h3" and mode == "nationaloperators":
                country_tag = element.find("span", class_="mw-headline")
                if country_tag is not None:
                    country, country_code = parse_h3_tag(country_tag)
            elif element.name == "table":
                csv_data = parse_table(element)
                counter += len(csv_data)
                for csv_data_row in csv_data:
                    writer.writerow(csv_data_row)
    finally:
        print("Finished. %s entries written." % counter)
        csv_file.close()

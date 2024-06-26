from numpy import rec
from rightmove_webscraper import RightmoveData
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import exists
from openrentScraper import write_seen_listing


def write_url(url):
    textfile = open("seen_urls.txt", "a")
    textfile.write(url + "\n")
    textfile.close()


def read_urls():

    if exists("seen_urls.txt"):
        textfile = open("seen_urls.txt", "r")
        urls = textfile.read()
        urls_list = urls.split("\n")
        textfile.close()
        return urls_list

    else:
        return list()


def get_rightmove_data(url, max_price_pp):

    seen_urls = read_urls()
    rm = RightmoveData(url)
    results = rm.get_results
    results["price_pp"] = round(results["price"] / results["number_bedrooms"])
    results = results.query(f"(price_pp <= {max_price_pp}) & ~(url in {seen_urls})")
    results = results.sort_values(by=["price_pp"], ascending=False)
    results = results.drop_duplicates()
    print(results.head())

    return results

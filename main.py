from rightmoveScraper import *
import os

url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=STATION%5E10022&insId=1&radius=1.0&minPrice=&maxPrice=1750&minBedrooms=1&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare='
max_price_pp = 1000

sender = os.environ.get('EMAIL_SENDER')
receivers = os.environ.get('EMAIL_RECEIVERS')
password = os.environ.get('EMAIL_PASS')

send_results(url, max_price_pp, sender, receivers, password)

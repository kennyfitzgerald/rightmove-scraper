from rightmoveScraper import *
import os

url = 'rightmove.co.uk/property-to-rent/find.html?locationIdentifier=STATION%5E341&maxBedrooms=3&minBedrooms=3&maxPrice=2500&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
max_price_pp = 1000

sender = os.environ.get('EMAIL_SENDER')
receivers = os.environ.get('EMAIL_RECEIVERS')
password = os.environ.get('EMAIL_PASS')

send_results(url, max_price_pp, sender, receivers, password)

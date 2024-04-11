from rightmoveScraper import *
from telegram import *
import os

url = 'https://rightmove.co.uk/property-to-rent/find.html?locationIdentifier=STATION%5E341&maxBedrooms=3&minBedrooms=3&maxPrice=2500&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
max_price_pp = 1000

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

rightmove_data = get_rightmove_data(url, max_price_pp)

send_to_telegram(rightmove_data, TELEGRAM_API_KEY, TELEGRAM_CHAT_ID)

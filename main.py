from rightmoveScraper import *
from telegram import *
from google_sheet import *
import os

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
GSHEETS_RIGHTMOVE_SHEET_ID = os.environ.get("GSHEETS_RIGHTMOVE_SHEET_ID")
GSHEETS_GID = 0

configs = google_sheet_to_json(GSHEETS_RIGHTMOVE_SHEET_ID, GSHEETS_GID)

for config in configs:
    url = config["rightmove_url"]
    max_price_pp = config["max_price_pp"]
    telegram_chat_ids = config["telegram_chat_ids"]
    description = config["description"]

    rightmove_data = get_rightmove_data(url, max_price_pp)
    send_to_telegram(rightmove_data, TELEGRAM_API_KEY, telegram_chat_ids, description)

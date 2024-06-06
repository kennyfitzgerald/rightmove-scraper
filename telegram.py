import requests
import time
from openrentScraper import write_seen_listing


def build_html(df):
    results = []

    for row in range(len(df)):
        link = (f'<a href="{df.iloc[row]["url"]}">'
                f'{df.iloc[row]["number_bedrooms"]} Bed, '
                f'{round(df.iloc[row]["price_pp"])} PP, '
                f'{df.iloc[row]["address"]}</a>')
        results.append((link, df.iloc[row]['url']))

    return list(set(results))


def chat_ids_to_list(chat_ids):
    return str(chat_ids).split(",")


def send_to_telegram(data, api_key, chat_id, description, site):

    apiURL = f"https://api.telegram.org/bot{api_key}/sendMessage"

    if len(data) == 0:
        return "No new results."

    if site == 'rightmove':
        results = build_html(data)
        textfile = 'seen_urls.txt'
    if site == 'openrent':
        results = list(zip(data['HTML'], data['id']))
        textfile = 'openrent_seen_listings.txt'

    chat_ids_list = chat_ids_to_list(chat_id)
    for chat_id in chat_ids_list:
        for message, id in results:
            message = f"New Result for {site} search: {description}\n\n" + message
            try:
                response = requests.post(
                    apiURL,
                    json={"chat_id": chat_id, "text": message, "parse_mode": "html"},
                )
                print(response.text)
                write_seen_listing(id, textfile)
                time.sleep(3)

            except Exception as e:
                print(e)
                time.sleep(45)

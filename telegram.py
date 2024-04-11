import requests
import string
import os


def build_html(df):

    results = []

    for row in range(0, len(df)):
        link = f"<a href=\"{df.iloc[row]['url']}\">{df.iloc[row]['number_bedrooms']} Bed, {round(df.iloc[row]['price_pp'])} PP, {df.iloc[row]['address']}</a>"
        results.append(link)

    return list(set(results))


def chat_ids_to_list(chat_ids):
    return str(chat_ids).split(",")


def send_to_telegram(data, api_key, chat_id, description):

    apiURL = f"https://api.telegram.org/bot{api_key}/sendMessage"

    if len(data) == 0:
        return "No new results."

    messages = build_html(data)

    chat_ids_list = chat_ids_to_list(chat_id)
    for chat_id in chat_ids_list:
        for message in messages:
            message = f"New Result for search: {description}\n\n" + message
            try:
                response = requests.post(
                    apiURL,
                    json={"chat_id": chat_id, "text": message, "parse_mode": "html"},
                )
                print(response.text)
            except Exception as e:
                print(e)

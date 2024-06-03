from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dateutil import parser

import re
import time
from bs4 import BeautifulSoup
from re import S, sub
from datetime import datetime
from os.path import exists
import pandas as pd

URL_BASE = "https://www.openrent.co.uk/"
URL_ENDPOINT = "https://www.openrent.co.uk/properties-to-rent/"
ADVERTS_URLS_SELECTOR = "a.pli.clearfix"
MAPS_XPATH_SELECTOR = "/html/body/div[4]/div[2]/section/div[2]/div/div/div/div/div[1]/div[5]/div/div[1]/img[1]"


def get_driver():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    return driver


def get_page(driver, url):

    driver.get(url)
    pre_scroll_height = driver.execute_script("return document.body.scrollHeight;")
    run_time, max_run_time = 0, 1
    while True:
        iteration_start = time.time()
        # Scroll webpage, the 100 allows for a more 'aggressive' scroll
        driver.execute_script("window.scrollTo(0, 100*document.body.scrollHeight);")
        post_scroll_height = driver.execute_script("return document.body.scrollHeight;")
        scrolled = post_scroll_height != pre_scroll_height
        timed_out = run_time >= max_run_time
        if scrolled:
            run_time = 0
            pre_scroll_height = post_scroll_height
        elif (not scrolled) & (not timed_out):
            run_time += time.time() - iteration_start
        elif not scrolled & timed_out:
            break

    html = driver.page_source
    page = BeautifulSoup(html, features="lxml")
    driver.refresh()
    time.sleep(1)

    return page


def extract_listing_id(html):

    for div in html.find_all("div"):
        if div.get("data-listing-id"):
            listing_id = int(div.get("data-listing-id"))
            break
    return listing_id


def get_let_agreed(html):

    let_agreed = len(html.find_all("span", {"class": "let-agreed"})) == 1
    return let_agreed


def get_price_pm(html):
    price_element = html.find("h2")
    price_text = price_element.get_text(strip=True)
    price_per_month = re.search(r"£([\d,]+)", price_text)
    if not price_per_month:
        return None
    price_per_month = price_per_month.group(1).replace(",", "")
    return float(price_per_month)


def get_listing_title(html):

    title_element = html.find("span", class_="banda pt listing-title")
    if title_element is None:
        return ""
    listing_title = title_element.get_text(strip=True)
    return listing_title


def extract_bedrooms(title):

    if "Room in a Shared House" in title or "Room in a Shared Flat" in title:
        bedrooms = 1
    else:
        match = re.search(r"(\d+) Bed", title)
        if match:
            bedrooms = int(match.group(1))
        else:
            bedrooms = 0
    return bedrooms


def get_listing_ids(page):
    listing_html = page.select(ADVERTS_URLS_SELECTOR)
    
    def process_listing(html):
        listing_id = extract_listing_id(html)
        let_agreed = get_let_agreed(html)
        price_pm = get_price_pm(html)
        title = get_listing_title(html)
        bedrooms = extract_bedrooms(title)
        price_pp = price_pm / bedrooms if price_pm and bedrooms > 0 else None
        
        return {
            "listing_id": listing_id,
            "let_agreed": let_agreed,
            "price_pm": price_pm,
            "title": title,
            "bedrooms": bedrooms,
            "price_pp": price_pp
        }
    
    return [process_listing(html) for html in listing_html]


def read_seen_listings(filepath):

    if exists(filepath):
        textfile = open(filepath, "r")
        listing_ids = textfile.read()
        listing_ids = listing_ids.split("\n")
        textfile.close()
        return listing_ids

    return list()


def filter_seen_listings(listing_ids, filepath):

    seen_listing_ids = read_seen_listings(filepath)
    filtered_listing_ids = [
        x for x in listing_ids if str(x["listing_id"]) not in seen_listing_ids
    ]
    return filtered_listing_ids


def filter_let_agreed(listing_ids):

    filtered_listing_ids = [
        x for x in listing_ids if not bool(x["let_agreed"])
    ]
    return filtered_listing_ids


def filter_price(listing_ids, max_price_pp):
    return [x for x in listing_ids if x.get("price_pp") is not None and x["price_pp"] <= max_price_pp]


def apply_listing_filters(listing_ids, filepath, max_price_pp):

    listing_ids = filter_seen_listings(listing_ids, filepath)
    listing_ids = filter_let_agreed(listing_ids)
    listing_ids = filter_price(listing_ids, max_price_pp)
    return listing_ids

def get_listing_details(driver, listing_id):

    def _extract_bool_from_html(html_list, ind):

        html = html_list[ind].find("i")["class"]
        bool = " ".join(html) != "fa fa-times"

        return bool

    url = f"{URL_BASE}{listing_id}"

    driver.get(url)
    driver.implicitly_wait(2)

    time.sleep(1.5)
    result = None
    response = driver.page_source

    soup = BeautifulSoup(response, features="lxml")

    title = soup.find_all("h1", {"class": "property-title"})[0].string

    overview = soup.find_all("table", {"class": "table table-striped intro-stats"})[0]
    bedrooms, bathrooms, max_tenants, location = [
        x.string for x in overview.find_all("strong")
    ]
    bedrooms = int(bedrooms)
    bathrooms = int(bathrooms)
    max_tenants = int(max_tenants)
    description = soup.find_all("div", {"class": "description"})[0].text

    features = soup.find_all("table", {"class": "table table-striped"})
    price_bills = features[0].find_all("td")
    deposit = float(sub(r"[^\d.]", "", price_bills[1].text))
    rent_total = float(sub(r"[^\d.]", "", price_bills[3].text))
    bills_included = _extract_bool_from_html(price_bills, 5)

    tenant_preference = features[1].find_all("td")
    student_friendly = _extract_bool_from_html(tenant_preference, 1)
    families_allowed = _extract_bool_from_html(tenant_preference, 3)
    pets_allowed = _extract_bool_from_html(tenant_preference, 5)
    smokers_allowed = _extract_bool_from_html(tenant_preference, 7)
    dss_lha_covers_rent = _extract_bool_from_html(tenant_preference, 9)

    availability = features[2].find_all("td")
    available_from = availability[1].text
    available_from_ts = (
        datetime.now() if available_from == "Today" else parser.parse(available_from)
    )
    available_from_ts = str(available_from_ts.date())
    minimum_tenancy = availability[3].text

    additional_features = features[3].find_all("td")
    has_garden = _extract_bool_from_html(additional_features, 1)
    has_parking = _extract_bool_from_html(additional_features, 3)
    has_fireplace = _extract_bool_from_html(additional_features, 5)
    furnished = additional_features[7].text
    epc_rating = additional_features[9].text

    try:
        transport = [
            x.text.replace("\r", "").replace("\n", "").strip()
            for x in soup.find_all("table", {"class": "table table-striped mt-1"})[
                0
            ].find_all("td", text=True)
        ]
    except:
        transport = list()

    try:
        closest_station = transport[2]
        closest_station_mins = int(transport[3].split(" ")[0])
    except:
        closest_station = ""
        closest_station_mins = None

    try:
        second_closest_station = transport[4]
        second_closest_station_mins = int(transport[5].split(" ")[0])
    except:
        second_closest_station = ""
        second_closest_station_mins = None

    room_only = title.split(",")[0] in [
        "Room in a Shared House",
        "Room in a Shared Flat",
    ]
    rent_per_person = (
        round(rent_total / int(bedrooms), 2) if not room_only else rent_total
    )

    listing_details = {
        "id": listing_id,
        "title": title,
        "room_only": room_only,
        "rent_per_person": rent_per_person,
        "location": location,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "max_tenants": max_tenants,
        "description": description,
        "deposit": deposit,
        "rent_total": rent_total,
        "bills_included": bills_included,
        "student_friendly": student_friendly,
        "families_allowed": families_allowed,
        "pets_allowed": pets_allowed,
        "smokers_allowed": smokers_allowed,
        "dss_1ha_covers_rent": dss_lha_covers_rent,
        "available_from": available_from,
        "available_from_ts": available_from_ts,
        "minimum_tenancy": minimum_tenancy,
        "has_garden": has_garden,
        "has_parking": has_parking,
        "has_fireplace": has_fireplace,
        "furnished": furnished,
        "epc_rating": epc_rating,
        "closest_station": closest_station,
        "closest_station_mins": closest_station_mins,
        "second_closest_station": second_closest_station,
        "second_closest_station_mins": second_closest_station_mins,
    }

    return listing_details


def get_all_results(driver, listing_ids):

    results = [
        get_listing_details(driver, x["listing_id"])
        for x in listing_ids
    ]
    results = add_html_info(results)
    return results


def write_seen_listings(results, filepath):

    listing_ids = [result["id"] for result in results]

    textfile = open(filepath, "a")
    for id in listing_ids:
        textfile.write(str(id) + "\n")
    textfile.close()


def add_html_info(results):

    for item in results:
        item['HTML'] = f"""<b>Title:</b> <a href="https://www.openrent.co.uk/{item['id']}">{item['title']}</a>\n<b>Rent:</b> {item['rent_total']}\n<b>Rooms:</b> {item['bedrooms']}\n<b>Closest Station:</b> {item['closest_station']} ({item['closest_station_mins']} minutes)\n<b>Available From:</b> {item['available_from_ts']}\n<b>Has Garden:</b> {item['has_garden']}"""
    return results

def get_openrent_data(url, max_price_pp):

    driver = get_driver()
    page = get_page(driver, url)
    listing_ids = get_listing_ids(page)
    listing_ids = apply_listing_filters(listing_ids, "openrent_seen_listings.txt", max_price_pp)
    results = get_all_results(driver, listing_ids)
    write_seen_listings(results, "openrent_seen_listings.txt")
    return pd.DataFrame(results)

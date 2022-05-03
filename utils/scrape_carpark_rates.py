from bs4 import BeautifulSoup
import requests
import json
import time
from datetime import datetime

count = 1
invalid_count = 0
BASE_URL = "https://www.sgcarmart.com/news/carpark_mobile.php?TYP=carpark&CPK="
ALL_CARPARKS = []


def deCFEmail(fp):
    try:
        r = int(fp[:2], 16)
        email = "".join([chr(int(fp[i : i + 2], 16) ^ r) for i in range(2, len(fp), 2)])
        return email
    except (ValueError):
        return fp


def scrape_one():
    global invalid_count
    website_data = requests.get(f"{BASE_URL}{count}")
    if website_data.status_code == 429:
        print("rate limit")
        invalid_count += 1
        return None
    soup = BeautifulSoup(website_data.text, "html.parser")
    main_body = soup.find("div", class_="mainmargin")
    if len(main_body.contents) == 1:
        print("invalid")
        invalid_count += 1
        return None

    # Carpark Name and Address
    carpark_name = (
        main_body.find("strong").text
        if not main_body.find("strong").text == "[email\xa0protected]"
        else deCFEmail(main_body.find("strong").find("a").attrs["data-cfemail"])
    )
    carpark_address = main_body.find("span").text

    rates_body = main_body.find_all("div")[1]
    all_rates = rates_body.find_all("p")
    rate_list = {}
    for rate in all_rates:
        d = rate.find("b").text
        e = rate.contents[-1].text
        rate_list[d] = e

    final_dict = {
        "carparkName": carpark_name,
        "carparkAddress": carpark_address,
        "rates": rate_list,
    }
    ALL_CARPARKS.append(final_dict)
    invalid_count = 0
    print(final_dict)
    return True


start_time = datetime.now()
for i in range(count, 2000):
    if scrape_one():
        time.sleep(0.5)
    else:
        if invalid_count > 20:
            break
    count += 1
    print(count)
print(datetime.now() - start_time)

carparks_json = {
    "timestamp": datetime.now().isoformat(),
    "data": ALL_CARPARKS,
}
f = open("CarparkRates.json", "w")
f.write(json.dumps(carparks_json))
f.close()

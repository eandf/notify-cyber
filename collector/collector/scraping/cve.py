import requests
from bs4 import BeautifulSoup
import random
import time
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import util
import log


def read_json(path):
    # ignore any unencodable character (skip unencodable characters)
    with open(str(path), errors="ignore") as file:
        content = json.load(file)
    return content


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG = read_json(os.path.join(FILE_PATH, "../../config.json"))["collector"]["cve"]
ROOT_URL = CONFIG["root_url"]
PAGES_TO_SCRAPE = 15


def fetch_cve_data(pages):
    base_url = "https://www.tenable.com/cve/newest?page={}"
    cve_data = []

    for page in range(1, pages + 1):
        url = base_url.format(page)
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.find_all("tr")

            for row in rows[1:]:  # Skip the header row
                cols = row.find_all("td")

                if len(cols) > 2:
                    cve_id = cols[0].text.strip()
                    description = cols[1].text.strip()
                    severity = cols[2].text.strip()

                    cve_data.append(
                        {"id": cve_id, "description": description, "severity": severity}
                    )

        # if response.status_code != 200:
        #     print(f"Failed to retrieve the web page for page {page}. Status code: {response.status_code}")

        # delay before starting a new scrape
        if page < pages:
            delay_seconds = round(random.uniform(1.5, 3), 2)
            log.info(
                f"(page {page} / {pages}) Pausing for {delay_seconds} seconds before scrapping the next CVE page scrape"
            )
            time.sleep(delay_seconds)

    return cve_data


def cve_get():
    cdata = []

    try:
        all_cve_data = fetch_cve_data(PAGES_TO_SCRAPE)

        cleaned_data = {}
        for entry in all_cve_data:
            key = entry["id"]
            cleaned_data[key] = entry
            cleaned_data[key]["url"] = f"https://www.tenable.com/cve/{key}"

        cdata = []
        for code in cleaned_data:
            cdata.append(
                {
                    "source": "cve",
                    "url": f"{ROOT_URL}{code}",
                    "title": code,
                    "date": str(cleaned_data[code]["url"].split("-")[1]),
                    "recorded": str(int(time.time())),
                    "details": cleaned_data[code]["description"],
                    "html": json.dumps(
                        {
                            "severity": cleaned_data[code]["severity"],
                            "original_url": cleaned_data[code]["url"],
                        }
                    ),
                }
            )
    except requests.exceptions.Timeout as err:
        log.error(str(cve_get.__name__) + "() error : " + str(err))
        cdata = []
    except Exception as err:
        log.error(str(cve_get.__name__) + "() error : " + str(err))
        cdata = []

    return cdata

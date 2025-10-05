from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json

# global/configurable variables
URL = "https://support.apple.com/en-us/HT201222"


def date_to_epoch(timestamp):
    try:
        dt_obj = datetime.strptime(timestamp, "%d %b %Y")
        epoch_time = int(dt_obj.timestamp())
        return epoch_time
    except:
        return None


def apple_get():
    global URL

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("div", id="tableWraper")

    array_of_objects = []
    headers = [
        header.text.strip().replace("\u00a0", " ") for header in table.find_all("th")
    ]
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if cells:
            obj = {}
            for i, cell in enumerate(cells):
                # extract text
                cell_text = cell.text.strip().replace("\u00a0", " ")
                obj[headers[i]] = cell_text

                # extract link if present
                link = cell.find("a")
                if link and link.get("href"):
                    obj[headers[i] + " Link"] = link.get("href")

            array_of_objects.append(obj)

    output = []
    for entry in array_of_objects:
        info = entry.get("Name and information link")
        msg = ""
        if info != None and "\n" in info:
            info = info.split("\n")
            msg = info[1:]
            info = info[0]

        # skip any posts with no URL
        url = entry.get("Name and information link Link")
        if url == None:
            continue

        # skip any posts with no date
        date = entry.get("Release date")
        if date == None:
            continue

        # date: January 21, 2024
        # about: we only want posts after 1-1-2023 and onwards!
        # note: 1672531200 seconds (Epoch) = Sunday, January 1, 2023 12:00:00 AM (GMT)
        date_epoch = date_to_epoch(date)
        if date_epoch == None or date_epoch < 1672531200:
            continue

        output.append(
            {
                "url": url,
                "title": info,
                "date": date,
                "details": entry.get("Available for"),
                "html": {"raw": entry, "msg": msg, "epoch": date_to_epoch(date)},
            }
        )

    # sort by recorded date (epoch) in ascending order
    sorted_data = sorted(output, key=lambda x: x["html"]["epoch"])
    for entry in sorted_data:
        # (1-21-2024) set all "html" values to None, the collector needs a complete rewrite
        entry["html"] = None

    return sorted_data

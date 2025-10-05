from time import strftime, localtime
from bs4 import BeautifulSoup
import requests
import string
import time
import json
import ast
import re
from datetime import datetime, timedelta
import requests
import string
import re
import ast

"""
ABOUT:      Microsoft Vulnerability List
URL:        https://msrc.microsoft.com/update-guide/vulnerability
EXAMPLE:    https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability?$orderBy=cveNumber+desc&$filter=(releaseDate+gt+2023-02-15T00:00:00-07:00+or+latestRevisionDate+gt+2023-02-15T00:00:00-07:00)+and+(releaseDate+lt+2023-03-15T23:59:59-06:00+or+latestRevisionDate+lt+2023-03-15T23:59:59-06:00)
DATE:       3-15-2023
"""


def clean_html(content):
    oline = content
    soup = BeautifulSoup(oline, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    tmp = " ".join(soup.stripped_strings)
    tmp = "".join(filter(lambda x: x in set(string.printable), tmp))
    tmp = re.sub(" +", " ", tmp)
    return tmp


def raw_mv_get():
    # use UTC for all times
    utc_now = datetime.utcnow()
    utc_two_weeks_ago = utc_now - timedelta(days=14)

    # format the time in a consistent way
    start_time = (
        utc_two_weeks_ago.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    )  # Add 'Z' to indicate UTC
    end_time = utc_now.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

    url = "https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability?$orderBy=cveNumber+desc&$filter=(releaseDate+gt+{}+or+latestRevisionDate+gt+{})+and+(releaseDate+lt+{}+or+latestRevisionDate+lt+{})".format(
        start_time, start_time, end_time, end_time
    )

    output = None
    try:
        response = requests.get(url)
        response = response.json()

        ## (4-13-2024) Fix a bug that effected scrapping
        # response = clean_html(str(response))
        # response = ast.literal_eval(response)

        output = response
    except Exception as err:
        print("error : {}".format(err))
        output = None

    return output


def microsoft_get():
    try:
        data = raw_mv_get()
        if data == None:
            return None

        root_url = "https://msrc.microsoft.com/update-guide/vulnerability/"
        output = []
        for entry in data["value"]:
            url = None
            if entry.get("cveNumber") != None:
                url = root_url + str(entry["cveNumber"])
            output.append(
                {
                    "url": url,
                    "title": entry.get("cveTitle"),
                    "date": entry.get("releaseNumber"),
                    "details": entry.get("description"),
                    "html": {"raw": entry, "root_url": root_url},
                }
            )

        # (1-22-2024) clean output; it's not ideal but it saves space...
        for entry in output:
            entry["html"] = None
            entry["details"] = ""

        return output
    except:
        return None

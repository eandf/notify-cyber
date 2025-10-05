"""
PLEASE READ

February 11, 2024

This scrapper no longer worked becaue tlix,
switched from using raw HTML to using,
JavaScript call(s). A fix is needed but is,
not available at the moment...
"""

from urllib.parse import unquote
import requests
import time
import json
import copy
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import log
import util

# configuration values
BASE_ROOT_URL = "https://www.trellix.com"
HTTP_GET_TIMEOUT_SECS = 20
ONE_DAY_IN_SECONDS = 24 * 60 * 60


def get_url():
    # # (2-10-2024) DEPRECATED
    # url = f"{BASE_ROOT_URL}/corpcomsvc/topicslisting?q=&newsPagePath=/content/mainsite/en-us/about/newsroom/stories/research&_={time.time()}"

    url = f"{BASE_ROOT_URL}/corpcomsvc/topicslisting?q=&newsPagePath=/content/mainsite/en-us/blogs/research&_={time.time()}"

    return url


def decode(line):
    return unquote(line).encode("utf8").decode("unicode_escape")


def key_value_decode(obj, skip_list=[]):
    output = copy.deepcopy(obj)
    for key in output:
        if str(key) in skip_list:
            continue
        output[key] = decode(output[key])
    return output


# global variable
LAST_COLLECTION = -1
LAST_OUTPUT = []


def tlix_get():
    global LAST_COLLECTION
    global LAST_OUTPUT

    current_time = time.time()

    # check if the last collection was more than a day ago
    if LAST_COLLECTION >= 0 and (current_time - LAST_COLLECTION) <= ONE_DAY_IN_SECONDS:
        log.info(
            f"[Tlix] skipping tlix collection because the last collection occurred on {LAST_COLLECTION} and it's currently {time.time()}, the difference in time most be over {ONE_DAY_IN_SECONDS} seconds"
        )

        # TODO: just return previous out until enough time passes by
        return LAST_OUTPUT

    output = []

    try:
        response = requests.get(get_url(), timeout=HTTP_GET_TIMEOUT_SECS)
        if response.status_code == 200:
            response = response.json()["topics"]
        else:
            log.error(
                "[Tlix] HTTP request failed with status code: "
                + str(response.status_code)
            )
            return output
    except Exception as e:
        log.error("[Tlix] Exception in HTTP request: " + str(e))
        return output

    for entry in response:
        try:
            entry = key_value_decode(entry, ["title"])

            sub_url = entry.get("url")
            if sub_url is None:
                print(f"ERROR: The entry {entry} does not have a URL")
                continue

            output.append(
                {
                    "url": BASE_ROOT_URL + sub_url,
                    "title": entry.get("title"),
                    "date": entry.get("releaseDate"),
                    # "recorded": current_time,
                    "details": entry.get("summary"),
                    "html": None,
                }
            )
        except Exception as err:
            log.error(f"[Tlix] {tlix_get.__name__}() error: {err}")

    LAST_COLLECTION = current_time
    LAST_OUTPUT = output

    return output

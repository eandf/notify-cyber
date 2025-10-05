from datetime import datetime
from bs4 import BeautifulSoup
import requests
import string
import json
import time
import log
import re
import os

CONFIG_PATH = str(os.path.dirname(os.path.realpath(__file__))) + "/../config.json"


def read_json(path):
    with open(str(path)) as file:
        content = json.load(file)
    return content


def read_file(path):
    with open(str(path)) as file:
        content = file.readlines()
    content = [i.strip() for i in content]
    return content


def valid_url_format(url):
    if type(url) != str:
        return False
    # https://stackoverflow.com/a/7160778
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


CONFIG_VALID_KEYS = read_json(CONFIG_PATH)["database"]["columns"]


def valid_scrape(content):
    if type(content) != list:
        log.error(
            "the data (first layer) is not type list but instead type "
            + str(type(content))
        )
        return False

    if len(content) == 0:
        log.error("data has zero entries (size of list/array is zero)")
        return False

    validKeys = CONFIG_VALID_KEYS
    for entry in content:
        if type(entry) != dict:
            log.error(
                "the entry "
                + str(entry)
                + " in the data is type "
                + str(type(entry))
                + " when it should be of type dict"
            )
            return False

        for key in entry:
            if type(entry[key]) != str and entry[key] != None:
                log.error(
                    "the key "
                    + str(key)
                    + " in entry "
                    + str(entry)
                    + " is type "
                    + str(type(entry[key]))
                    + " when it should be type str or equal to None"
                )
                return False

            if key == "url" and valid_url_format(entry[key]) == False:
                log.error(
                    "the url key in entry "
                    + str(entry)
                    + " is not a valid url: "
                    + str(entry[key])
                )
                return False

            if key not in validKeys:
                log.error(
                    "the key " + str(key) + " is not a valid key: " + str(validKeys)
                )
                return False

            if key != "html" and key != "url":
                if bool(BeautifulSoup(str(entry[key]), "html.parser").find()):
                    log.error(
                        "the key "
                        + str(key)
                        + " in entry "
                        + str(entry)
                        + " has html code in it"
                    )
                    return False

    return True


CONFIG_API = read_json(CONFIG_PATH)["api"]


def validate_input(value):
    output = None

    if type(value) != dict:
        return output

    if len(value) != len(CONFIG_API["valid_input_keys"]):
        return output

    if list(value.keys()) != CONFIG_API["valid_input_keys"]:
        return output

    tmp = type(value["after"])
    if tmp != int and tmp != float:
        return output

    if len(CONFIG_API["valid_sources"]) < len(value):
        return output

    if len(str(value["sources"])) > CONFIG_API["max_array_str_size"]:
        return output

    if len(str(value["filter"])) > CONFIG_API["max_array_str_size"]:
        return output

    tmp = list(CONFIG_API["valid_sources"].keys())
    for source in value["sources"]:
        if str(source) not in tmp:
            return output

    output = value
    for i in range(len(output["filter"])):
        # change any filter word to ONLY include allowed characters
        tmp = re.sub(r"[^A-Za-z0-9-_ ]+", "", str(output["filter"][i]))
        output["filter"][i] = " ".join(tmp.split())

    return output


def load_str_date(str_date):
    date_formats = [
        "%m-%d-%Y",
        "%Y-%m-%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%dT%H:%M:%SZ",
    ]

    epoch_time = None
    for format in date_formats:
        try:
            date_object = datetime.strptime(str_date, format)
            epoch_time = date_object.timestamp()
            break
        except:
            pass

    if epoch_time == None:
        log.error(
            "Failed to transform following string date to epoch: {}".format(str_date)
        )

    return epoch_time


def clean_html(content):
    oline = content
    soup = BeautifulSoup(oline, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    tmp = " ".join(soup.stripped_strings)
    tmp = "".join(filter(lambda x: x in set(string.printable), tmp))
    tmp = re.sub(" +", " ", tmp)
    return tmp


def print_it(data, indent=4):
    print(json.dumps(data, indent=indent))
    return


CONFIG_REQUEST = read_json(CONFIG_PATH)["request"]


def http_get(
    url, headers=CONFIG_REQUEST["header"], timeout=CONFIG_REQUEST["sec_timeout"]
):
    response = None
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code < 300:
            return response.content
    except:
        pass
    return response

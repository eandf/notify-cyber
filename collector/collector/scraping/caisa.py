from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import log


def caisa_get():
    ROOT_URL = "https://www.cisa.gov"
    URL = "https://www.cisa.gov/news-events/cybersecurity-advisories"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    HTML_DATE_CLASS = "c-teaser__date"
    filtered_htmls = soup.find_all("div", class_="c-teaser__date")
    dates = []
    for segment in filtered_htmls:
        line = str(segment).split("\n")[0]
        line = (
            line[line.find(str(datetime.now().year)) :]
            .split(">")[0]
            .replace('"', "")
            .replace("'", "")
        )
        dates.append(line)

    filtered_htmls = soup.find_all("h3", class_="c-teaser__title")

    cdata = []
    counter = 0
    for segment in filtered_htmls:

        line = str(segment).split("\n")

        try:
            title = line[2]
            # title = title.replace("'", '"')
            title = title.replace("<span>", "")
            title = title.replace("</span>", "")

            url = line[1]
            url = url.replace("'", '"')
            url = url[url.find('<a href="') + len('<a href="') : url.find('" target=')]
            url = url.replace("'", '"').replace(" ", "")
            url = ROOT_URL + url

            date = None
            try:
                date = url[url.find(str(datetime.now().year)) :].split("/")[0:3]
                if len(date) != 3:
                    raise ValueError(
                        str(caisa_get.__name__)
                        + "() error : failed to load date (len != 3)"
                    )
                date = "{}-{}-{}T12:00:00Z".format(date[0], date[1], date[2])
            except:
                if counter < len(dates):
                    date = dates[counter]
                    log.error(
                        str(caisa_get.__name__)
                        + "() error : failed to load date from scrape so the estimated date from "
                        + str(HTML_DATE_CLASS)
                        + " for title -> "
                        + str(title)
                    )
                else:
                    log.error(
                        str(caisa_get.__name__)
                        + "() error : failed to load date and estatimed date so the date value was set to NONE for title -> "
                        + str(title)
                    )

            html_data = None
            cdata.append(
                {
                    "url": url,
                    "title": title,
                    "date": date,
                    "details": None,
                    "html": html_data,
                }
            )

        except Exception as err:
            log.error(str(caisa_get.__name__) + "() error : " + str(err))

        counter += 1

    return cdata


if __name__ == "__main__":
    # NOTE: (3-3-2025) this part of the code is only used for testing and is only executed when the script is called directly
    output = caisa_get()
    print(json.dumps(output, indent=4))

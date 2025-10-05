from bs4 import BeautifulSoup
import cloudscraper
import json
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import util
import log


def isg_get():
    URL = "https://www.itsecurityguru.org/news/"

    # bypass Cloudflare
    scraper = cloudscraper.create_scraper()

    page = scraper.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    filtered_htmls = soup.find_all("h3", class_="jeg_post_title")

    cdata = []
    for segment in filtered_htmls:
        try:
            line = str(segment).split("\n")[1]
            tmp = re.split("<|>|href=\"|href='", line)
            url = tmp[2][:-1]
            title = util.clean_html(tmp[3])
            date = "-".join(url.split("/")[3:6])
            detail = None
            html_data = None
            cdata.append(
                {
                    "url": url,
                    "title": title,
                    "date": date,
                    "details": detail,
                    "html": html_data,
                }
            )
        except Exception as err:
            log.error(str(isg_get.__name__) + "() error : " + str(err))

    return cdata


if __name__ == "__main__":
    # NOTE: (3-3-2025) this part of the code is only used for testing and is only executed when the script is called directly
    output = isg_get()
    print(json.dumps(output, indent=4))

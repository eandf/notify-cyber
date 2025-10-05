from bs4 import BeautifulSoup
import requests
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import util
import log


def thn_get():
    URL = "https://thehackernews.com/"

    # https://realpython.com/beautiful-soup-web-scraper-python/
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    filtered_htmls = soup.find_all("div", class_="body-post clear")

    cdata = []
    for segment in filtered_htmls:

        line = str(segment).split("\n")

        try:
            url = line[1]
            url = url[url.find("https://") : url.find('">')]

            title = line[5]
            title = title.replace("'", '"')
            title = title[
                title.find('<img alt="')
                + len('<img alt="') : title.find('" decoding="async')
            ]
            title = title.replace('"', "'")

            # (9-13-2023) edge cause were the title's html uses "&amp;" to represent "&"
            title = title.replace("&amp;", "&")

            image = line[5]
            image = image[image.find("https://") : image.find('"/></noscript')]
            image = util.clean_html(image)

            date = line[10]
            date = date[date.find("</i>") + len("</i>") : date.find("</span>")]

            # # (7-14-2023) disabled grabbing "article preview/details" because it gets overwritten by AI summarization
            # detail = line[13]
            # detail = detail[detail.find('<div class="home-desc"> ')+len('<div class="home-desc"> '):detail.find('</div>')]
            # detail = util.clean_html(detail)
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
            log.error(str(thn_get.__name__) + "() error : " + str(err))

    return cdata

from datetime import datetime, timezone
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import util
import log


# TODO: (3-3-2025) this solution sucks and does not solve the root issue with the scraper but it's better then nothing so for now, I am going with this solution. But in the future a new and better solution is needed!
def dr_get():
    try:
        ROOT_URL = "https://www.darkreading.com/"
        URL = ROOT_URL + "latest-news"

        content = util.scrape_with_webcrawlerapi(URL, "html")
        if content["error"] == True:
            return []

        content = str(content).replace("<", "\n").replace(">", "\n").replace(" ", "\n")

        ignore_sub_strs = [
            "?",
            "author",
            "keyword/",
            "program/",
            "assets/",
            "/iot",
            "cyber-risk/data-privacy",
            "cybersecurity-operations/physical-security",
            "vulnerabilities-threats/insider-threats",
            "cybersecurity-operations/identity-access-management-security",
            "cyberattacks-data-breaches",
            "ics-ot-security",
            "endpoint-security/mobile-security",
            "endpoint-security/remote-workforce",
            "cybersecurity-operations/cybersecurity-careers",
        ]

        content_filter = []
        for line in content.split("\n"):
            if 'href="/' not in line:
                continue
            line = line.replace('href="/', "").replace('"', "")
            continue_adding = True
            for item in ignore_sub_strs:
                if item in line:
                    continue_adding = False
                    break
            dashes_count = len(line.split("-")) - 1
            if continue_adding and dashes_count >= 2:
                content_filter.append(line)

        content_filter = list(set(content_filter))

        output = []
        for entry in content_filter:
            url = ROOT_URL + entry
            title = url.split("/")[-1].replace("-", " ").title()
            output.append(
                {
                    "url": url,
                    "title": title,
                    "date": str(datetime.now(timezone.utc)),
                    "details": None,
                    "html": None,
                }
            )

        return output
    except Exception as err:
        log.error(str(dr_get.__name__) + "() error : " + str(err))
        return []


if __name__ == "__main__":
    # NOTE: (3-3-2025) this part of the code is only used for testing and is only executed when the script is called directly
    output = dr_get()
    print(json.dumps(output, indent=4))

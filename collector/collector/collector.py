import random
import json
import time
import sys
import os

from dotenv import load_dotenv
import util
import log

# load project's config
config_path = str(os.path.dirname(os.path.realpath(__file__))) + "/../config.json"
config = util.read_json(config_path)


def load_envs():
    for file_path in config["env_paths"]:
        if os.path.exists(file_path):
            log.info(f"Sourcing Environment variables from file '{file_path}'")
            load_dotenv(dotenv_path=file_path)
            return

    raise Exception(f"Failed to find a valid/existing env file path")


# load environment variables automatically
load_envs()

import db_supa
import sys
import ai

from scraping import caisa
from scraping import thn
from scraping import cve
from scraping import microsoft

scrapped_sources = {
    "thn": {"func": thn.thn_get, "args": []},
    "caisa": {"func": caisa.caisa_get, "args": []},
    "cve": {"func": cve.cve_get, "args": []},
    "microsoft": {"func": microsoft.microsoft_get, "args": []},
}


def get_all():
    # status code: 0 = successful & 1 = failed
    output = {"status": 0, "state": {"success": [], "fails": []}, "data": {}}

    for scrape in scrapped_sources:
        start_time = time.time()
        func = scrapped_sources[scrape]["func"]
        args = scrapped_sources[scrape]["args"]
        if len(args) > 0:
            results = func(*args)
        else:
            results = func()
        runtime = time.time() - start_time
        output["data"][scrape] = results
        log.info(
            "Completed running scrapper for {} in {} seconds".format(scrape, runtime)
        )

    for key in output["data"]:
        if util.valid_scrape(output["data"][key]):
            output["state"]["success"].append(key)
        else:
            output["state"]["fails"].append(key)
            output["status"] = 1
            log.critical("failed to scrape " + str(key))

    return output


def sql_proof(value):
    """
    About: remove ' from certain values to avoid sql error(s)
    Notes:
        - this solution is not ideal but it works for now
    """
    if type(value) == str:
        value = value.replace("'", "")
    return value


def collect():
    scrape_job = get_all()

    # (4-23-2023) print how many entries we collected - this does not account for duplicates in the db
    dcount = {}
    for dtmp in scrape_job["data"]:
        dcount[dtmp] = len(scrape_job["data"][dtmp])
    log.info(
        "collection source count (not excluding db duplicates): {}".format(str(dcount))
    )

    successes = scrape_job["state"]["success"]
    fails = scrape_job["state"]["fails"]
    datas = scrape_job["data"]

    if len(fails) == len(datas):
        log.critical("scrape job completed failed for sources " + str(fails))

    log_msg = (
        "successfully scraped from sources "
        + str(successes)
        + " and failed to scrape from sources "
        + str(fails)
    )
    if scrape_job["status"] != 0:
        log.error(log_msg)
    else:
        log.info(log_msg)

    all_urls = []
    for key, entries in datas.items():
        for entry in entries:
            if "url" in entry:
                all_urls.append(str(entry["url"]).replace(" ", ""))

    if not all_urls:
        log.critical("No URLs found to process.")
        return

    all_not_in_database = db_supa.urls_not_exist_in_database(
        db_supa.MAIN_TABLE, all_urls
    )

    log.info(
        f"{len(all_not_in_database)} total URLs do NOT exist in the database, so they need to be added"
    )

    added_counter = 0
    failed_counter = 0
    for source in datas:
        data = datas[source]
        for entry in data:
            if all_not_in_database != None and entry["url"] in all_not_in_database:
                entry["title"] = sql_proof(entry["title"])
                entry["source"] = str(source)
                entry["recorded"] = int(time.time())
                entry["details"] = sql_proof(entry["details"])
                entry["html"] = sql_proof(entry["html"])

                # query ai to get overview of article
                if source not in config["collector"]["ignore_ai_sources"]:
                    details = ""
                    html_data = ai.get_overview(entry["url"])

                    if html_data != None:
                        details = str(html_data["overview"])
                    else:
                        # TODO: (4-22-2023) this is a bad solution and can result in some news not getting added to the db but it works for now
                        html_data = {}
                        log.critical(
                            "(CODE RED!!!) url {} return None using ai.{}(), due to this the entry will not be recorded into the database (lets hope it works in the next batch collection)".format(
                                entry["url"], ai.get_overview.__name__
                            )
                        )
                        failed_counter += 1
                        continue

                    entry["details"] = sql_proof(details)
                    entry["html"] = sql_proof(json.dumps(html_data))

                db_status = db_supa.insert(db_supa.MAIN_TABLE, entry)
                if db_status:
                    added_counter += 1
                    log.info(
                        "successfully added new data which has url " + str(entry["url"])
                    )
                else:
                    failed_counter += 1
                    log.critical(
                        "failed to add the following entry to db: " + str(entry)
                    )

            # # (4-24-2023) commented this log out because it was really spamming the log files (because of CVE)
            # else:
            #     log.info("not adding url {} to database because it's already in the database".format(entry["url"]))

    if added_counter > 0:
        log.info("added " + str(added_counter) + " new entries to the database")

    if failed_counter > 0:
        log.critical(
            "failed to add " + str(failed_counter) + " new entries to the database"
        )

    return


if __name__ == "__main__":
    log.info("Starting New Collection Job")

    start_time = time.time()

    status = True
    try:
        collect()
    except Exception as err:
        status = False
        log.critical(
            "FAILED COLLECTION - {} sec - error : {}".format(str(time.time()), str(err))
        )

    runtime = time.time() - start_time

    log.info(
        "Collection Job Complete - Status: {} Runtime: {} seconds".format(
            status, runtime
        )
    )

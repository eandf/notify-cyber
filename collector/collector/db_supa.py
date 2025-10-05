from supabase.lib.client_options import ClientOptions
from supabase import create_client, Client
import time
import json
import os

import log

PROJECT_URL = os.environ.get("SUPABASE_URL")
PROJECT_KEY = os.environ.get("SUPABASE_SECRET_KEY")
MAIN_TABLE = os.environ.get("MAIN_TABLE")


def urls_not_exist_in_database(table, urls, chunk_size=50):
    """
    Check which URLs don't exist in the database table.

    Args:
        table: The table name to query
        urls: List of URLs to check
        chunk_size: Number of URLs to process in each batch

    Returns:
        List of URLs that don't exist in the database, or None if error occurs
    """
    try:
        client_options = ClientOptions(
            postgrest_client_timeout=60  # timeout in seconds
        )

        supabase = create_client(PROJECT_URL, PROJECT_KEY, options=client_options)

        existing_urls = []

        # process URLs in smaller chunks to avoid timeout
        for i in range(0, len(urls), chunk_size):
            url_chunk = urls[i : i + chunk_size]
            try:
                response = (
                    supabase.table(table).select("url").in_("url", url_chunk).execute()
                )
                existing_urls.extend([entry["url"] for entry in response.data])
                time.sleep(0.1)  # small delay between chunks to prevent rate limiting
            except Exception as chunk_err:
                log.warning(f"Error processing chunk {i//chunk_size + 1}: {chunk_err}")
                continue

        not_existing_urls = list(set(urls) - set(existing_urls))
        return not_existing_urls

    except Exception as err:
        log.critical(
            f"{urls_not_exist_in_database.__name__}() encountered an unexpected error: {str(err)}"
        )
        return None


def get_all_url(table, start=1, end=1000, offset=1000, max_iter=500):
    output = []
    total_requests = 0
    start_time = time.time()

    try:
        supabase = create_client(PROJECT_URL, PROJECT_KEY)

        max_id = (
            supabase.table(table)
            .select("id")
            .order(column="id", desc=True)
            .limit(1)
            .execute()
        )
        max_id = int(max_id.data[0]["id"])
        if max_id <= 0:
            log.error("max id is not greater then or equal to zero, so aborting")
            return None

        log.info("current max id: {}".format(max_id))

        while True:
            result = (
                supabase.table(table)
                .select("id", "url")
                .lte("id", end)
                .gte("id", start)
                .execute()
            )
            output.extend(result.data)

            current_largest = output[len(output) - 1]["id"]

            if current_largest >= max_id:
                break

            start += offset
            end += offset
            total_requests += 1
            if total_requests >= max_iter:
                log.critical(
                    "{}() loop exceeded max iteration limit of {}".format(
                        get_all_url.__name__, max_iter
                    )
                )
                return None

    except Exception as err:
        log.critical(
            "{}() encountered unexpected error occurred: {}".format(
                get_all_url.__name__, err
            )
        )
        return None

    runtime = time.time() - start_time
    log.info(
        "{}() collected {} entries by making {} requests in a runtime of {} seconds".format(
            get_all_url.__name__, len(output), total_requests, runtime
        )
    )

    return output


def insert(tablename, new_row):
    # NOTE: new_row MOST be type dict
    try:
        supabase = create_client(PROJECT_URL, PROJECT_KEY)
        output = supabase.table(tablename).insert(new_row).execute()
        log.info(
            "{}() successfully inserted new_row resulting in the following output: {}".format(
                insert.__name__, output
            )
        )
        return True
    except Exception as err:
        log.critical(
            "{}() encountered an unexpected error: {}".format(insert.__name__, err)
        )
        pass
    return False


def find_max_id(data):
    """
    Finds and returns the dictionary from a list of dictionaries that contains the maximum 'id' value,
    provided the dictionary also includes a 'url' key. Returns None if no suitable max is found,
    or if an exception occurs.

    :param data: List of dictionaries, each expected to potentially contain an 'id' and 'url'.
    :return: The dictionary with the highest 'id' value and an 'url' key or None.
    """
    try:
        if not data:
            None
        max_entry = max(data, key=lambda x: x.get("id", float("-inf")))
        if "id" in max_entry and "url" in max_entry:
            return max_entry
    except Exception as err:
        log.critical(
            "{}() encountered an unexpected error: {}".format(find_max_id.__name__, err)
        )
    return None

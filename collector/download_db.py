# Backup Entire Notify Cyber Database
# May 20, 2023

from supabase import create_client, Client
from dotenv import load_dotenv
import json
import time
import sys
import os

# Load config and environment variables
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
with open(config_path) as f:
    config = json.load(f)

# Try to load .env from configured paths
for env_path in config["env_paths"]:
    if os.path.exists(env_path):
        print(f"Loading environment variables from: {env_path}")
        load_dotenv(dotenv_path=env_path)
        break

PROJECT_URL = os.environ.get("SUPABASE_URL")
PROJECT_KEY = os.environ.get("SUPABASE_SECRET_KEY")
MAIN_TABLE = os.environ.get("MAIN_TABLE")


def write_json(path, data, ind=4):
    with open(str(path), "w") as file:
        json.dump(data, file, indent=ind)
    return


def get_all_data(table, start=1, end=1000, offset=1000, max_iter=500):
    output = []
    total_requests = 0

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

        print("current max id: {}".format(max_id))

        while True:
            print(
                "query number {} with values: start={}, end={}, offset={}, max_iter={}".format(
                    total_requests, start, end, offset, max_iter
                )
            )
            result = (
                supabase.table(table)
                .select("*")
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
                print(
                    "{}() loop exceeded max iteration limit of {}".format(
                        get_all_data.__name__, max_iter
                    )
                )
                return None

    except Exception as err:
        print(
            "{}() encountered unexpected error occurred: {}".format(
                get_all_data.__name__, err
            )
        )
        return None

    return output


if __name__ == "__main__":
    start_time = time.time()

    data = get_all_data(MAIN_TABLE)
    if data == None:
        sys.exit(1)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    logs_dir = os.path.join(script_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    filename = os.path.join(logs_dir, "backup_nc_{}.json".format(int(time.time())))

    write_json(filename, data)

    runtime = time.time() - start_time

    print("\nRESULTS:")
    print(" - Created File: {}".format(filename))
    print(" - Total Entries: {}".format(len(data)))
    print(" - Runtime: {} seconds".format(runtime))

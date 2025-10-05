import logging
import json
import sys
import os


def read_json(path):
    with open(str(path)) as file:
        content = json.load(file)
    return content


config_path = str(os.path.dirname(os.path.realpath(__file__))) + "/../config.json"
config = read_json(config_path)

# create handlers for file and stdout
LOG_FILE_PATH = config["log_file"]
DEBUG_LOG_PATH = config["debug_log_file"]
try:
    file_handler = logging.FileHandler(config["log_file"])
except:
    file_handler = logging.FileHandler(config["debug_log_file"])
    print(
        f"ERROR: Log file {LOG_FILE_PATH} does not exist, switching to: {DEBUG_LOG_PATH }"
    )

stdout_handler = logging.StreamHandler()

logging.basicConfig(
    handlers=[file_handler, stdout_handler],
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S %Z",
)


def debug(message):
    logging.debug(str(message))
    return


def info(message):
    logging.info(str(message))
    return


def warning(message):
    logging.warning(message)
    return


def error(message):
    logging.error(message)
    return


def critical(message):
    logging.critical(message)
    return

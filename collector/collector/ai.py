from newspaper import Article
import tiktoken
import openai
import time
import json
import math
import re
import os

import util
import log

config_path = str(os.path.dirname(os.path.realpath(__file__))) + "/../config.json"
CONFIG = util.read_json(config_path)["ai"]

openai.api_key = os.getenv("OPENAI_KEY").strip("\n")


def alog(sev, message):
    log_msg = "({}) {}".format(str(time.time()), str(message).capitalize())

    if sev > 5:
        sev = int(sev / 10)

    if sev == 1:
        log.debug(log_msg)
    elif sev == 2:
        log.info(log_msg)
    elif sev == 3:
        log.warning(log_msg)
    elif sev == 4:
        log.error(log_msg)
    else:
        log.critical(log_msg)

    return


def get_content(url):
    content = None

    # attempt 1: newspaper's Article
    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text
        content = content.split("\n")
        if len(content) == 0:
            return None
        content = " ".join(content)
        content = re.sub(" +", " ", content)
        if len(content) == 0:
            raise Exception(
                "length of content extracted created by Article() for url {} has length 0".format(
                    url
                )
            )
        return str(content)

    except Exception as err:
        alog(
            5,
            "{}() failed to scrape {} using Article-Package, "
            "attempting to scrape using http_get & clean_html methods -> {}".format(
                get_content.__name__, url, err
            ),
        )

    # attempt 2: http_get + clean_html
    try:
        content = util.http_get(url)
        content = util.clean_html(content)
        return str(content)
    except Exception as err:
        alog(
            5,
            "{}() failed to scrape {} using http_get & clean_html methods  -> {}".format(
                get_content.__name__, url, err
            ),
        )

    # all attempts failed
    return None


# estimate the token lengh of a given string and given model name
#   - # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except:
        # TODO: (9-7-2024) They are not updating tiktoken, so this jank solution was created
        # NOTE: (9-7-2024) We need a replacement for this package
        encoding = tiktoken.encoding_for_model("gpt-4")

    num_tokens = len(encoding.encode(string))
    return num_tokens


# remove every character except a-z, A-Z, 0-9, -, and " "
def remove_non_alphanumeric(input_string):
    output_string = ""
    for char in str(input_string):
        if char.isalnum() or char == "-" or char.isspace():
            output_string += char
    return output_string


# trim the end of a string until it meets a set token max using proportional feedback system
def trim_end(text, model, max_size, p, rs=10):
    new_text = str(text)
    current_token_size = num_tokens_from_string(text, model)

    while current_token_size > max_size and len(new_text) >= rs:
        tokens = new_text.split()
        rs = min(rs, math.ceil(len(tokens) / 2))
        last_token = tokens[-rs]
        new_text = new_text[: -(len(last_token) + rs)]
        current_token_size = num_tokens_from_string(new_text, model)
        rs = int(abs(max_size - current_token_size) * p)
        rs = max(1, rs)
        alog(
            1,
            "{}() - [ Current Token Size: {} | Text Length: {} | RS Value: {} ]".format(
                trim_end.__name__, current_token_size, len(new_text), rs
            ),
        )

    percentage = len(new_text) / len(text)

    # # (7-29-2023) Commented out because it was spamming the log file
    # alog(1, "{}() - Removed {}% of the text for the following text: {}".format(trim_end, percentage, text))

    return new_text, percentage


# used to trim a prompt to a LLM if it exceeds the LLM's input token limit
def size_prompt(prompt, text):
    final_prompt = build_prompt(prompt, text)

    # valid prompt if it does not pass the token limit
    etoken = num_tokens_from_string(final_prompt, CONFIG["model_name"])
    if (etoken + CONFIG["token_offset"]) <= CONFIG["token_limit"]:
        alog(
            1,
            "in {}() the prompt is ~ {} tokens which is below/equal to the {} token limit so no modifications needed".format(
                size_prompt.__name__, etoken, CONFIG["token_limit"]
            ),
        )
        return final_prompt

    # trim the end of the text to reduce token size
    elimit = CONFIG["token_limit"] - CONFIG["token_offset"]
    new_prompt, percentage = trim_end(
        final_prompt,
        CONFIG["model_name"],
        elimit,
        CONFIG["trim_p_value"],
        CONFIG["trim_init_value"],
    )
    if percentage >= CONFIG["ideal_text_percent"]:
        alog(
            1,
            "in {}() the prompt is ~ {} tokens which is above the {} token limit so the prompt was trimmed to {} of it's original length".format(
                size_prompt.__name__, etoken, CONFIG["token_limit"], percentage
            ),
        )
        return new_prompt

    # remove every character that except for a-z, 0-9, -, and " " from the text if a large amount of the text was trimmed
    new_text = remove_non_alphanumeric(text)
    final_prompt2 = build_prompt(prompt, new_text)
    etoken = num_tokens_from_string(final_prompt2, CONFIG["model_name"])
    if (etoken + CONFIG["token_offset"]) < CONFIG["token_limit"]:
        alog(
            3,
            "in {}() the prompt is ~ {} (above {} token limit), but it was trimmed to {}, above {} limit, of it's length so {}() to address the token size issue".format(
                size_prompt.__name__,
                etoken,
                CONFIG["token_limit"],
                percentage,
                CONFIG["ideal_text_percent"],
                remove_non_alphanumeric.__name__,
            ),
        )
        return final_prompt2

    # just return the trimmed text, even if a lot of if has been trimmed, if all else fails
    alog(
        3,
        "in {}() the prompt is ~ {} (above {} token limit), but it was trimmed to {}, above {} limit, of it's length. {}() failed as well so the trimmed result was returned".format(
            size_prompt.__name__,
            etoken,
            CONFIG["token_limit"],
            percentage,
            CONFIG["ideal_text_percent"],
            remove_non_alphanumeric.__name__,
        ),
    )

    return new_prompt


# construct the final prompt for a LLM giving an initial prompt and some additional text
def build_prompt(prompt, text):
    final_prompt = re.sub(" +", " ", prompt + "\n\n```\n" + text + "\n```").lstrip(
        "\n "
    )
    return final_prompt


def getOverviewAI(text):
    prompt = CONFIG["prompts"]["summary"].format(
        CONFIG["sentences"], CONFIG["min_words"], CONFIG["max_words"]
    )

    final_prompt = size_prompt(prompt, text)

    # # TODO: (3-5-2025) commented out to avoid bug...
    # # only continue if final_prompt was built currectly (not just prompt but prompt & text)
    # if len(final_prompt) <= (len(prompt) + 15):
    #     alog(
    #         5,
    #         "{}() stopped processing prompt to model {} due to prompt, most likely, not containing the article's text. here is the final_prompt that failed: {}".format(
    #             getOverviewAI.__name__, CONFIG["model_name"], final_prompt
    #         ),
    #     )
    #     return None

    output = None

    try:
        completion = openai.ChatCompletion.create(
            model=CONFIG["model_name"],
            messages=[{"role": "user", "content": final_prompt}],
        )

        results = completion["choices"][0]["message"]["content"]

        totalTokens = completion["usage"]["total_tokens"]
        estimatedCost = (totalTokens / 1000) * CONFIG["models_cost_per_1k_tokens"]

        output = {
            "content": results,
            "text": {
                "prompt": final_prompt,
                "text": text,
            },
            "tokens": {
                "tokens": totalTokens,
                "ecost": estimatedCost,
                "etoken": num_tokens_from_string(final_prompt, CONFIG["model_name"]),
            },
            "raw": completion,
        }
    except Exception as err:
        alog(
            5,
            "{}() failed to process data though, or after, {} model due to an unexpected error -> {}".format(
                getOverviewAI.__name__, CONFIG["model_name"], err
            ),
        )

    alog(
        2,
        "the {}() processed request and outputed the following: {}".format(
            getOverviewAI.__name__, json.dumps(output)
        ),
    )

    return output


# attempts to extract a cve json's description(s)
def cve_merge_descriptions(json_object):
    try:
        description_data = json_object["description"]["description_data"]
        descriptions = [item["value"] for item in description_data]
        merged_description = " ".join(descriptions)
    except Exception as err:
        merged_description = remove_non_alphanumeric(json.dumps(json_object))
        alog(
            4,
            "failed to extract descriptions from text in {}() so {}() was called due to the following error -> {}".format(
                cve_merge_descriptions.__name__, remove_non_alphanumeric.__name__, err
            ),
        )

    return merged_description


def remove_quotes(string):
    quotes = ['"', "'", "`", "‘", "’", "“", "”"]
    if string.startswith(tuple(quotes)):
        string = string[1:]
    if string.endswith(tuple(quotes)):
        string = string[:-1]
    return string


# main "root" function for AI script
def get_overview(url):
    try:
        text = ""
        if type(url) == dict:
            text = cve_merge_descriptions(url)
        else:
            text = get_content(url)
            if type(text) != dict:
                text = util.clean_html(get_content(url))
            else:
                text = str(text)
        data = getOverviewAI(text)
        content = remove_quotes(data["content"])
        return {"overview": content, "complete": data}
    except Exception as err:
        alog(
            5,
            "failed to get overview from {} model for an unexpected reason -> {}".format(
                CONFIG["model_name"], err
            ),
        )
    return None

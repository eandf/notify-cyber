import json
import copy
import re

NUM_SENTENCES_TO_REMOVE = 2

with open("db.json", "r") as file:
    data = json.load(file)

output = []
for entry in data:
    if entry.get("html") != None:
        del entry["html"]

    sentences = re.split(r"[.!?]+", entry["details"])

    if len(sentences) > NUM_SENTENCES_TO_REMOVE:
        sentences = sentences[:-NUM_SENTENCES_TO_REMOVE]
        entry["details"] = ".".join(sentences).rstrip(". !? ") + "."

    output.append(copy.deepcopy(entry))

with open("db.json", "w") as file:
    json.dump(output, file)

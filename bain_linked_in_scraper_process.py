import re
import json
import os
import pandas as pd


def parse(obj, base="https://www.linkedin.com/in/"):
    try:
        elements = obj["data"]["elements"][1]["elements"]
    except IndexError:
        elements = obj["data"]["elements"][0]["elements"]
    pattern = re.compile(r"DISTANCE_(.+)")
    store = []
    for i in elements:
        dump = {}
        name = i["title"]["text"]
        title = i["headline"]["text"]
        url = base + i["publicIdentifier"]
        location = i["subline"]["text"]
        dump["name"] = name
        dump["title"] = title
        dump["location"] = location
        dump["url"] = url
        store.append(dump.copy())
        del dump
    return store


root = "assets/bain_linkedin_scraper"
paths = os.listdir(root)
paths = ["%s/%s" % (root, i) for i in paths]
paths = list(filter(lambda x: "json" in x, paths))
store = []
for i in paths:
    with open(i, "r") as file:
        data = json.loads(file.read())
        store = store + parse(data)
df = pd.DataFrame(store)
df = df[list(store[1].keys())]
print(df.shape)
df.to_excel("output/bain_employees_linkedin_profiles.xlsx", index=False)
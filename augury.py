from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
from time import sleep
import os
import pandas as pd
import json


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


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
#
#
root = "assets/augury"
# psw = "qIhhek-dehzew-4dobqe"
# uname = "nikhilkamlesh.soni@gmail.com"
# search_url_base = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%222665061%22%5D&facetGeoRegion=%5B%22us%3A0%22%5D&facetNetwork=%5B%22S%22%5D&origin=FACETED_SEARCH&page="
# url1 = "https://www.linkedin.com/"
# driver = webdriver.Chrome()
# driver.get(url1)
# username = driver.find_element_by_id("login-email")
# password = driver.find_element_by_id("login-password")
# username.send_keys(uname)
# password.send_keys(psw)
# driver.find_element_by_id("login-submit").click()
# mkdir(root)
# for i in range(3):
#     k = i+1
#     search_url = search_url_base + str(k)
#     driver.get(search_url)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     html = driver.page_source
#     soup = BeautifulSoup(html, "html.parser")
#     target = soup.find_all("code", {"id": re.compile(r"bpr-guid-\d.+")})
#     payload = ""
#     for j in target:
#         if "metadata" in j.text:
#             payload = j.text.strip()
#     with open("%s/%s.json" % (root, str(k)), "w") as out:
#         out.write(payload)
#     sleep(random.uniform(2, 3))
#     print(k)
#
# driver.close()
#

paths = os.listdir(root)
paths = ["%s/%s" % (root, i) for i in paths]
paths = list(filter(lambda x: "json" in x, paths))
store = []
_K = 0
STOP = 300
for i in paths:
    with open(i, "r") as file:
        data = json.loads(file.read())
    store = store + parse(data)
    del data
    if _K == STOP:
        break
    _K += 1
df = pd.DataFrame(store)
df = df[list(store[1].keys())]
df.to_excel("output/augury_employees_linkedin_profiles.xlsx", index=False)
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
from time import sleep
import os
import pandas as pd
import json


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


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


root = "assets/microsoft_linkedin_scraper"
mkdir(root)
psw = "qIhhek-dehzew-4dobqe"
uname = "nikhilkamlesh.soni@gmail.com"
search_url_base = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%221035%22%2C%2210073178%22%2C%2210957831%22%2C%2211206713%22%2C%221386954%22%2C%221638785%22%2C%22165397%22%2C%2218086638%22%2C%221889423%22%2C%2219537%22%2C%222270931%22%2C%222446424%22%2C%22263515%22%2C%2230203%22%2C%223178875%22%2C%223238203%22%2C%223290211%22%2C%223763403%22%2C%225097047%22%2C%22589037%22%2C%22692068%22%5D&facetGeoRegion=%5B%22us%3A0%22%5D&facetNetwork=%5B%22S%22%5D&origin=FACETED_SEARCH&page="
url = "https://www.linkedin.com/"
driver = webdriver.Chrome()
driver.get(url)
username = driver.find_element_by_id("login-email")
password = driver.find_element_by_id("login-password")
username.send_keys(uname)
password.send_keys(psw)
driver.find_element_by_id("login-submit").click()
for i in range(100):
    k = i+1
    search_url = search_url_base + str(k)
    driver.get(search_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    target = soup.find_all("code", {"id": re.compile(r"bpr-guid-\d.+")})
    payload = ""
    for j in target:
        if "metadata" in j.text:
            payload = j.text.strip()
    with open("%s/%s.json" % (root, str(k)), "w") as out:
        out.write(payload)
    sleep(random.uniform(2, 3))
    print(k)

driver.close()
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
df.to_excel("output/microsoft_employees_linkedin_profiles.xlsx", index=False)
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import certifi
import json
from time import sleep
import random
import re
import os


# A simple script based web scraper to scrape email addresses of Bain recruiters from Bain's website.
# Raw Queries to extract JSON were figured out using Network Monitoring
# Use of Regex to separate the recruiter's name and their title

def response(url, request='GET', header=None, auth=None):

    '''
    Sends the request to a server and receives the response

    Args:
        url (str): URL
        request (str): 'GET' or 'POST'
        header (str): Header String
        auth (str): Signed Query

    Returns:
        urllib3.response.HTTPResponse: Response

    '''

    if request.lower() == 'get':
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            resp = http.request(request, url)
        except (urllib3.exceptions.MaxRetryError, ValueError) as error:
            resp = error
        return resp
    elif request.lower() == 'post':
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            resp = http.request(request, url + auth, headers=header)
        except (urllib3.exceptions.MaxRetryError, ValueError) as error:
            resp = error
        return resp
    else:
        return None


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


SUFFIX = "adh"
consultant = "3429"
aconsultant = "3472"
adh = "3416"
roles = [{"role": "adh", "app_id": "3416", "url": "https://www.bain.com/careers/roles/advanced-degree/"},
         {"role": "consultant", "app_id": "3429", "url": "https://www.bain.com/careers/roles/consultant/"},
         {"role": "aconsultant", "app_id": "3472", "url": "https://www.bain.com/careers/roles/ac/"}]
target = roles[2]
querybase = "https://www.bain.com/en/api/application/%s/get?queryValue=" % target["app_id"]
resp = response(target["url"])
soup = BeautifulSoup(resp.data, "html.parser")
cities = soup.find_all("a", {"class": "feed-filter-block__filter-link"})
store = {}
for i in cities:
    id = i["data-query-value"]
    query_url = querybase + id
    payload = response(query_url)
    sleep(random.uniform(0.1, 2))
    if payload.status == 200:
        data = payload.data.decode("utf-8")
    else:
        data = None
    store[i.text] = {"id": id, "query_url": query_url, "data": data}

mkdir("assets")
with open("assets/bain_raw_cities_data_%s.json" % target["role"], "w") as file:
    json.dump(store, file)

with open("assets/bain_raw_cities_data_%s.json" % target["role"], 'r') as fp:
    data = json.load(fp)

uso = pd.Series(["Atlanta", "Boston", "Chicago", "Dallas", "Houston", "Los Angeles", "New York", "San Francisco",
                 "Seattle", "Silicon Valley", "Washington D.C."])

pattern = re.compile(r"mailto:(.+)")
store = []
for i in data:
    temp_store = dict()
    html = json.loads(data[i]["data"])["html"]
    soup = BeautifulSoup(html, "html.parser")
    atags = soup.find_all("a")
    for j in atags:
        result = re.search(pattern, j["href"])
        if result:
            temp_store["city"] = i
            temp_store['email'] = result.group(1)
            temp_store['name'] = j.text
            store.append(temp_store.copy())
            temp_store.clear()


df = pd.DataFrame(store)
df.insert(loc=0, column="title", value="")
for i, j in df.iterrows():
    splt = j["name"].split("-")
    if len(splt) > 0:
        df.loc[i, "name"] = splt[0]
        df.loc[i, "title"] = splt[len(splt)-1]
df = df[["name", "title", "email", "city"]]
bool_val = df["city"].isin(uso)
df = df[bool_val]
mkdir("output")
df.to_excel("output/details_%s.xlsx" % target["role"], index=False)

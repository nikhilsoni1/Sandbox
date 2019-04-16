import requests
import json
import sqlite3
# import pypubs
from lxml import etree


def json_recursion(obj, path):
    '''
    XPath like recursion of a JSON structure.
    Args:
        obj (dict): Parsed JSON or a dict
    Returns:
        Object at the specified XPath
    '''
    path = path.split("/")
    if len(path) > 1:
        target = path.pop(0)
        path = "/".join(path)
        if type(obj) is dict:
            return json_recursion(obj.get(target, None), path)
        else:
            return json_recursion(obj[int(target)], path)
    else:
        target = path.pop(0)
        if type(obj) is dict:
            return obj.get(target, None)
        else:
            target = int(target)
            return obj[int(target)]


base = "http://sherpa.mimas.ac.uk/romeo/api29.php?issn="

response = requests.get("http://api.crossref.org/works?sample=100&select=ISSN")
json_text = response.text
data = json.loads(json_text)
issn_data = json_recursion(data, "message/items")
store = list()
for i in issn_data:
    issn = i.get("ISSN", [])
    store += issn
for i in store:
    url = "%s%s" % (base, i)
    resp = requests.get(url)
    text = str.encode(resp.text)
    element = etree.fromstring(text)
    target = element.find("conditions")
    df = True
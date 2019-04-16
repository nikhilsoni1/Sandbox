import pandas as pd
from datetime import datetime
import re
import requests
from lxml import etree
import os
from time import sleep
import random
import sqlite3
import pandas as pd

src = "/Users/soni/Downloads/ead.json"
assets = "assets/ead"
output = "output/ead"
json_store = "assets/ead/json"
db_fname = "ead.db"

db_conn = sqlite3.connect(os.path.join(assets, db_fname))
db_cursor = db_conn.cursor()

try:
    db_cursor.execute('''CREATE TABLE EAD (Receipt_Number text, status text)''')
except sqlite3.OperationalError:
    pass


def status_parser(strng):
    result = True
    if "rejected" in strng:
        result = False
    return result


def proc(data):
    pattern1 = r"If you do not receive(.+)by\s(.+)\,"
    store = list()
    payload = dict()
    for i, j in data.items():
        splt = j.split(",")
        regx = re.search(pattern1, j)
        if regx is not None:
            regx_result = regx.group(2)
            by_date = regx_result
        else:
            by_date = None
        try:
            status = splt[2]
        except IndexError as e:
            print(e, splt)
        remark = splt[5]
        dt = ''.join(splt[:2])
        dt = dt.replace("On", "").strip()

        dt = datetime.strptime(dt, "%B %d %Y")

        payload["Receipt"] = i
        payload["Date"] = dt.date()
        payload["Status"] = status_parser(status)
        try:
            payload["By_Date"] = datetime.strptime(by_date, "%B %d, %Y")
        except TypeError:
            payload["By_Date"] = by_date
        if not payload["Status"]:
            payload["Remark"] = remark
        store.append(payload.copy())
        payload.clear()
    return store


def uscis(base, cursor, rng=1000, thres=2):
    _K = 0

    store = [base - i for i in range(rng)]
    dump = dict()

    for i in store:
        receipt_number = "YSC%d" % i
        payload = {"changeLocale": "", "appReceiptNum": receipt_number, "initCaseSearch": "CHECK+STATUS"}

        session = requests.Session()
        xpath = r"/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p"
        r = session.post('https://egov.uscis.gov/casestatus/mycasestatus.do', data=payload)
        print(receipt_number, r.status_code)
        if r.status_code == 200:
            html = etree.fromstring(r.text, parser=etree.HTMLParser())
            target = html.xpath(xpath)
            try:
                txt = target[0].text
                if "I-765" in txt:
                    pld = (receipt_number, txt)
                    print(pld)
                    cursor.execute("INSERT INTO EAD VALUES (?,?)", pld)
                    db_conn.commit()
            except IndexError:
                pass
            sleep(random.uniform(0.02, 0.05))
        else:
            _K += 1
        if _K == thres:
            print(receipt_number, r.status_code)
            return dump
    return dump


my_number = 1990158312
start = 1990152212
uscis(start, db_cursor)


df = pd.read_sql('SELECT * FROM EAD', db_conn)
df_dict = df.to_dict(orient="records")

data = dict()
x = df.to_dict(orient="records")
for i in x:
    a = [tuple(i.values())]
    b = dict(a)
    data.update(b)

dump = proc(data)
df = pd.DataFrame(dump)
order = ["Receipt", "Date", "Status", "Remark", "By_Date"]
df = df[order]
df.to_sql("EAD_PROCESSED", db_conn, if_exists="replace")
db_conn.close()



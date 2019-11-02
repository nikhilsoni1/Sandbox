from datetime import datetime
import requests
from lxml import etree
import os
import sqlite3
import re

def uscis(receipt_number):
    txt = None
    # receipt_number = "YSC%d" % i
    payload = {"changeLocale": "", "appReceiptNum": receipt_number, "initCaseSearch": "CHECK+STATUS"}
    session = requests.Session()
    xpath = r"/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p"
    r = session.post('https://egov.uscis.gov/casestatus/mycasestatus.do', data=payload)
    print(receipt_number, r.status_code)
    if r.status_code == 200:
        html = etree.fromstring(r.text, parser=etree.HTMLParser())
        target = html.xpath(xpath)
        txt = target[0].text
    return txt


def write(cursor, payload, table_name):
    write_query = "INSERT INTO %s VALUES (?,?)" % table_name
    cursor.executemany(write_query, payload)
    return None

assets = "assets/ead"
output = "output/ead"
db_fname = "ead.db"
now = datetime.now().strftime("%m%d")
table_name = "Consolidated"

db_conn = sqlite3.connect(os.path.join(assets, db_fname))
db_cursor = db_conn.cursor()

table_create_query = "CREATE TABLE Consolidated (Receipt_Number text PRIMARY KEY, changed_status text, init_status text, change_date text)"

try:
    db_cursor.execute(table_create_query)
except sqlite3.OperationalError:
    pass


diff_pattern = re.compile(r"EAD_\d\d\d\d_diff")
db_cursor.execute('SELECT name from sqlite_master where type= "table"')
tables_list = db_cursor.fetchall()
tables_list = [i[0] for i in tables_list]
tables_list = list(filter(lambda x: True if re.search(diff_pattern, x) else False, tables_list))
store = []

for i in tables_list:
    hj = i
    df = True
    year = str(datetime.now().year)
    date = i.split("_")[1] + year
    date = str(datetime.strptime(date, "%m%d%Y").date())

    query = 'SELECT * FROM %s' % i
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    diff_dict = dict(results)
    query = 'SELECT * FROM EAD WHERE Receipt_Number in (SELECT Receipt_Number FROM %s)' % i
    db_cursor.execute(query)
    ead_results = db_cursor.fetchall()
    ead_results_dict = dict(ead_results)

    for key, value in diff_dict.items():
        changed_status = value
        init_status = ead_results_dict.get(key)
        payload = (key, changed_status, init_status, date)
        store.append(payload)


db_cursor.executemany("INSERT OR IGNORE INTO Consolidated VALUES (?,?,?,?)", store)
db_conn.commit()
db_conn.close()
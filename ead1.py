from datetime import datetime
import requests
from lxml import etree
import os
import sqlite3


def uscis(receipt_number):
    txt = None
    payload = {"changeLocale": "", "appReceiptNum": receipt_number, "initCaseSearch": "CHECK+STATUS"}
    session = requests.Session()
    xpath = r"/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p"
    r = session.post('https://egov.uscis.gov/casestatus/mycasestatus.do', data=payload)
    print(receipt_number, r.status_code)
    if r.status_code == 200:
        html = etree.fromstring(r.text, parser=etree.HTMLParser())
        target = html.xpath(xpath)
        iter_text = lambda x: ''.join(x.itertext()).strip()
        txt = list(map(iter_text, target))
    txt = list(filter(lambda x: x is not None and x != '', txt))
    if len(txt) > 0:
        return txt[0]
    else:
        return None


def write(cursor, payload, table_name):
    write_query = "INSERT INTO %s VALUES (?,?)" % table_name
    cursor.executemany(write_query, payload)
    return None


os.chdir("/Users/soni/Documents/Projects/Sandbox")

assets = "assets/ead"
output = "output/ead"
db_fname = "ead.db"
now = datetime.now().strftime("%m%d")
table_name = "EAD_%s_diff" % now

db_conn = sqlite3.connect(os.path.join(assets, db_fname))
db_cursor = db_conn.cursor()

table_create_query = "CREATE TABLE %s (Receipt_Number text, status text)" % table_name

try:
    db_cursor.execute(table_create_query)
except sqlite3.OperationalError:
    pass

db_cursor.execute('''SELECT * FROM EAD_0424''')
results = db_cursor.fetchall()
store = []
for ctr, i in enumerate(results):
    receipt, status = i
    new_status = uscis(receipt)
    if new_status.lower() != status.lower() and "post office" not in new_status.lower():
        print("Status for %s changed\n\n" % receipt)
        payload = (receipt, new_status)
        store.append(payload)

write(db_cursor, store, table_name)
del_query = "DELETE FROM EAD_0424 WHERE Receipt_Number IN (SELECT Receipt_Number FROM %s)" % table_name
db_conn.execute(del_query)
db_conn.commit()
db_conn.close()
os.system("/Users/soni/Documents/Projects/Sandbox/venv/bin/python /Users/soni/Documents/Projects/Sandbox/ead_consolidation.py")
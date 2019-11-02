import requests
from lxml import etree
import logging


def uscis(receipt_number):
    txt = None
    payload = {"changeLocale": "", "appReceiptNum": receipt_number, "initCaseSearch": "CHECK+STATUS"}
    session = requests.Session()
    xpath = r"/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p"
    r = session.post('https://egov.uscis.gov/casestatus/mycasestatus.do', data=payload)
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


status = uscis("YSC1990198312")
df = True

# logging.basicConfig(filename="/Users/soni/Desktop/log.txt",
#                             filemode='a',
#                             format='%(asctime)s: %(message)s',
#                             datefmt='%m/%d/%Y %H:%M:%S',
#                             level=logging.DEBUG)
#
# logging.info(status)
# print(status)





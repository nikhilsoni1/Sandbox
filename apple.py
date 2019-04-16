from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome()
import re
import random
from time import sleep

psw = "qIhhek-dehzew-4dobqe"
uname = "nikhilkamlesh.soni@gmail.com"
search_url_base = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22162479%22%5D&facetGeoRegion=%5B%22us%3A0%22%2C%22us%3A84%22%2C%22us%3A70%22%5D&facetNetwork=%5B%22S%22%5D&page="
url1 = "https://www.linkedin.com/"
driver.get(url1)
username = driver.find_element_by_id("login-email")
password = driver.find_element_by_id("login-password")
username.send_keys(uname)
password.send_keys(psw)
driver.find_element_by_id("login-submit").click()
for i in range(280):
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
    with open("assets/apple_emp/selenium/%s.json" % str(k), "w") as out:
        out.write(payload)
    sleep(random.uniform(2, 3))
    print(k)

driver.close()



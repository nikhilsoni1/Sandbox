from bs4 import BeautifulSoup

path = "/Users/soni/Downloads/stuff"
with open(path, "r") as conn:
    file = conn.read()
soup = BeautifulSoup(file, "html.parser")
target = soup.find_all("a")
for i in target:
    print(i)
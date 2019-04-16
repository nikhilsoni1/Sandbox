import requests


url = "https://www.goodreads.com/book/show/3.Harry_Potter_and_the_Sorcerer_s_Stone"
search_url = "https://www.goodreads.com/book/reviews/3?hide_last_page=true&amp;page=2"
session = requests.Session()
r = session.get(url)
s = session.get(search_url)
print(s.text)


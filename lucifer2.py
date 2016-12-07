import re
import requests
from bs4 import BeautifulSoup as bs4
with open('Safari Bookmarks.html') as f:
    r = f.read()

h = bs4(r, "lxml")
links = h.find_all('a', href=re.compile('^http'))
print(len(links))

r = requests.get('http://localhost:8888/fresh/')
print(r.json()[0].get('status'))

for i,link in enumerate(links):
    try:
        url = link.get('href')
        print(i, url)
        r = requests.get('http://localhost:8888/add/'+url)
        print(r.json()[0].get('status'))
    except:
        print('FAIL', i, url)

for i,link in enumerate(links):
    try:
        url = link.get('href')
        print(i, url)
        r = requests.get('http://localhost:8888/screen/'+url)
        print(r.json()[0].get('status'))
    except:
        print('FAIL', i, url)

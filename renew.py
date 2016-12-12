import re
import requests
from bs4 import BeautifulSoup as bs4

r = requests.get('http://localhost:8888/all/')
links = r.json()

#for i,link in enumerate(links):
#    try:
#        url = link.get('href')
#        print(i, url)
#        r = requests.get('http://localhost:8888/add/'+url)
#        print(r.json()[0].get('status'))
#    except:
#        print('FAIL', i, url)

for i,link in enumerate(links):
    try:
        url = link.get('url')
        print(i, url)
        r = requests.get('http://localhost:8888/screen/'+url)
        print(r.json()[0].get('status'))
    except:
        print('FAIL', i, url)

import os.path
from datetime import datetime
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME

schema = Schema(title=TEXT(stored=True), url=TEXT(stored=True), date=DATETIME(stored=True), content=TEXT)

if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema)

import re
import requests
from bs4 import BeautifulSoup as bs4
with open('Safari Bookmarks.html') as f:
    r = f.read()

h = bs4(r, "lxml")
links = h.find_all('a', href=re.compile('^http'))
print(len(links))

writer = ix.writer()
for i,link in enumerate(links):
    try:
        url = link.get('href')
        print(i, url)
        r = requests.get(url, timeout=5)
        writer.add_document(title=link.text, url=url, date=datetime.utcnow(), content=r.text)
    except:
        print('FAIL', i, url)
writer.commit()

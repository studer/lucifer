import os.path
import hashlib
import requests
import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.escape
from bs4 import BeautifulSoup as bs4
from datetime import datetime
from selenium import webdriver
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.qparser import MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin

class SearchHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, search):
        ix = open_dir("index")
        with ix.searcher() as searcher:
            qp = MultifieldParser(['title', 'content', 'url'], ix.schema)
            qp.add_plugin(DateParserPlugin())
            query = qp.parse(search)
            results = searcher.search(query)
            self.write(tornado.escape.json_encode([{'title':r.get('title'), 'url':r.get('url'), 'date':r.get('date').strftime("%A, %d. %B %Y %I:%M%p"), 'hash':r.get('hash', 'blank')} for r in results[:10]]))
            self.set_header('Content-Type', 'application/json')

class ScreenHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, url):
        try:
            driver = webdriver.PhantomJS()
            driver.set_window_size(1024, 768)
            driver.set_page_load_timeout(30)
            driver.get(url)
            hashx = hashlib.sha256(url.encode('utf8')).hexdigest()
            driver.save_screenshot('template/'+hashx+'.png')
            driver.quit()
            self.write(tornado.escape.json_encode([{'status':'OK', 'hash':hashx}]))
            self.set_header('Content-Type', 'application/json')
        except:
            self.write(tornado.escape.json_encode([{'status':'ERROR'}]))
            self.set_header('Content-Type', 'application/json')

class AddHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, url):
        try:
            r = requests.get(url, timeout=5)
            h = bs4(r.text, "lxml")
            ix = open_dir("index")
            writer = ix.writer()
            hashx = hashlib.sha256(url.encode('utf8')).hexdigest()
            writer.update_document(title=h.title.text, url=url, date=datetime.utcnow(), content=r.text, hash=hashx)
            writer.commit()
            self.write(tornado.escape.json_encode([{'status':'OK', 'hash':hashx}]))
            self.set_header('Content-Type', 'application/json')
        except:
            self.write(tornado.escape.json_encode([{'status':'ERROR'}]))
            self.set_header('Content-Type', 'application/json')

class FreshHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            schema = Schema(title=TEXT(stored=True), url=TEXT(stored=True), date=DATETIME(stored=True), content=TEXT, hash=ID(stored=True, unique=True))
            if not os.path.exists("index"):
                os.mkdir("index")
            ix = create_in("index", schema)
            self.write(tornado.escape.json_encode([{'status':'OK'}]))
            self.set_header('Content-Type', 'application/json')
        except:
            self.write(tornado.escape.json_encode([{'status':'ERROR'}]))
            self.set_header('Content-Type', 'application/json')


def make_app():
    handler = [
            (r'/search/(.*)', SearchHandler),
            (r'/screen/(.*)', ScreenHandler),
            (r'/add/(.*)', AddHandler),
            (r'/fresh/', FreshHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': 'template'}),
        ]
    settings = dict(
            template_path="template",
            static_path="template",
            debug=True,
        )
    return tornado.web.Application(handler, **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.escape
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin

class MainHandler(tornado.web.RequestHandler):
    #@tornado.gen.coroutine
    def get(self, search):
        ix = open_dir("index")

        with ix.searcher() as searcher:
            qp = MultifieldParser(['title', 'content', 'url'], ix.schema)
            qp.add_plugin(DateParserPlugin())
            query = qp.parse(search)
            results = searcher.search(query, terms=True)
            self.write(tornado.escape.json_encode([{'title':r.get('title'), 'url':r.get('url'), 'date':r.get('date').strftime("%A, %d. %B %Y %I:%M%p"), 'hash':'2c7fb59f0729d8af81a7c4aa6d7086b93a47575c821bebf5386eec4d39554d3a'} for r in results[:10]]))
            self.set_header('Content-Type', 'application/json')
            #for r in results:
                #self.write(str(r.get('title')))
                #self.write(unicode(r.matched_terms()))
                #print(r.highlights('title'))


def make_app():
    handler = [
            (r'/search/(.*)', MainHandler),
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

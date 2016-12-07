from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin

ix = open_dir("index")

with ix.searcher() as searcher:
    qp = MultifieldParser(['title', 'content', 'url'], ix.schema)
    qp.add_plugin(DateParserPlugin())
    query = qp.parse("qoqa")
    results = searcher.search(query, terms=True)
    for r in results:
        print(r.get('hash'))
        print(r.matched_terms())
        #print(r.highlights('title'))

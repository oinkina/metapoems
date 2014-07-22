from google.appengine.ext import db


class AuthorCorpus(db.Model):
  author_ID = db.IntegerProperty()
  author_name = db.StringProperty()
  corpus = db.StringListProperty()


acorp = AuthorCorpus(author_ID=65,
                    author_name="Shakespeare, William",
                    corpus=[
                    	"http://www.gutenberg.org/cache/epub/2264/pg2264.txt",
                    	"http://www.gutenberg.org/cache/epub/2265/pg2265.txt",
                    	"http://www.gutenberg.org/cache/epub/2267/pg2267.txt",
               				]

                    	)

acorp.put()



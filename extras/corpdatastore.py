from google.appengine.ext import ndb
import webapp2
import authors


class AuthorCorpus(ndb.Model):
  author_name = ndb.StringProperty()
  work_ids = ndb.ListProperty()
  server = ndb.StringProperty()
  directory = ndb.StringProperty()
  filename = ndb.StringProperty()

for i in authors.authors:
  author = AuthorCorpus(author_name=i)
  author.put()

query = author.query()
print query.fetch
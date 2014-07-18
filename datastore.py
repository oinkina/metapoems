from google.appengine.ext import ndb

class Ngram(ndb.Model):
  
  word  = ndb.StringProperty(required=True)
  count = ndb.IntegerProperty(required=True)
from google.appengine.ext import ndb, db
import pickle


class Ngram(ndb.Model):
  
  word  = ndb.StringProperty(required=True)
  count = ndb.IntegerProperty(required=True)


# http://forums.udacity.com/questions/6021587/how-tostore-dictionary-and-other-python-objects-in-google-datastore

class DictProperty(db.Property):
  data_type = dict

  def get_value_for_datastore(self, model_instance):
    value = super(DictProperty, self).get_value_for_datastore(model_instance)
    return db.Blob(pickle.dumps(value))

  def make_value_from_datastore(self, value):
    if value is None:
      return dict()
    return pickle.loads(value)

  def default_value(self):
    if self.default is None:
      return dict()
    else:
      return super(DictProperty, self).default_value().copy()

  def validate(self, value):
    if not isinstance(value, dict):
      raise db.BadValueError('Property %s needs to be convertible '
                         'to a dict instance (%s) of class dict' % (self.name, value))
    return super(DictProperty, self).validate(value)

  def empty(self, value):
    return value is None

class LanguageModel(db.Model):
   bigram   = DictProperty(required=True)
   trigram  = DictProperty(required=True)
   quadgram = DictProperty(required=True)
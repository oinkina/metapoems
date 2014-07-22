from google.appengine.ext import db


class AuthorCorpus(db.Model):
  author_ID = db.StringProperty()
  author_name = db.StringProperty()
  corpus = db.StringProperty()


acorp = AuthorCorpus(first_name='Antonio',
                    last_name='Salieri')

employee.hire_date = datetime.datetime.now().date()
employee.attended_hr_training = True

employee.put()

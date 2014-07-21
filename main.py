from datastore import Ngram

import jinja2 
import os
import webapp2


jinja_environment = jinja2.Environment(loader=
  jinja2.FileSystemLoader(os.path.dirname(__file__)))
 
### Handlers ### 

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    # browse all objects in "Ngram" kind
    query = Ngram.query()
    # retrieve ngrams and set to var ngrams 
    ngrams = query.fetch()

    template_values = {
      'title'  : "Datastore", 
      'ngrams' : ngrams
    }

    template = jinja_environment.get_template('home.html')
    self.response.out.write(template.render(template_values))

class PoemHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'title' : 'Poem'
    }
    template = jinja_environment.get_template('poems/generate.html')
    self.response.out.write(template.render(template_values))

 
routes = [
  ('/', HomeHandler),
  ('/poem', PoemHandler),
]
app = webapp2.WSGIApplication(routes, debug=True)
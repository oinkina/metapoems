from datastore import Ngram
from markov import generatePoem

import jinja2 
import os
import webapp2



jinja_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))
 
### Handlers ### 

class NgramHandler(webapp2.RequestHandler):
  def get(self):
    # browse all objects in "Ngram" kind
    query = Ngram.query()
    # retrieve ngrams and set to var ngrams 
    ngrams = query.fetch()

    template_values = {
      'title'  : "Datastore", 
      'ngrams' : ngrams
    }

    template = jinja_environment.get_template('ngram.html')
    self.response.out.write(template.render(template_values))

class MakePoemHandler(webapp2.RequestHandler):
  def get(self):
    
    template_values = {}

    template = jinja_environment.get_template('poems/makePoem.html')

    self.response.out.write(template.render(template_values))


class PoemHandler(webapp2.RequestHandler):
  def get(self):

    poem = generatePoem("shakespeare.txt") 

    template_values = {
      'poem' : poem
    }

    template = jinja_environment.get_template('poems/generatedpoem.html')

    self.response.out.write(template.render(template_values))

 
routes = [
  ('/', MakePoemHandler),
  ('/poem', PoemHandler),
  ('/ngram', NgramHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
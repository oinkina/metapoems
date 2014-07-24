import markov

import jinja2 
import os
import webapp2
#from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))
 

### Handlers ### 

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'output' : output
    }
    template = jinja_environment.get_template('home.html')
    self.response.out.write(template.render(template_values))

class MakePoemHandler(webapp2.RequestHandler):
  def get(self):
    
    template_values = {}

    template = jinja_environment.get_template('poems/makePoem.html')

    self.response.out.write(template.render(template_values))


class PoemHandler(webapp2.RequestHandler):
  def get(self):

    #poem = markov.generatePoem("shakespeare.txt") 
    
    y = self.request.get("link")
    for f in os.listdir("corpus"):
      if y == f[:-4]:
        author = str(f)
    try:
      ona = generatePoem("corpus/" + author)
    except Exception as e:
      self.response.out.write(str(e))

    template_values = {
      'poem' : ona
    }

    template = jinja_environment.get_template('poems/generatedpoem.html')

    self.response.out.write(template.render(template_values))

# class PublishHandler(webapp2.RequestHandler):
#   def get(self):

 
routes = [
  ('/home', HomeHandler),
  ('/', MakePoemHandler),
  ('/poem', PoemHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)


### RHYMING ###

# url = "http://rhymebrain.com/talk?function=getRhymes&word=hello"
# result = urlfetch.fetch(url)
# if result.status_code == 200:
#   output = result.content

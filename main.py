from markov import *

import jinja2 
import os
import webapp2
#from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))
 

### Handlers ### 

class MakePoemHandler(webapp2.RequestHandler):
  def get(self):
    
    template_values = {}

    template = jinja_environment.get_template('poems/makePoem.html')

    self.response.out.write(template.render(template_values))


class PoemHandler(webapp2.RequestHandler):
  def get(self):

    y = self.request.get("link")
    for f in os.listdir("corpus"):
      if y == f[:-4]:
        author = str(f)

    title, poem = generatePoem("corpus/" + author, lineLength=7, error = 3, lines=10)
    # try:
    #   ona = generatePoem("corpus/" + author)
    # except Exception as e:
    #   self.response.out.write(str(e))

    template_values = {
      'title' : title,
      'poem' : poem,
      'author' : author
    }

    template = jinja_environment.get_template('poems/generatedpoem.html')

    self.response.out.write(template.render(template_values))

# class PublishHandler(webapp2.RequestHandler):
#   def get(self):

# class NewPoemHandler(webapp2.RequestHandler):
#   def get(self):
#     lineLength = self.request.get('lineLength')
#     lines = self.request.get('lines')



 
routes = [
  #('/home', HomeHandler),
  ('/', MakePoemHandler),
  ('/poem', PoemHandler),
  #('/newpoem', PoemHandler)
]

app = webapp2.WSGIApplication(routes, debug=True)


### RHYMING ###

# url = "http://rhymebrain.com/talk?function=getRhymes&word=hello"
# result = urlfetch.fetch(url)
# if result.status_code == 200:
#   output = result.content

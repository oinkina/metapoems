import jinja2 
import os
import webapp2

jinja_environment = jinja2.Environment(loader=
  jinja2.FileSystemLoader(os.path.dirname(__file__)))
 
class PoemHomeHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    template = jinja_environment.get_template('poem_home.html')
    self.response.out.write(template.render(template_values))
  
app = webapp2.WSGIApplication([('/poem', PoemHomeHandler),
  ],
  debug=True)
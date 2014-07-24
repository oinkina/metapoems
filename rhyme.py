from google.appengine.api import urlfetch

url = "http://rhymebrain.com/talk?function=getRhymes&word=hello"
result = urlfetch.fetch(url)
if result.status_code == 200:
  print result.content
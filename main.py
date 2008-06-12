import cgi
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
import os
from google.appengine.ext.webapp import template

class Catalog(db.Model):
    country = db.StringProperty()
    year = db.DateTimeProperty()
    number = db.IntegerProperty()
    type = db.StringProperty()
    inlabel = db.StringProperty()
    outlable = db.StringProperty()

class MainPage(webapp.RequestHandler):
  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Stamp(webapp.RequestHandler):
    def get(self,  country="ambomaa"):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(country)

class Reset(webapp.RequestHandler):
    def get(self):
        if not users.get_current_user():
            greeting = users.create_login_url("/")
            self.response.out.write('<html><body><a href=\"%s\">Login first as admin</a></body></html>' % greeting)
            return
        if users.is_current_user_admin():
            while True:
                q = Catalog.all() # max 1000 at time
                if q == None:
                    break
                for result in q:
                    del q
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("reset done")
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("reset requires admin")

class MainPage(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')

def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        (r'/stamp/[A-Za-z]+', Stamp), 
                                        ('/reset', Reset)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()

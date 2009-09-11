#!/usr/bin/env python

import cgi
#import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm,  inch,  pica

import os
import logging

#class Conf(db.Model):
#  user = db.UserProperty()
#  timestamp = db.DateTimeProperty(auto_now=True)
#  pagewidth = db.FloatProperty()
#  pageheight = db.FloatProperty()
#  logotxt = db.StringProperty()


#def setDefaults(user):
#  conf = Conf(
#    user = user,
#    pagewidth = A4[0], # does not work
#    pageheight = A4[1],
##        pagewidth = 150*mm,
##        pageheight = 150*mm,
#    logotxt = "Anonymous Albumatics")
#  conf.save()


#class Resetdb(webapp.RequestHandler):
#  def get(self):
#    if not users.get_current_user():
#      self.response.out.write(
#        '<a href="' +
#        users.create_login_url('/resetdb') +
#        '">First, log in as admin</a>')
#    elif users.is_current_user_admin():
#      self.response.out.write('reset')
#      user = users.User("__default__"),
#      setDefaults(user)
#    else:
#      self.response.out.write('non admin user')


class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    admin = False
    prefs = False
    if user:
      prefs = True
      login_message = 'Logged in as ' + user.nickname()
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
      if users.is_current_user_admin():
        login_message += ' (admin)'
        admin = True
    else:
      login_message = 'Not logged in'
      url = users.create_login_url(self.request.uri)
      url_linktext = 'You have to log in to set preferences'
    template_values = {
      'message': None,
      'prefs': prefs,
      'login_message': login_message,
      'url': url,
      'url_linktext': url_linktext,
      'admin': admin,
      }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))


#class Prefs(webapp.RequestHandler):
#  def get(self):
#    user = users.get_current_user()
#    if not user:
#      self.response.out.write(
#        '<a href="' +
#        users.create_login_url('/prefs') +
#        '">Log in to set personal preferences</a>'
#      )
#    else:
#      logotxt = user.nickname()
#      conf = Conf(
#        user = user,
#        pagewidth = A4[0],
#        pageheight = A4[1],
#        logotxt = logotxt)
#      conf.put()
#    path = os.path.join(os.path.dirname(__file__), 'main.html')
#    self.response.out.write(template.render(path, template_values))


class Stamp():
    def __init__(self, w, h, text=None, label=None):
        self.w = w
        self.h = h
        self.text = text
        self.label = label

    def generate(self, pdf):
        p = pdf.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, self.h)
        p.lineTo(self.w, self.h)
        p.lineTo(self.w, 0)
        p.close()
        pdf.drawPath(p)
        if self.text:
            fs = 8
            pdf.setFont("Helvetica", fs)  # TODO:
            pdf.drawCentredString(self.w/2, self.h/2 - fs/2, self.text)
        if self.label:
            pdf.setFont("Helvetica", 10)  # TODO:
            pdf.drawCentredString(self.w/2, -5 * mm, self.label)


class Page():
    def __init__(self, conf):
        self.conf = conf
        self.lines = []
        self.nlines = 0
        self.size = {}

    def addSize(self, name, w, h):
        self.size[name] = (w, h)

    def addLine(self, line):
        stamps = []
        for s in line:
            (w, h) = self.size[s]
            stamps.append(Stamp(w, h))
        self.lines += [stamps]
        self.nlines += 1

    def _lineHeight(self, no):
        max = 0
        for s in self.lines[no]:
            if s.h > max:
                max = s.h
        return max

    def _sumLineHeight(self):
        sum = 0
        for l in range(self.nlines):
            sum += self._lineHeight(l)
        return sum

    def _sumStampWidth(self, lineno):
        sum = 0
        for s in self.lines[lineno]:
            sum += s.w
        return sum

    def _nstamps(self, lineno):
        return len(self.lines[lineno])

    def _generateStamps(self, pdf, w, h):
        """The layout algorithm of stamp frames.
        
        In principle, the free space is divided 
        evenly between the stamps. The distance
        of a stamp and the margin is the same as the
        distance between stamps.
        
        However, it is more common that stamps
        are in the middle and the space in between
        is limited by maxxdistance and maxydistance.
        
        If there is a label outside the stamp frame,
        it does not affect the placemente of frames.
        
        """
        conf = self.conf
        free_h = h - self._sumLineHeight()
        ydistance = free_h / (self.nlines + 1)
        if ydistance > conf.maxydistance:
            ydistance = conf.maxydistance
        topmargin = (free_h - (self.nlines - 1) * ydistance) / 2
        y = h - topmargin
        for l in range(self.nlines):
            y -= self._lineHeight(l)
            free_w = w - self._sumStampWidth(l)
            xdistance = free_w / (self._nstamps(l) + 1)
            if xdistance > conf.maxxdistance:
                xdistance = conf.maxxdistance
            leftmargin = (free_w - (self._nstamps(l) - 1) * xdistance) / 2
            x = leftmargin
            for s in self.lines[l]:
                pdf.saveState()
                pdf.translate(x,y)
                s.generate(pdf)
                pdf.restoreState()
                x += s.w + xdistance
            y -= ydistance

    def _generateMargins(self, pdf):
        conf = self.conf
        p = pdf.beginPath()
        p.moveTo(conf.leftmargin, conf.bottommargin)
        p.lineTo(conf.leftmargin, conf.pageheight - conf.topmargin)
        p.lineTo(conf.pagewidth - conf.leftmargin, conf.pageheight - conf.topmargin)
        p.lineTo(conf.pagewidth - conf.leftmargin, conf.bottommargin)
        p.close()
        pdf.drawPath(p)

    def _generateFooter(self, pdf):
        conf = self.conf
        y = conf.bottommargin - 12 - 3
        pdf.setFont("Helvetica", 12)  # TODO:
        pdf.drawString(conf.leftmargin, y, conf.leftfooter)
        pdf.drawRightString(conf.pagewidth - conf.leftmargin, y, conf.rightfooter)

    def generate(self, pdf):
        conf = self.conf
        self._generateMargins(pdf)
        self._generateFooter(pdf)
        # change coordinates to exclude margins
        pdf.translate(conf.leftmargin, conf.bottommargin)
        width = conf.pagewidth - conf.leftmargin - conf.rightmargin
        height = conf.pageheight - conf.topmargin - conf.bottommargin
        pdf.setFont("Helvetica", 36)  #TODO:
        pdf.drawCentredString(width/2, height - conf.header1pos, conf.header1)
        pdf.setFont("Helvetica", 18)  # TODO:
        pdf.drawCentredString(width/2, height - conf.header2pos, conf.header2)
        # change coordinates to exclude header
        height -= conf.header2pos
        self._generateStamps(pdf, width, height)
        pdf.showPage()


class Conf:
    """Class where to collect page configuration values.

    Configuration variables can be accessed as:
    conf = Conf()
    conf.attr = ...  # or setattr(conf, attr, val) if attr is variable
    a = conf.attr  # or getattr(conf, attr) if attr is variable
    if hasattr(conf, attr):  # is needed because attribute
        ...  # must not be accessed at all if it does not exist

    The usage here is to first set configuration values
    from the URL, then overwrite those values not set 
    with default value by calling method set_default().
    Then, the value is overwritten with the value that 
    is possibly found from the user profile.

    """
    def set_default(self,  attr,  val):
        """Set default value unless it is not already set from URL."""
        if not hasattr(self,  attr):
            setattr(self,  attr,  val)


class Pdf(webapp.RequestHandler):
    """Handles web request to print a pdf page."""
    def get(self):
#        user = users.get_current_user()
#      if not user:
#        user = users.User("__default__")
#      q = Conf.all()
#      q.filter("user =", user)
#      conf = q.get()
        error = ""
        conf = Conf()
        for n,  val in enumerate(self.request.path.split("/")):
            if n == 0:
                if not val == "":
                    error += "<p>Internal error, first field should be empty</p>"
            if n == 1:
                if not val == "pdf":
                    error += "<p>Internal error, second field should be 'pdf'</p>"
            elif n == 2:
                country = val
            elif n == 3:
                area = val
            elif n == 4:
                year = val
            elif n == 5:
                no = val
            elif n == 6:
                templ = val
        if not country:
            country="COUNTRY"
        if not area:
            area="Area"
        if not year:
            year="YYYY"
        if not no:
            no="#"
        if not templ:
            templ="ABBA-AA-BBB"
        if self.request.query_string:
            for assignment in self.request.query_string.split('&'):
                var,  val = assignment.split('=')
                setattr(conf,  var,  val)
        if not hasattr(conf,  "unit"):
            conf.unit = "mm"
        if conf.unit == "mm":
            unit = mm
        elif conf.unit == "in":
            unit = inch
        elif conf.unit == "pica":
            unit = pica
        elif conf.unit == "pt":
            unit = 1
        else:
            error += "unknown unit " + conf.unit +" (allowed: mm, in, pica, pt)"
            unit = mm
        for attr in ["pagewidth", "pageheight",
                    "topmargin",  "bottommargin",  "leftmargin",  "rightmargin", 
                    "header1pos",  "header2pos", 
                    "maxxdistance",  "maxydistance"]:
            if not hasattr(conf,  attr):
                continue
            try:
                setattr(conf,  attr,  float(getattr(conf,  attr)) * unit)
            except:
                error += "could not interpret size of " + attr + "\n"
        # TODO: shorthand page size "letter"
        conf.set_default("pagewidth",  A4[0])
        conf.set_default("pageheight", A4[1])
        conf.set_default("logotext", "Albumatic")
        conf.set_default("topmargin", 12 * mm)
        conf.set_default("bottommargin",  18 * mm)
        conf.set_default("leftmargin",  15 * mm)
        conf.set_default("rightmargin",  15 * mm)
        conf.set_default("header1pos",  25 * mm)
        conf.set_default("header1font",  ("Helvetica",  36))
        conf.set_default("header2pos",  35 * mm)
        conf.set_default("header2font", ("Helvetica",  18))
        conf.set_default("maxxdistance",  15 * mm)
        conf.set_default("maxydistance", 25 * mm)
        # TODO: check font descriptions
        # TODO: overwrite attributes with user's profile
        # TODO: translate header country to your local language
        # These settings you don't normally change, but you can
        conf.set_default("header1",  country)
        conf.set_default("header2",  area)
        conf.set_default("leftfooter",  conf.logotext)
        conf.set_default("rightfooter",  year + '/' + no)
        if error == "":
            self.response.headers['Content-Type'] = 'application/pdf'
            p = Page(conf)
            p.addSize('A', 30 * mm, 40 * mm)
            p.addSize('B', 20 * mm, 30 * mm)
            for line in templ.split('-'):
                p.addLine(line)
            pdf = Canvas(self.response.out, (conf.pagewidth, conf.pageheight))
            p.generate(pdf)
            pdf.save()
        else:
            self.response.out.write(error)


application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/pdf/.*', Pdf),
#    ('/resetdb', Resetdb),
#    ('/prefs', Prefs)
    ], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()

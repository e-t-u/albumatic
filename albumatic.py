#!/usr/bin/env python

import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


class Conf(db.Model):
  user = db.UserProperty()
  pagewidth = db.FloatProperty()
  pageheight = db.FloatProperty()
  logotxt = db.StringProperty()


class Resetdb(webapp.RequestHandler):
  def get(self):
    if not users.get_current_user():
      self.response.out.write(
        '<a href="' +
        users.create_login_url('/resetdb') +
        '">First, log in as admin</a>')
    elif users.is_current_user_admin():
      self.response.out.write('reset')
      conf = Conf(
        user = users.User("__default__"),
        pagewidth = A4[0],
        pageheight = A4[1],
#        pagewidth = 150*mm,
#        pageheight = 150*mm,
        logotxt = "Anonymous Albumatics")
      conf.save()
    else:
      self.response.out.write('non admin')


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(
"""
<html><body>
<a href="pdf/COUNTRY/Area/Year/No/ABA-BBB-AA">test print</a>
<a href="prefs">Set personal preferences</a>
<a href="%s">Logout</a>
<a href="/resetdb">Admin: reset defaults</a>
</body></html>
""" % users.create_logout_url("/")
    )


class Prefs(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.response.out.write(
        '<a href="' +
        users.create_login_url('/prefs') +
        '">Log in to set personal preferences</a>'
      )
    else:
      logotxt = user.nickname()
      conf = Conf(
        user = user,
        pagewidth = A4[0],
        pageheight = A4[1],
        logotxt = logotxt)
      conf.put()
      self.response.out.write(
"""
<html><body>
<p>logotext set as %s</p>
</body></html>
""" % logotxt
      )

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
      pdf.setFont("Helvetica", fs)
      pdf.drawCentredString(self.w/2, self.h/2 - fs/2, self.text)
    if self.label:
      pdf.setFont("Helvetica", 10)
      pdf.drawCentredString(self.w/2, -5 * mm, self.label)

class Page():
  def __init__(self,
      pagewidth = A4[0], pageheight = A4[1],
      topmargin = 12 * mm, bottommargin = 18 * mm,
      leftmargin = 15 * mm, rightmargin = 15 * mm,
      leftfooter = 'Albumatic', rightfooter = '1',
      header1pos = 25 * mm, header1font = ("Helvetica", 36),
      header1 = "COUNTRY",
      header2pos = 35 * mm, header2font = ("Helvetica", 18),
      header2 = "Area"):
    self.pageheight = pageheight
    self.pagewidth = pagewidth
    self.topmargin = topmargin
    self.bottommargin = bottommargin
    self.leftmargin = leftmargin
    self.rightmargin = rightmargin
    self.leftfooter = leftfooter
    self.rightfooter = rightfooter
    self.header1pos = header1pos
    self.header1font = header1font
    self.header1 = header1
    self.header2pos = header2pos
    self.header2font = header2font
    self.header2 = header2
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
    maxxdistance = 15 * mm
    maxydistance = 25 * mm
    free_h = h - self._sumLineHeight()
    ydistance = free_h / (self.nlines + 1)
    if ydistance > maxydistance:
      ydistance = maxydistance
    topmargin = (free_h - (self.nlines - 1) * ydistance) / 2
    y = h - topmargin
    for l in range(self.nlines):
      y -= self._lineHeight(l)
      free_w = w - self._sumStampWidth(l)
      xdistance = free_w / (self._nstamps(l) + 1)
      if xdistance > maxxdistance:
        xdistance = maxxdistance
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
    p = pdf.beginPath()
    p.moveTo(self.leftmargin, self.bottommargin)
    p.lineTo(self.leftmargin, self.pageheight - self.topmargin)
    p.lineTo(self.pagewidth - self.leftmargin, self.pageheight - self.topmargin)
    p.lineTo(self.pagewidth - self.leftmargin, self.bottommargin)
    p.close()
    pdf.drawPath(p)

  def _generateFooter(self, pdf):
    y = self.bottommargin - 12 - 3
    pdf.setFont("Helvetica", 12)
    pdf.drawString(self.leftmargin, y, self.leftfooter)
    pdf.drawRightString(self.pagewidth - self.leftmargin, y, self.rightfooter)

  def generate(self, pdf):
    self._generateMargins(pdf)
    self._generateFooter(pdf)
    # change coordinates to exclude margins
    pdf.translate(self.leftmargin, self.bottommargin)
    width = self.pagewidth - self.leftmargin - self.rightmargin
    height = self.pageheight - self.topmargin - self.bottommargin
    pdf.setFont("Helvetica", 36)
    pdf.drawCentredString(width/2, height - self.header1pos, self.header1)
    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(width/2, height - self.header2pos, self.header2)
    # change coordinates to exclude header
    height -= self.header2pos
    self._generateStamps(pdf, width, height)
    pdf.showPage()
    

class Pdf(webapp.RequestHandler):
  def post(self):
    a = 1
  def get(self, country="COUNTRY", area="Area", year="YYYY", no="#", templ="ABBA-AA-BBB"):
    self.response.headers['Content-Type'] = 'application/pdf'
    user = users.get_current_user()
    if not user:
      user = users.User("__default__")
    q = Conf.all()
    q.filter("user =", user)
    conf = q.get()
#    pagewidth = conf.pagewidth
#    pageheight = conf.pageheight
    pagewidth = A4[0]
    pageheight = A4[1]
    logotxt = conf.logotxt
    p = Page(
      header1 = country,
      header2 = area,
      leftfooter = logotxt,
      rightfooter = year + '/' + no)
    p.addSize('A', 30 * mm, 40 * mm)
    p.addSize('B', 20 * mm, 30 * mm)
    for line in templ.split('-'):
      p.addLine(line)
    pdf = Canvas(self.response.out, (pagewidth, pageheight))
    p.generate(pdf)
    pdf.save()


application = webapp.WSGIApplication([
  ('/', MainPage),
#  (r'/pdf/(.*)/(.*)/(.*)/(.*)', Pdf),
  (r'/pdf/(.*)/(.*)/(.*)/(.*)/(.*)', Pdf),
  ('/pdf', Pdf),
  ('/resetdb', Resetdb),
  ('/prefs', Prefs)
  ], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

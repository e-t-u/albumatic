#!/usr/bin/env python

#
# Google App Engine program to print stamp album pages
#
# In the current version there is no session but all the
# results depend only from the URL given without any stored
# state.
#
# The first version used session and those parts of the 
# program are not yet removed (they may be still needed).
# That is why there is so much confusing code commented out.
#
# This program requires Reportlab library to produce
# PDF documents. Note that it does not work with google app
# engine local development server but it works as a part
# of uploaded application (bug in Google app engine?).
#
# Esa Turtiainen, 2009-2011, licence GPL v3
#

import cgi
import urllib
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


class MainPage(webapp.RequestHandler):
  def get(self):
#    user = users.get_current_user()
    admin = False
    prefs = False
#    if user:
#      prefs = True
#      login_message = 'Logged in as ' + user.nickname()
#      url = users.create_logout_url(self.request.uri)
#      url_linktext = 'Logout'
#      if users.is_current_user_admin():
#        login_message += ' (admin)'
#        admin = True
#    else:
#      login_message = 'Not logged in'
#      url = users.create_login_url(self.request.uri)
#      url_linktext = 'You have to log in to set preferences'
    template_values = {
      'message': None,
#      'prefs': prefs,
#      'login_message': login_message,
#      'url': url,
#      'url_linktext': url_linktext,
#      'admin': admin,
      }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))


class Stamp():
    def __init__(self, w, h, text=None, label=None):
        self.w = w
        self.h = h
        self.text = text
        self.label = label

    def set_label(self, text):
	self.label = text

    def set_text(self, text):
	self.text = text

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
        for attr in dir(conf):
            if attr[:5] == 'size_':
                name = attr[5:]
                val = getattr(conf,  attr)
                self.size[name] = val

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


stamp_sizes = {
    "A": (20, 24),  # h
    "B": (20, 26),  # h
    "C": (21, 24),  # hl
    "D": (21.5, 26),  # hl
    "E": (21.5, 30),  # l
    "F": (23, 27.5),  # h
    "G": (24, 29),  # h
    "H": (24, 40),  # h
    "I": (24, 41),  # l
    "J": (25, 30),  # h
    "K": (25, 36),  # h
    "L": (26, 31),  # hl
    "M": (26, 36),  # h
    "N": (26, 40),  # hl
    "O": (26, 41),  # hl
    "P": (26, 43),  # hl
    "Q": (27.5, 33),  # h
    "R": (28, 34),  # h
    "S": (28, 39),  # h
    "T": (29, 36),  # h
    "U": (30, 39),  # h
    "V": (30, 41),  # h
    "W": (33, 55),  # hl
    "X": (35, 35),  # hl
    "Y": (41, 41),  # hl
    "Z": (41, 53),  # h
    "a": (24, 21),  # hl
    "b": (26, 21.5),  # hl
    "c": (29, 24),  # h
    "d": (31, 24),  # h
    "e": (31, 26),  # h
    "f": (33, 27.5),  # hl
    "g": (34, 28),  # h
    "h": (36, 25),  # h
    "i": (36, 26),  # hl
    "j": (36, 29),  # h
    "k": (39, 28),  # h
    "l": (39, 30),  # h
    "m": (40, 24),  # h
    "n": (40, 26),  # h
    "o": (40, 33),  # h
    "p": (41, 24),  # hl
    "q": (41, 26),  # hl
    "r": (41, 30),  # hl
    "s": (43, 26),  # hl
    "t": (46, 27.5),  # hl
    "u": (53, 41),  # h
    "v": (55, 33)  # hl
    }


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
                conf.country = urllib.unquote(val)
            elif n == 3:
                conf.area = urllib.unquote(val)
            elif n == 4:
                conf.year = urllib.unquote(val)
            elif n == 5:
                conf.no = urllib.unquote(val)
            elif n == 6:
                conf.template = val
        conf.set_default("country",  "COUNTRY")
        conf.set_default("area",  "Area")
        conf.set_default("year",  "YYYY")
        conf.set_default("no",  "#")
        conf.set_default("template",  "X")
        if self.request.query_string:
            for assignment in self.request.query_string.split('&'):
                try:
                    var,  val = assignment.split('=')
                    setattr(conf,  var,  val)
                except:
                    error += "<p>Empty assignment " + assignment + "</p>"
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
        # TODO: shorthand for page size "letter"
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
        conf.set_default("header1",  conf.country)
        conf.set_default("header2",  conf.area)
        conf.set_default("leftfooter",  conf.logotext)
        conf.set_default("rightfooter",  conf.year + '/' + conf.no)
        for attr in conf.__dict__:
            if attr[:5] == "size_":
                name = attr[5:]
                val = getattr(conf,  attr)
                size = val.split(",")
                if len(size) != 2:
                    error += "<p>size of " + name + "must be w,h</p>"
                try:
                    w = float(size[0]) * unit
                    h = float(size[1]) * unit
                except:
                    error += "<p>could not parse size " + name + "=" + val + "</p>"
                    w = 1.0
                    h = 1.0
                setattr(conf,  attr,  (w,  h))
        for key,  value in stamp_sizes.items():
            if not len(value) == 2:
                error += "<p>internal error: default size wrong</p>"
            try:
                w = float(value[0]) * mm
                h = float(value[1]) * mm
            except:
                error += "<p>internal error: default size wrong (not float)</p>"
            conf.set_default("size_" + key,  (w,  h))

	#
        # Arguments are prepared, ready to create Page
        #
        p = Page(conf)
        for line in conf.template.split('-'):
            p.addLine(line)
	for attr in conf.__dict__:
            if attr[:2] == "t_":
                try:
	            no = attr[2:]
                    row, col = no.split("_")
                    row = int(row) - 1
                    col = int(col) - 1
                    if row < 0: raise Exception
                    if col < 0: raise Exception
                except:
                    error += "<p>Not a valid nunber pair in %s</p>" % attr
		    row = 0
                    col = 0
                text = getattr(conf, attr)
                text = urllib.unquote(text)
                try:
                    p.lines[row][col].text = text
                except:
                    error += "<p>Stamp does not exist %s</p>" % attr
	for attr in conf.__dict__:
            if attr[:2] == "l_":
                try:
	            no = attr[2:]
                    row, col = no.split("_")
                    row = int(row) - 1
                    col = int(col) - 1
                    if row < 0: raise Exception
                    if col < 0: raise Exception
                except:
                    error += "<p>Not a valid nunber pair in %s</p>" % attr
		    row = 0
                    col = 0
                text = getattr(conf, attr)
                text = urllib.unquote(text)
                try:
                    p.lines[row][col].label = text
                except:
                    error += "<p>Stamp does not exist %s</p>" % attr
        if hasattr(conf, "placeholders"):
            # default is "both" - only case when labels is not shown is when
            # "texts" is defined and vice versa
            showlabels = (not conf.placeholders == "texts")
            showtexts = (not conf.placeholders == "labels")
            for row, l in enumerate(p.lines):
                for col, s in enumerate(l):
                    # TODO: only if there is no previous value
                    # TODO: placeholders=label/text/both (default)
                    if showlabels and not p.lines[row][col].label:
                        p.lines[row][col].label = "%s,%s" % (row + 1, col + 1)
                    if showtexts and not p.lines[row][col].text:
                        p.lines[row][col].text = "%s,%s" % (row + 1, col + 1)
                
        pdf = Canvas(self.response.out, (conf.pagewidth, conf.pageheight))
        p.generate(pdf)

        #
        # If there are errors, we return them as HTML, otherwise
        # we return the PDF
        #
        if error == "":
            self.response.headers['Content-Type'] = 'application/pdf'
            pdf.save()
        else:
            self.response.out.write(error)


# TODO: Pdf must be cleaned to be re-usable
# Note that ReportLab SVG generation is beta
# it would be safer to generate SVG from scratch
# (python svgwrite)
#class Svg(webapp.RequestHandler):
#    """Handles web request to return a SVG page."""
#    def get(self):
#        self.response.headers['Content-Type'] = 'image/svg+xml'


application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/pdf.*', Pdf),
#    ('/svg.*', Svg),
    ], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()

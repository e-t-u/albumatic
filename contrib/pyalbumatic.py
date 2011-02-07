# -*- coding: UTF-8 -*-
#
# Library pyalbumatic to use service albumatic.appspot.com
# (or some other instance of the same service)
#

import urllib
import urllib2

pathattrs = ("country",  "area",  "year",  "no",  "template",  "filename")

class Albumatic:
    """Object of class Albumactic represents a connection to albumatic service
    (default albumatic.appspot.com). Configuration attributes are set into a stack
    so that it is possible to push previous values as defaults and set new values.
    Pop removes one level of defaults.
    """
    def __init__(self, host="albumatic.appspot.com", verbose=False):
        """Initialize service host name and set defaults to attribute stack"""
        self.verbose = verbose
        self.host = host
        self.stack = []
        self.stack.append({})

    def __setitem__(self,  attr,  val):
        """Assign to albumatic attribute like a dictionary a["country"] = "USA" """
        self.stack[-1][attr] = val

    def __getitem__(self,  attr):
        """Return the attribute value. If not defined, the topmost default value of the stack is returned.
        It is not error if the value is not there but None is returned.
        """
        for d in reversed(self.stack):
            if attr in d:
                return d[attr]
        return None

    def __delitem__(self,  attr):
        """Delete attribute value in the current scope like in a dictionary.
        The value returns to the default defined in the upper stack.
        """
        del self.stack[-1][attr]

    def attrpush(self):
        """Current attribute assignments turn into defaults and assignments after this are poppable"""
        self.stack.append({})

    def attrpop(self):
        """Remove all attribute assignments done after last push"""
        self.stack.pop()

    def __iter__(self):
        """Albumatic object can be used in for statement and it returns all nonpath attributes"""
        attrlist = []
        for d in reversed(self.stack):
            for attr in d.keys():
                if attr in pathattrs:
                    continue
                if attr not in attrlist:
                    yield(attr)
                    attrlist.append(attr)

    def url(self):
        """Return URL of the current state of the Albumatic object as string"""
        url = "http://" + self.host + "/pdf"
        for attr in pathattrs:
            if self[attr]:
                url += "/" + urllib.quote(self[attr])
            else:
                url += "/"
        attrlist = []
        for attr in self:
            attrlist.append(urllib.quote(attr) + "=" + urllib.quote(self[attr]))
        attrstr = "&".join(attrlist)
        if attrstr:
            url +="?" + "&".join(attrlist)
        return url

    def getpdf(self):
        """Return PDF from the server using the current settings.
        PDF is returned as a string.
        """
        try:
            f = urllib2.urlopen(self.url())
        except urllib2.URLError:
            print "Could not open URL ",  self.url()
            return ""
        if not f.info().gettype() == "application/pdf":
            print "Return document is not PDF: ",  self.url()
            return ""
        str = f.read()
        f.close()
        if self.verbose:
            print "got ",  self.url()
        return str

    def writefile(self,  file=None):
        """Write the PDF of the current settings to a file.
        Default file name is in attribute filename.
        """
        if file:
            filename = file
        else:
            filename = self["filename"]
        if not filename:
            print "No default filename given"
            raise IOError
        try:
            f = open(filename,  "w")
        except:
            print "Could not open file for write: ",  filename
            raise IOError
        f.write(self.getpdf())
        f.close()
        if self.verbose:
            print "Wrote" + filename


def selftest():
    print "Testing:"
    a = Albumatic(verbose = False)
    print "Empty URL: ",  a.url()
    a.attrpush()
    a["country"] = "country"
    a["area"] = "area"
    a["year"] = "year"
    a["no"] = "no"
    a["template"] = "template"
    a["filename"] = "filename"
    print "Pathattributes set: ",  a.url()
    a.attrpush()
    a["year"] = "1999"
    print "Year overwritten: ",  a.url()
    a.attrpop()
    print "Return to default: ",  a.url()
    a.attrpop()
    print "Return to empty: ",  a.url()
    a.attrpush()
    a["a1"] = "v1"
    print "Added an attribute a1: ",  a.url()
    a["a2"] = "v2"
    print "Added attribute a2: ",  a.url()
    a.attrpush()
    a["a1"] = "new value"
    print "Pushed new value to a1: ",  a.url()
    a.attrpop()
    print "Popped to previous values: ",  a.url()
    a.attrpop()
    a.attrpush()
    a["area"] = "Îñţérñåţîöñåļîžåţîöñ"
    a["Îñţérñåţîöñåļîžåţîöñ"] = "Îñţérñåţîöñåļîžåţîöñ"
    print "Internationalization in path attribute and in attribute name and value: ",  a.url()
    a.attrpop()
    pdf = a.getpdf()
    if pdf:
        print "Was able to return PDF from server using empty settings",  a.url()
    else:
        print "Was not able to return PDF from server using empty settings",  a.url()
    import tempfile
    a.attrpush()
    t = tempfile.NamedTemporaryFile()
    a["filename"] = t.name
    t.close() # we just use the unique name for testing
    print "Testing writing based on attribute filename"
    try:
        a.writefile()
    except IOError:
        print "Something went wrong in writing to temporary file",  a["filename"]
    else:
        print "Writing succeeded to temporary file",  a["filename"]
    a.attrpop()
    print "Testing writing based on given filename"
    t = tempfile.NamedTemporaryFile()
    filename = t.name
    t.close()
    try:
        a.writefile(file=filename)
    except IOError:
        print "Something went wrong in writing to temporary file",  filename
    else:
        print "Writing succeeded to temporary file",  filename


if __name__ == "__main__":
    selftest()

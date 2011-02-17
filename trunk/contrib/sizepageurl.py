#!/usr/bin/env/python

#
# Program to generate URL's to print all the stamp sizes
# Note: this is for Python 2.6, in Python 3 next->__next__
#

def atov():
    for c in range(0,22):
        yield chr(ord('a') + c)

def AtoZ():
    for c in range(0,26):
        yield chr(ord('A') + c)

def url(urlbase, rows, genfunc):
    a = genfunc()
    rowtemplates = []
    texts = []
    try:
        for row in range(len(rows)):
            rowtemplate = ""
            for col in range(rows[row]):
                ch = a.next()
                rowtemplate += ch
                texts.append("t_" + str(row + 1) + "_" + str(col + 1) + "=" + ch)
            rowtemplates.append(rowtemplate)
    except StopIteration:
        None
    url = urlbase
    url += "?"
    url += "template=" + "-".join(rowtemplates)
    url += "&"
    url += "&".join(texts)
    return url

rows = (5, 4, 4, 4, 3, 2)
urlbase = "http://albumatic.appspot.com/pdf/Sizes/Landscape///landscape.pdf"
print url(urlbase, rows, atov)

rows = (7, 6, 5, 4, 4)
urlbase = "http://albumatic.appspot.com/pdf/Sizes/Potrait///portrait.pdf"
print url(urlbase, rows, AtoZ)

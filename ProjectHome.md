You give an URL that describes your album page, albumatic returns a PDF file containing that page. Add album links to your www-page, bookmarks, blog, send them as emails... Just anything. You can describe an album in one web page and use mass downloader (like FlashGot) to download the whole album with one command.

The current implementation an early alpha.

The system is hosted in Google App engine in http://albumatic.appspot.com but you are free to host it in the system of your own. Google is pretty fast:-) Note that this is an free account in Google App Engine which means that theoretically we may hit daily quota there (thousands of pages per day). If that happens, just try next day or obtain your own free account and install this software.

The current implementation uses ReportLab toolkit to generate PDF. The compatible version is copied to version management here. ReportLab toolkit uses BSD license. Note that this version of Reportlab does not work with Google App Engine local dev\_appserver.py but it works when it is uploaded to the real engine.
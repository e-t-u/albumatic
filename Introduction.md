# New! #

I am re-activating development of this program.

The new idea is not to make a database into the program but to make a generic
tool that can generate an Album page based on URL. The URL contains all the
necessary information to build the page.

That means that the album pages per se can be located in this Wiki
or in any other web page.


# Introduction #

Albumatic is a tool to generate stamp album pages.


# Details #

You can go to http://albumatic.appspot.com/. There is some log-in
and preferences trials that are not usable yet.

But, you can test the lay-out engine by giving directly the URL like:
http://albumatic.appspot.com/pdf/COUNTRY/Area/year/page/ABBA-BBB-AA.

You get a PDF album page with headers from URL COUNTRY and Area and
footer from year/page (A4 page size!). The lay-out of stamps is taken
from the last string. There are currently only two sizes of stamp places
called A and B. In this example, there are three rows containing 4, 3 and 2
stamps on rows. A is a larger stamp and B smaller.

PDF is generated using ReportLab Python module.


# TODO #

I am now considering if I should give all the parameters in the URL
or to use database to store them. In Google AppServer the easy way is
that I require the user to log in to set complex parameters (new sizes,
pagesize). I don't copletely like the approach but it is easy. The most
acute things are to get definition of sizes, pagesize and stamp labels.
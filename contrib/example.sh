#!/bin/sh

#
# This is an example bash (Linux) script to retrieve several 
# albumatic pages automatically using wget.
#

URL=http://albumatic.appspot.com/pdf
ALBUM=USA/Definitives/2009
ATTR=unit=in&pagewidth=8.5&pageheight=11  # letter

# very short and lazy shorthands
U=$URL/$ALBUM
A="?$ATTR"

# get pages, modify templates here
wget $U/1/ABBA-hh-XX$A -O 1.pdf
wget $U/2/BBB-ccc-ddd$A -O 2.pdf

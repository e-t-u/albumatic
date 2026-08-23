#!/bin/sh
# Example script to retrieve Albumatic pages automatically via HTTP

URL=http://localhost:8000/pdf
ALBUM=USA/Definitives/2009
ATTR="unit=in&pagewidth=8.5&pageheight=11"  # letter

# very short and lazy shorthands
U=$URL/$ALBUM
A="?$ATTR"

# get pages, modify templates here
curl -s "$U/1/ABBA-hh-XX$A" -o 1.pdf
curl -s "$U/2/BBB-ccc-ddd$A" -o 2.pdf


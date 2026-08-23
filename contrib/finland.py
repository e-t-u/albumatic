# -*- coding: UTF-8 -*-

import os
import pyalbumatic

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finland_album")
os.makedirs(OUT_DIR, exist_ok=True)

a = pyalbumatic.Albumatic(verbose=True)

# Shared album defaults
a["country"] = "Suomi — Finland"
a["placeholders"] = "none"
a.attrpush()

# Page 1: 1856 Soikiomerkit
a.attrpush()
a["year"] = "1856"
a["no"] = "1"
a["area"] = "1856 Oval Issue"
a["template"] = "ee-e"
a["t_1_1"] = "5 kop"
a["t_1_2"] = "10 kop"
a["t_2_1"] = "5 kop"
a["l_1_1"] = "Small Pearl"
a["l_2_1"] = "Large Pearl"
a.writefile(os.path.join(OUT_DIR, "finland_1856.pdf"))
a.attrpop()

a.attrpush()
a["year"] = "1860"
a["no"] = "2"
a["area"] = "1860 Large perforation, Currency Kop"
a["template"] = "LL-LL"
a["t_1_1"] = "5 kop//blue"
a["t_1_2"] = "10 kop//rose"
a["t_2_1"] = "5 kop//dark blue"
a["t_2_2"] = "10 kop//carmine"
a["l_1_1"] = "Perf. I"
a["l_1_2"] = "Perf. I"
a["l_2_1"] = "Perf. II"
a["l_2_2"] = "Perf. II"
a.writefile(os.path.join(OUT_DIR, "finland_1860.pdf"))
a.attrpop()

# Page 3: 1866 Penni- ja markka-arvot
a.attrpush()
a["year"] = "1866"
a["no"] = "3"
a["area"] = "1866 Currency Penni and Markka (Perf. II)"
a["template"] = "LL-LL-L"
a["t_1_1"] = "5 p//brown"
a["t_1_2"] = "10 p//black"
a["t_2_1"] = "20 p//blue"
a["t_2_2"] = "40 p//rose"
a["t_3_1"] = "1 mk//brown"
a.writefile(os.path.join(OUT_DIR, "finland_1866.pdf"))
a.attrpop()

a.attrpush()
a["year"] = "1875"
a["no"] = "4"
a["area"] = "1875–1882 Value in all Corners"
a["template"] = "D-DDDD-DDDD"
a["t_1_1"] = "32 p//carmine"
a["t_2_1"] = "2 p//gray"
a["t_2_2"] = "5 p//orange"
a["t_2_3"] = "8 p//green"
a["t_2_4"] = "10 p//olive brown"
a["t_3_1"] = "20 p//ultramarine"
a["t_3_2"] = "25 p//carmine"
a["t_3_3"] = "32 p//pink"
a["t_3_4"] = "1 mk//violet"
a["l_1_1"] = "Copenhagen print//14x13½"
a["l_2_1"] = "Helsinki print"
a["l_2_2"] = "Helsinki print"
a["l_2_3"] = "Helsinki print"
a["l_2_4"] = "Helsinki print"
a["l_3_1"] = "Helsinki print"
a["l_3_2"] = "Helsinki print"
a["l_3_3"] = "Helsinki print//Perf. 11"
a["l_3_4"] = "Helsinki print"
a.writefile(os.path.join(OUT_DIR, "finland_1875.pdf"))
a.attrpop()

a.attrpush()
a["year"] = "1885"
a["no"] = "5"
a["area"] = "1885 New Colors"
a["template"] = "DD-DD-DDD"
a["t_1_1"] = "5 p//green"
a["t_1_2"] = "10 p//rose"
a["t_2_1"] = "20 p//orange"
a["t_2_2"] = "25 p//blue"
a["t_3_1"] = "1 mk//gray/pink"
a["t_3_2"] = "5 mk//green/pink"
a["t_3_3"] = "10 mk//brown/pink"
a.writefile(os.path.join(OUT_DIR, "finland_1885.pdf"))
a.attrpop()

# Page 6: 1889 Value Only in Upper Corners
a.attrpush()
a["year"] = "1889"
a["no"] = "6"
a["area"] = "1889 Value Only in Upper Corners"
a["template"] = "DDD-DD-DDD"
a["t_1_1"] = "2 p//gray"
a["t_1_2"] = "5 p//green"
a["t_1_3"] = "10 p//pink"
a["t_2_1"] = "20 p//orange"
a["t_2_2"] = "25 p//blue"
a["t_3_1"] = "1 mk//gray/pink"
a["t_3_2"] = "5 mk//green/pink"
a["t_3_3"] = "10 mk//brown/pink"
a.writefile(os.path.join(OUT_DIR, "finland_1889.pdf"))
a.attrpop()

# Page 7: 1891 Russian Pattern (Venäläismalli)
a.attrpush()
a["year"] = "1891"
a["no"] = "7"
a["area"] = "1891 Russian Pattern (Venäläismalli)"
a["template"] = "DDD-DDD-DDDD-LLL"
a["t_1_1"] = "1 kop//orange"
a["t_1_2"] = "2 kop//green"
a["t_1_3"] = "3 kop//rose"
a["t_2_1"] = "4 kop//carmine/rose"
a["t_2_2"] = "7 kop//blue"
a["t_2_3"] = "10 kop//dark blue"
a["t_3_1"] = "14 kop//rose/blue"
a["t_3_2"] = "20 kop//blue/carmine"
a["t_3_3"] = "35 kop//violet/green"
a["t_3_4"] = "50 kop//green/violet"
a["t_4_1"] = "1 rbl//brown/orange"
a["t_4_2"] = "3.50 rbl//black/yellow"
a["t_4_3"] = "7 rbl//black/orange"
a.writefile(os.path.join(OUT_DIR, "finland_1891.pdf"))
a.attrpop()

a.attrpop()
print("Generated 7 album pages for Finland 1856-1891 in contrib/finland_album/.")

# -*- coding: UTF-8 -*-
#
# Generate classic stamp album pages for Finland 1856-1889 (Klassiset vaakunamerkit)
#

import pyalbumatic

a = pyalbumatic.Albumatic(verbose=True)

# Shared album defaults
a["country"] = "Suomi — Finland"
a["placeholders"] = "none"
a.attrpush()

# Page 1: 1856 Soikiomerkit
a.attrpush()
a["year"] = "1856"
a["no"] = "1"
a["area"] = "1856 Soikiomalli — Oval Issue"
a["template"] = "ee-e"
a["t_1_1"] = "5 kop"
a["t_1_2"] = "10 kop"
a["t_2_1"] = "5 kop"
a["l_1_1"] = "Small Pearl"
a["l_2_1"] = "Large Pearl"
a.writefile("finland_1856.pdf")
a.attrpop()

# Page 2: 1860 Isoposkihampaiset
a.attrpush()
a["year"] = "1860"
a["no"] = "1"
a["area"] = "1860 Vaakunamalli — Serpentine Roulette I"
a["template"] = "LL-LL"
a["t_1_1"] = "5 kop. sininen"
a["t_1_2"] = "10 kop. ruusu"
a["t_2_1"] = "5 kop. tumma sini"
a["t_2_2"] = "10 kop. karmiini"
a["l_1_1"] = "Hammaste I"
a["l_1_2"] = "Hammaste I"
a["l_2_1"] = "Uurteeton"
a["l_2_2"] = "Ohut paperi"
a.writefile("finland_1860.pdf")
a.attrpop()

# Page 3: 1866 Penni- ja markka-arvot
a.attrpush()
a["year"] = "1866"
a["no"] = "1"
a["area"] = "1866 Vaakunamalli — Penni- ja markka-arvot (Hammaste II)"
a["template"] = "LLL-LL"
a["t_1_1"] = "5 p. ruskea"
a["t_1_2"] = "10 p. musta"
a["t_1_3"] = "20 p. sininen"
a["t_2_1"] = "40 p. ruusu"
a["t_2_2"] = "1 mk ruskea"
a["l_1_1"] = "Hammaste II"
a["l_1_2"] = "Vaalea lila"
a["l_1_3"] = "Sininen"
a["l_2_1"] = "Ruusupaperi"
a["l_2_2"] = "Keltanahka"
a.writefile("finland_1866.pdf")
a.attrpop()

# Page 4: 1875 Helsingin painos
a.attrpush()
a["year"] = "1875"
a["no"] = "1"
a["area"] = "1875–1882 Helsingin painos — Vaakunakuviot"
a["template"] = "DDDD-DDD"
a["t_1_1"] = "2 p. harmaa"
a["t_1_2"] = "5 p. oranssi"
a["t_1_3"] = "8 p. vihreä"
a["t_1_4"] = "10 p. ruskea"
a["t_2_1"] = "20 p. sininen"
a["t_2_2"] = "32 p. karmiini"
a["t_2_3"] = "1 mk violetti"
a["l_1_1"] = "Hki 11"
a["l_1_2"] = "Hki 11"
a["l_1_3"] = "Hki 12½"
a["l_1_4"] = "Hki 12½"
a["l_2_1"] = "Hki 12½"
a["l_2_2"] = "Hki 12½"
a["l_2_3"] = "Hki 14"
a.writefile("finland_1875.pdf")
a.attrpop()

# Page 5: 1885 Penniarvot
a.attrpush()
a["year"] = "1885"
a["no"] = "1"
a["area"] = "1885 Vaakunamalli — Yksiväriset penniarvot"
a["template"] = "DDD-DDD"
a["t_1_1"] = "2 p. harmaa"
a["t_1_2"] = "5 p. vihreä"
a["t_1_3"] = "10 p. ruusu"
a["t_2_1"] = "20 p. oranssi"
a["t_2_2"] = "25 p. sininen"
a["t_2_3"] = "50 p. ruskea"
a["l_1_1"] = "12½ Hki"
a["l_1_2"] = "12½ Hki"
a["l_1_3"] = "Helsinki"
a["l_2_1"] = "Tampere"
a["l_2_2"] = "Turku / Åbo"
a["l_2_3"] = "Viipuri"
a.writefile("finland_1885_penni.pdf")
a.attrpop()

# Page 6: 1885 Markka-arvot
a.attrpush()
a["year"] = "1885"
a["no"] = "2"
a["area"] = "1885 Vaakunamalli — Kaksiväriset markka-arvot"
a["template"] = "GGG"
a["t_1_1"] = "1 mk harmaa/ruusu"
a["t_1_2"] = "5 mk vihreä/ruusu"
a["t_1_3"] = "10 mk ruskea/ruusu"
a["l_1_1"] = "1 Mk (Hki 12½)"
a["l_1_2"] = "5 Mk (Hämeenlinna)"
a["l_1_3"] = "10 Mk (Kuopio)"
a.writefile("finland_1885_markka.pdf")
a.attrpop()

# Page 7: 1889 Penniarvot
a.attrpush()
a["year"] = "1889"
a["no"] = "1"
a["area"] = "1889 Vaakunamalli — Penniarvot (Uusi kaiverrus)"
a["template"] = "DDD-DDD"
a["t_1_1"] = "2 p. harmaa"
a["t_1_2"] = "5 p. vihreä"
a["t_1_3"] = "10 p. punainen"
a["t_2_1"] = "20 p. keltainen"
a["t_2_2"] = "25 p. sininen"
a["t_2_3"] = "50 p. ruskea"
a["l_1_1"] = "12½ Hki"
a["l_1_2"] = "12½ Hki"
a["l_1_3"] = "Östermyra"
a["l_2_1"] = "Vaasa / Wasa"
a["l_2_2"] = "Oulu / Uleåborg"
a["l_2_3"] = "Pori"
a.writefile("finland_1889_penni.pdf")
a.attrpop()

# Page 8: 1889 Markka-arvot & Åland
a.attrpush()
a["year"] = "1889"
a["no"] = "2"
a["area"] = "1889 Vaakunamalli — Markka-arvot & Åland"
a["template"] = "GGG"
a["t_1_1"] = "1 mk harmaa"
a["t_1_2"] = "5 mk vihreä"
a["t_1_3"] = "10 mk ruskea"
a["l_1_1"] = "1 Mk (Helsingfors)"
a["l_1_2"] = "5 Mk (Mariehamn)"
a["l_1_3"] = "10 Mk (Saimaa)"
a.writefile("finland_1889_markka.pdf")
a.attrpop()

a.attrpop()
print("Generated 8 album pages for Finland 1856-1889.")

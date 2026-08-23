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
a["area"] = "1856 Soikiomalli — First Oval Issue (Portostämpel)"
a["template"] = "BB-BB"
a["t_1_1"] = "5 kop. sininen"
a["t_1_2"] = "10 kop. punainen"
a["t_2_1"] = "5 kop. (pienihelminen)"
a["t_2_2"] = "10 kop. (isohelminen)"
a["l_1_1"] = "Pystyurapaperi (Wove)"
a["l_1_2"] = "Pystyurapaperi"
a["l_2_1"] = "Vaakasuora urapaperi"
a["l_2_2"] = "Valkoinen paperi"
a.writefile("finland_1856.pdf")
a.attrpop()

# Page 2: 1860 Isoposkihampaiset
a.attrpush()
a["year"] = "1860"
a["no"] = "1"
a["area"] = "1860 Vaakunamalli — Serpentine Roulette I"
a["template"] = "BB-BB"
a["t_1_1"] = "5 kop. sininen"
a["t_1_2"] = "10 kop. ruusunpunainen"
a["t_2_1"] = "5 kop. tummansininen"
a["t_2_2"] = "10 kop. karmiini"
a["l_1_1"] = "Hammaste I (Isoposkinen)"
a["l_1_2"] = "Hammaste I"
a["l_2_1"] = "Paperi uurteeton"
a["l_2_2"] = "Ohut paperi"
a.writefile("finland_1860.pdf")
a.attrpop()

# Page 3: 1866 Penni- ja markka-arvot
a.attrpush()
a["year"] = "1866"
a["no"] = "1"
a["area"] = "1866 Vaakunamalli — Penni- ja markka-arvot (Hammaste II)"
a["template"] = "BBB-BB"
a["t_1_1"] = "5 p. ruskea"
a["t_1_2"] = "10 p. musta"
a["t_1_3"] = "20 p. sininen"
a["t_2_1"] = "40 p. ruusunpunainen"
a["t_2_2"] = "1 mk ruskea"
a["l_1_1"] = "Serpentine Roulette II"
a["l_1_2"] = "Vaalea lila paperi"
a["l_1_3"] = "Sininen paperi"
a["l_2_1"] = "Ruusu paperi"
a["l_2_2"] = "Keltanahkanen paperi"
a.writefile("finland_1866.pdf")
a.attrpop()

# Page 4: 1875 Helsingin painos
a.attrpush()
a["year"] = "1875"
a["no"] = "1"
a["area"] = "1875–1882 Helsingin painos — Vaakunakuviot"
a["template"] = "AAAA-AAA"
a["t_1_1"] = "2 p. harmaa"
a["t_1_2"] = "5 p. oranssi"
a["t_1_3"] = "8 p. vihreä"
a["t_1_4"] = "10 p. ruskea"
a["t_2_1"] = "20 p. sininen"
a["t_2_2"] = "32 p. karmiini"
a["t_2_3"] = "1 mk violetti"
a["l_1_1"] = "Hammaste 11"
a["l_1_2"] = "Hammaste 11"
a["l_1_3"] = "Hammaste 12½"
a["l_1_4"] = "Hammaste 12½"
a["l_2_1"] = "Hammaste 12½"
a["l_2_2"] = "Hammaste 12½"
a["l_2_3"] = "Hammaste 14"
a.writefile("finland_1875.pdf")
a.attrpop()

# Page 5: 1885 Penniarvot
a.attrpush()
a["year"] = "1885"
a["no"] = "1"
a["area"] = "1885 Vaakunamalli — Yksiväriset penniarvot"
a["template"] = "AAA-AAA"
a["t_1_1"] = "2 p. harmaa"
a["t_1_2"] = "5 p. vihreä"
a["t_1_3"] = "10 p. ruusu"
a["t_2_1"] = "20 p. oranssi"
a["t_2_2"] = "25 p. sininen"
a["t_2_3"] = "50 p. ruskea"
a["l_1_1"] = "Hammaste 12½"
a["l_1_2"] = "Hammaste 12½"
a["l_1_3"] = "Helsinki / Helsingfors"
a["l_2_1"] = "Tampere / Tammerfors"
a["l_2_2"] = "Turku / Åbo"
a["l_2_3"] = "Viipuri / Wiborg"
a.writefile("finland_1885_penni.pdf")
a.attrpop()

# Page 6: 1885 Markka-arvot
a.attrpush()
a["year"] = "1885"
a["no"] = "2"
a["area"] = "1885 Vaakunamalli — Kaksiväriset markka-arvot"
a["template"] = "BBB"
a["t_1_1"] = "1 mk harmaa & ruusu"
a["t_1_2"] = "5 mk vihreä & ruusu"
a["t_1_3"] = "10 mk ruskea & ruusu"
a["l_1_1"] = "1 Markka (Hammaste 12½)"
a["l_1_2"] = "5 Markkaa (Hämeenlinna)"
a["l_1_3"] = "10 Markkaa (Kuopio)"
a.writefile("finland_1885_markka.pdf")
a.attrpop()

# Page 7: 1889 Penniarvot
a.attrpush()
a["year"] = "1889"
a["no"] = "1"
a["area"] = "1889 Vaakunamalli — Penniarvot (Uusi kaiverrus)"
a["template"] = "AAA-AAA"
a["t_1_1"] = "2 p. harmaa"
a["t_1_2"] = "5 p. vihreä"
a["t_1_3"] = "10 p. punainen"
a["t_2_1"] = "20 p. keltainen"
a["t_2_2"] = "25 p. sininen"
a["t_2_3"] = "50 p. ruskea"
a["l_1_1"] = "Hammaste 12½"
a["l_1_2"] = "Hammaste 12½"
a["l_1_3"] = "Östermyra & Ähtäri"
a["l_2_1"] = "Vaasa / Wasa"
a["l_2_2"] = "Oulu / Uleåborg"
a["l_2_3"] = "Pori / Björneborg"
a.writefile("finland_1889_penni.pdf")
a.attrpop()

# Page 8: 1889 Markka-arvot & Åland
a.attrpush()
a["year"] = "1889"
a["no"] = "2"
a["area"] = "1889 Vaakunamalli — Markka-arvot & Åland"
a["template"] = "BBB"
a["t_1_1"] = "1 mk harmaa"
a["t_1_2"] = "5 mk vihreä"
a["t_1_3"] = "10 mk ruskea"
a["l_1_1"] = "1 Markka (Helsingfors)"
a["l_1_2"] = "5 Markkaa (Åland — Mariehamn)"
a["l_1_3"] = "10 Markkaa (Saimaan höyrylaiva)"
a.writefile("finland_1889_markka.pdf")
a.attrpop()

a.attrpop()
print("Generated 8 album pages for Finland 1856-1889.")

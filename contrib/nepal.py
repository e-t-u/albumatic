# -*- coding: UTF-8 -*-
#
# Generate some album pages from Nepal stamps
#

import pyalbumatic

a = pyalbumatic.Albumatic(verbose=True)

#defaults
a["country"] = "Nepal"
a["no"] = "1" # other no's used only if there are many pages in the same year
a["placeholders"] = "texts"
a.attrpush()

# Crossed knives
a["year"] = "1881"
#a["size_X"] = "10,20" # currently can not be used due to quotation bug in service

# page 1
a.attrpush()
a["area"] = "1881 Crossed Knives, European paper"
a["template"] = "XXX-X-XXX-X"
a["l_1_1"] = "pin perf. 1A"
a["l_1_2"] = "2A"
a["l_1_3"] = "4A"
a["t_1_1"] = "blue"
a["t_1_2"] = "lila"
a["t_1_3"] = "green"
a["l_2_1"] = "Recut 1899 1A"
a["t_2_1"] = "blue"
a["l_3_1"] = "no perf. 1A"
a["l_3_2"] = "2A"
a["l_3_3"] = "4A"
a["t_3_1"] = "blue"
a["t_3_2"] = "lila"
a["t_3_3"] = "green"
a["l_4_1"] = "Recut 1899 1A"
a["t_4_1"] = "blue"
a.writefile("1.pdf")
a.attrpop()

# Page 2
a.attrpush()
a["no"] = "2"
a["area"] = "1881 Crossed Knives, Good Local paper"
a["template"] = "XXX-XXX"
a["l_1_1"] = "thin 1A"
a["l_1_2"] = "2A"
a["l_1_3"] = "4A"
a["t_1_1"] = "blue"
a["t_1_2"] = "blue"
a["t_1_3"] = "green"
a["l_2_1"] = "thick 1A"
a["l_2_2"] = "2A"
a["l_2_3"] = "4A"
a["t_2_1"] = "blue"
a["t_2_2"] = "blue"
a["t_2_3"] = "green"
a.writefile("2.pdf")
a.attrpop()

# Page 3
a.attrpush()
a["no"] = "3"
a["area"] = "1881 Crossed Knives, Poor local paper"
a["template"] = "XXX-XXX"
a["l_1_1"] = "no perf. 1A"
a["l_1_2"] = "2A"
a["l_1_3"] = "4A"
a["t_1_1"] = "gray"
a["t_1_2"] = "red"
a["t_1_3"] = "green"
a["l_2_1"] = "pin perf. 1A"
a["l_2_2"] = "2A"
a["l_2_3"] = "4A"
a["t_2_1"] = "gray"
a["t_2_2"] = "violet"
a["t_2_3"] = "green"
a.writefile("3.pdf")
a.attrpop()

# Page 4
a.attrpush()
a["no"] = "4"
a["area"] = "Crossed Knives, Dark center, 1917"
a["template"] = "XXX"
a["l_1_1"] = "1A"
a["l_1_2"] = "2A"
a["l_1_3"] = "4A"
a["t_1_1"] = "blue"
a["t_1_2"] = "red"
a["t_1_3"] = "green"
a.writefile("4.pdf")
a.attrpop()

# Page 5
a["year"] = "1899"
a.attrpush()
a["area"] = "1899 Two Knives, Poor Local paper"
a["template"] = "XX-XX"
a["l_1_1"] = "pin perf. ½A"
a["l_1_2"] = "½A"
a["t_1_1"] = "gray"
a["t_1_2"] = "red"
a["l_2_1"] = "no perf. ½A"
a["l_2_2"] = "½A"
a["t_2_1"] = "gray"
a["t_2_2"] = "red"
a.writefile("5.pdf")
a.attrpop()

# Page 6
a["year"] = "1907"
a.attrpush()
a["area" ] = "Shiva, 5 characters below"
a["template"] = "dd-dd"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["l_2_1"] = "8 P"
a["l_2_2"] = "16 P"
a["t_2_1"] = "red"
a["t_2_2"] = "purple"
a.writefile("6.pdf")
a.attrpop()

# Page 7
a.attrpush()
a["no"] = "2"
a["area" ] = "Shiva, 9 characters below, 1930"
a["template"] = "ddd-ddd-ef"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_1_3"] = "8 P"
a["l_2_1"] = "16 P"
a["l_2_2"] = "24 P"
a["l_2_3"] = "32 P"
a["l_3_1"] = "1 R"
a["l_3_2"] = "5 R"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_1_3"] = "red"
a["t_2_1"] = "purple"
a["t_2_2"] = "orange"
a["t_2_3"] = "blue"
a["t_3_1"] = "orange"
a["t_3_2"] = "br/bl"
a.writefile("7.pdf")
a.attrpop()

# Page 8
a.attrpush()
a["no"] = "3"
a["area" ] = "Shiva, new year in bottom corners, 1935"
a["template"] = "ddd-ddd"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_1_3"] = "8 P"
a["l_2_1"] = "16 P"
a["l_2_2"] = "24 P"
a["l_2_3"] = "32 P"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_1_3"] = "red"
a["t_2_1"] = "purple"
a["t_2_2"] = "orange"
a["t_2_3"] = "blue"
a.writefile("8.pdf")
a.attrpop()

# Page 9
a.attrpush()
a["no"] = "4"
a["area" ] = "Shiva, Local print, 1941"
a["template"] = "ddd-ddd-e"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_1_3"] = "8 P"
a["l_2_1"] = "16 P"
a["l_2_2"] = "24 P"
a["l_2_3"] = "32 P"
a["l_3_1"] = "1 R"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_1_3"] = "red"
a["t_2_1"] = "purple"
a["t_2_2"] = "orange"
a["t_2_3"] = "blue"
a["t_3_1"] = "orange"
a.writefile("9.pdf")
a.attrpop()

# Page 10
a["year"] = "1949"
a.attrpush()
a["area" ] = "1949"
a["template"] = "AAAA-eEe-ef"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_1_3"] = "6 P"
a["l_1_4"] = "8 P"
a["l_2_1"] = "20 P"
a["l_2_2"] = "16 P"
a["l_2_3"] = "24 P"
a["l_3_1"] = "32 P"
a["l_3_2"] = "1 R"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_1_3"] = "red"
a["t_1_4"] = "orange"
a["t_2_1"] = "blue"
a["t_2_2"] = "lila"
a["t_2_3"] = "red"
a["t_3_1"] = "blue"
a["t_3_2"] = "orange"
a.writefile("10.pdf")
a.attrpop()

# Page 11
a["year"] = "1954"
a.attrpush()
a["area" ] = "1954"
a["template"] = "AA-AAA-EEEE-EEE"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_2_1"] = "6 P"
a["l_2_2"] = "8 P"
a["l_2_3"] = "12 P"
a["l_3_1"] = "16 P"
a["l_3_2"] = "20 P"
a["l_3_3"] = "24 P"
a["l_3_4"] = "32 P"
a["l_4_1"] = "50 P"
a["l_4_2"] = "1 R"
a["l_4_3"] = "2 R"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_2_1"] = "red"
a["t_2_2"] = "lila"
a["t_2_3"] = "orange"
a["t_3_1"] = "brown"
a["t_3_2"] = "red"
a["t_3_3"] = "brown"
a["t_3_4"] = "blue"
a["t_4_1"] = "red"
a["t_4_2"] = "red"
a["t_4_3"] = "orange"
a.writefile("11.pdf")
a.attrpop()

# Page 12
a["year"] = "1954B"
a.attrpush()
a["area" ] = "1954"
a["template"] = "ee-eee-gggg-ggg"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_2_1"] = "6 P"
a["l_2_2"] = "8 P"
a["l_2_3"] = "12 P"
a["l_3_1"] = "16 P"
a["l_3_2"] = "20 P"
a["l_3_3"] = "24 P"
a["l_3_4"] = "32 P"
a["l_4_1"] = "50 P"
a["l_4_2"] = "1 R"
a["l_4_3"] = "2 R"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_2_1"] = "red"
a["t_2_2"] = "lila"
a["t_2_3"] = "orange"
a["t_3_1"] = "brown"
a["t_3_2"] = "red"
a["t_3_3"] = "brown"
a["t_3_4"] = "blue"
a["t_4_1"] = "red"
a["t_4_2"] = "red"
a["t_4_3"] = "orange"
a.writefile("12.pdf")
a.attrpop()

# Page 13
a["year"] = "1956-"
a.attrpush()
a["template"] = "AFA-DD-H"
a.writefile("13.pdf")
a.attrpop()

# Page 14
a["year"] = "1957"
a.attrpush()
a["template"] = "AAAAA-EEE-EEEE"
a["l_1_1"] = "2 P"
a["l_1_2"] = "4 P"
a["l_1_3"] = "6 P"
a["l_1_4"] = "8 P"
a["l_1_5"] = "12 P"
a["l_2_1"] = "16 P"
a["l_2_2"] = "20 P"
a["l_2_3"] = "24 P"
a["l_3_1"] = "32 P"
a["l_3_2"] = "50 P"
a["l_3_3"] = "1 R"
a["l_3_4"] = "2 R"
a["t_1_1"] = "brown"
a["t_1_2"] = "green"
a["t_1_3"] = "red"
a["t_1_4"] = "lila"
a["t_1_5"] = "orange"
a["t_2_1"] = "brown"
a["t_2_2"] = "red"
a["t_2_3"] = "lila"
a["t_3_1"] = "blue"
a["t_3_2"] = "red"
a["t_3_3"] = "red"
a["t_3_4"] = "orange"
a.writefile("14.pdf")
a.attrpop()

# Page 15
a["year"] = "1958-"
a.attrpush()
a["template"] = "F-aga-A"
a.writefile("15.pdf")
a.attrpop()

# Page 16
a["year"] = "1959"
a.attrpush()
a["area"] = "1959"
a["template"] = "AaA-aAa-EEEE-EEEE"
a["l_1_1"] = "1 P"
a["l_1_2"] = "2 P"
a["l_1_3"] = "4 P"
a["l_2_1"] = "8 P"
a["l_2_2"] = "6 P"
a["l_2_3"] = "12 P"
a["l_3_1"] = "16 P"
a["l_3_2"] = "20 P"
a["l_3_3"] = "24 P"
a["l_3_4"] = "32 P"
a["l_4_1"] = "50 P"
a["l_4_2"] = "1 R"
a["l_4_3"] = "2 R"
a["l_4_4"] = "5 R"
a.writefile("16.pdf")
a.attrpop()

# Page 17
a["year"] = "1959-"
a.attrpush()
a["template"] = "i-ACE-EB-DDD"
a.writefile("17.pdf")
a.attrpop()

# Page 18
a["year"] = "1961-"
a.attrpush()
a["template"] = "GG-GGGG-GG"
a.writefile("18.pdf")
a.attrpop()

# Page 19
a["year"] = "1962-"
a.attrpush()
a["template"] = "GG-GG-GGG"
a.writefile("19.pdf")
a.attrpop()

# Page 20
a["year"] = "1962"
a.attrpush()
a["area"] = "1962"
a["template"] = "AAA-III-JJ"
a["l_1_1"] = "1 P"
a["l_1_2"] = "2 P"
a["l_1_3"] = "5 P"
a["l_2_1"] = "10 P"
a["l_2_2"] = "40 P"
a["l_2_3"] = "75 P"
a["l_3_1"] = "2 R"
a["l_3_2"] = "5 R"
a.writefile("20.pdf")
a.attrpop()


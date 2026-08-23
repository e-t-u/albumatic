/**
 * Albumatic Interactive Visual Designer & Layout Generator
 * Multi-Page Album, Batch Notation, and Full Unicode Support
 */

// Application Album State
const albumState = {
  country: "USA",
  area: "Definitives",
  year: "2009",
  logotext: "Albumatic",
  unit: "mm",
  pagewidth: 210,
  pageheight: 297,
  topmargin: 12,
  bottommargin: 18,
  leftmargin: 15,
  rightmargin: 15,
  header1pos: 25,
  header2pos: 35,
  maxxdistance: 15,
  maxydistance: 25,
  pages: [
    {
      country: "USA",
      area: "Definitives",
      year: "2009",
      no: "1",
      template: "ABBA-hh-BBB",
      logotext: "Albumatic",
      rightfooter: null,
      unit: "mm",
      pagewidth: 210,
      pageheight: 297,
      topmargin: 12,
      bottommargin: 18,
      leftmargin: 15,
      rightmargin: 15,
      header1pos: 25,
      header2pos: 35,
      maxxdistance: 15,
      maxydistance: 25,
      placeholders: "none",
      texts: {},
      labels: {},
      custom_sizes: {}
    }
  ]
};

let currentPageIndex = 0;
let standardSizes = {};
let zoomLevel = 1.0;

function getCurrentPage() {
  if (!albumState.pages[currentPageIndex]) {
    currentPageIndex = 0;
  }
  return albumState.pages[currentPageIndex];
}

// Preset Albums
const PRESETS = {
  "default": [
    {
      country: "USA",
      area: "Definitives",
      year: "2009",
      no: "1",
      template: "ABBA-hh-BBB",
      texts: {},
      labels: {}
    }
  ],
  "finland_album": [
    {
      country: "Suomi — Finland",
      area: "1856 Soikiomalli — First Oval Issue (Portostämpel)",
      year: "1856",
      no: "1",
      template: "BB-BB",
      texts: { "1_1": "5 kop. sininen", "1_2": "10 kop. punainen", "2_1": "5 kop. (pienihelminen)", "2_2": "10 kop. (isohelminen)" },
      labels: { "1_1": "Pystyurapaperi (Wove)", "1_2": "Pystyurapaperi", "2_1": "Vaakasuora urapaperi", "2_2": "Valkoinen paperi" }
    },
    {
      country: "Suomi — Finland",
      area: "1860 Vaakunamalli — Serpentine Roulette I",
      year: "1860",
      no: "2",
      template: "BB-BB",
      texts: { "1_1": "5 kop. sininen", "1_2": "10 kop. ruusunpunainen", "2_1": "5 kop. tummansininen", "2_2": "10 kop. karmiini" },
      labels: { "1_1": "Hammaste I (Isoposkinen)", "1_2": "Hammaste I", "2_1": "Paperi uurteeton", "2_2": "Ohut paperi" }
    },
    {
      country: "Suomi — Finland",
      area: "1866 Vaakunamalli — Penni- ja markka-arvot (Hammaste II)",
      year: "1866",
      no: "3",
      template: "BBB-BB",
      texts: { "1_1": "5 p. ruskea", "1_2": "10 p. musta", "1_3": "20 p. sininen", "2_1": "40 p. ruusunpunainen", "2_2": "1 mk ruskea" },
      labels: { "1_1": "Serpentine Roulette II", "1_2": "Vaalea lila paperi", "1_3": "Sininen paperi", "2_1": "Ruusu paperi", "2_2": "Keltanahkanen paperi" }
    },
    {
      country: "Suomi — Finland",
      area: "1875–1882 Helsingin painos — Vaakunakuviot",
      year: "1875",
      no: "4",
      template: "AAAA-AAA",
      texts: { "1_1": "2 p. harmaa", "1_2": "5 p. oranssi", "1_3": "8 p. vihreä", "1_4": "10 p. ruskea", "2_1": "20 p. sininen", "2_2": "32 p. karmiini", "2_3": "1 mk violetti" },
      labels: { "1_1": "Hammaste 11", "1_2": "Hammaste 11", "1_3": "Hammaste 12½", "1_4": "Hammaste 12½", "2_1": "Hammaste 12½", "2_2": "Hammaste 12½", "2_3": "Hammaste 14" }
    },
    {
      country: "Suomi — Finland",
      area: "1885 Vaakunamalli — Yksiväriset penniarvot",
      year: "1885",
      no: "5",
      template: "AAA-AAA",
      texts: { "1_1": "2 p. harmaa", "1_2": "5 p. vihreä", "1_3": "10 p. ruusu", "2_1": "20 p. oranssi", "2_2": "25 p. sininen", "2_3": "50 p. ruskea" },
      labels: { "1_1": "Hammaste 12½", "1_2": "Hammaste 12½", "1_3": "Helsinki / Helsingfors", "2_1": "Tampere / Tammerfors", "2_2": "Turku / Åbo", "2_3": "Viipuri / Wiborg" }
    },
    {
      country: "Suomi — Finland",
      area: "1885 Vaakunamalli — Kaksiväriset markka-arvot",
      year: "1885",
      no: "6",
      template: "BBB",
      texts: { "1_1": "1 mk harmaa & ruusu", "1_2": "5 mk vihreä & ruusu", "1_3": "10 mk ruskea & ruusu" },
      labels: { "1_1": "1 Markka (Hammaste 12½)", "1_2": "5 Markkaa (Hämeenlinna)", "1_3": "10 Markkaa (Kuopio)" }
    },
    {
      country: "Suomi — Finland",
      area: "1889 Vaakunamalli — Penniarvot (Uusi kaiverrus)",
      year: "1889",
      no: "7",
      template: "AAA-AAA",
      texts: { "1_1": "2 p. harmaa", "1_2": "5 p. vihreä", "1_3": "10 p. punainen", "2_1": "20 p. keltainen", "2_2": "25 p. sininen", "2_3": "50 p. ruskea" },
      labels: { "1_1": "Hammaste 12½", "1_2": "Hammaste 12½", "1_3": "Östermyra & Ähtäri", "2_1": "Vaasa / Wasa", "2_2": "Oulu / Uleåborg", "2_3": "Pori / Björneborg" }
    },
    {
      country: "Suomi — Finland",
      area: "1889 Vaakunamalli — Markka-arvot & Åland",
      year: "1889",
      no: "8",
      template: "BBB",
      texts: { "1_1": "1 mk harmaa", "1_2": "5 mk vihreä", "1_3": "10 mk ruskea" },
      labels: { "1_1": "1 Markka (Helsingfors)", "1_2": "5 Markkaa (Åland — Mariehamn)", "1_3": "10 Markkaa (Saimaan höyrylaiva)" }
    }
  ],
  "china_demo": [
    {
      country: "中国 — China",
      area: "大清邮政 — Large Dragon & Coiling Dragon (1878-1898)",
      year: "1878",
      no: "1",
      template: "XXX-XXX",
      custom_sizes: { "X": [35.0, 35.0] },
      texts: { "1_1": "壹分银 (1 Candarin)", "1_2": "叁分银 (3 Candarins)", "1_3": "伍分银 (5 Candarins)", "2_1": "壹角 (10 Cents)", "2_2": "贰角 (20 Cents)", "2_3": "伍角 (50 Cents)" },
      labels: { "1_1": "海关薄纸", "1_2": "阔边大龙", "1_3": "厚纸光芒", "2_1": "蟠龙加盖", "2_2": "红印花加贴", "2_3": "伦敦版" }
    }
  ],
  "nepal_album": [
    { country: "Nepal", year: "1881", no: "1", area: "1881 Crossed Knives, European paper", template: "XXX-X-XXX-X", texts: {"1_1":"blue","1_2":"lila","1_3":"green","2_1":"blue","3_1":"blue","3_2":"lila","3_3":"green","4_1":"blue"}, labels: {"1_1":"pin perf. 1A","1_2":"2A","1_3":"4A","2_1":"Recut 1899 1A","3_1":"no perf. 1A","3_2":"2A","3_3":"4A","4_1":"Recut 1899 1A"} },
    { country: "Nepal", year: "1881", no: "2", area: "1881 Crossed Knives, Good Local paper", template: "XXX-XXX", texts: {"1_1":"blue","1_2":"blue","1_3":"green","2_1":"blue","2_2":"blue","2_3":"green"}, labels: {"1_1":"thin 1A","1_2":"2A","1_3":"4A","2_1":"thick 1A","2_2":"2A","2_3":"4A"} },
    { country: "Nepal", year: "1881", no: "3", area: "1881 Crossed Knives, Poor local paper", template: "XXX-XXX", texts: {"1_1":"gray","1_2":"red","1_3":"green","2_1":"gray","2_2":"violet","2_3":"green"}, labels: {"1_1":"no perf. 1A","1_2":"2A","1_3":"4A","2_1":"pin perf. 1A","2_2":"2A","2_3":"4A"} },
    { country: "Nepal", year: "1881", no: "4", area: "Crossed Knives, Dark center, 1917", template: "XXX", texts: {"1_1":"blue","1_2":"red","1_3":"green"}, labels: {"1_1":"1A","1_2":"2A","1_3":"4A"} },
    { country: "Nepal", year: "1899", no: "1", area: "1899 Two Knives, Poor Local paper", template: "XX-XX", texts: {"1_1":"gray","1_2":"red","2_1":"gray","2_2":"red"}, labels: {"1_1":"pin perf. ½A","1_2":"½A","2_1":"no perf. ½A","2_2":"½A"} },
    { country: "Nepal", year: "1907", no: "1", area: "Shiva, 5 characters below", template: "dd-dd", texts: {"1_1":"brown","1_2":"green","2_1":"red","2_2":"purple"}, labels: {"1_1":"2 P","1_2":"4 P","2_1":"8 P","2_2":"16 P"} },
    { country: "Nepal", year: "1907", no: "2", area: "Shiva, 9 characters below, 1930", template: "ddd-ddd-ef", texts: {"1_1":"brown","1_2":"green","1_3":"red","2_1":"purple","2_2":"orange","2_3":"blue","3_1":"orange","3_2":"br/bl"}, labels: {"1_1":"2 P","1_2":"4 P","1_3":"8 P","2_1":"16 P","2_2":"24 P","2_3":"32 P","3_1":"1 R","3_2":"5 R"} },
    { country: "Nepal", year: "1907", no: "3", area: "Shiva, new year in bottom corners, 1935", template: "ddd-ddd", texts: {"1_1":"brown","1_2":"green","1_3":"red","2_1":"purple","2_2":"orange","2_3":"blue"}, labels: {"1_1":"2 P","1_2":"4 P","1_3":"8 P","2_1":"16 P","2_2":"24 P","2_3":"32 P"} },
    { country: "Nepal", year: "1907", no: "4", area: "Shiva, Local print, 1941", template: "ddd-ddd-e", texts: {"1_1":"brown","1_2":"green","1_3":"red","2_1":"purple","2_2":"orange","2_3":"blue","3_1":"orange"}, labels: {"1_1":"2 P","1_2":"4 P","1_3":"8 P","2_1":"16 P","2_2":"24 P","2_3":"32 P","3_1":"1 R"} },
    { country: "Nepal", year: "1949", no: "1", area: "1949 Definitive Issue", template: "AAAA-eEe-ef", texts: {"1_1":"brown","1_2":"green","1_3":"red","1_4":"orange","2_1":"blue","2_2":"lila","2_3":"red","3_1":"blue","3_2":"orange"}, labels: {"1_1":"2 P","1_2":"4 P","1_3":"6 P","1_4":"8 P","2_1":"20 P","2_2":"16 P","2_3":"24 P","3_1":"32 P","3_2":"1 R"} },
    { country: "Nepal", year: "1954", no: "1", area: "1954 Map and Stupa", template: "AA-AAA-EEEE-EEE", texts: {}, labels: {} },
    { country: "Nepal", year: "1954", no: "2", area: "1954B Landscape Set", template: "ee-eee-gggg-ggg", texts: {}, labels: {} },
    { country: "Nepal", year: "1957", no: "1", area: "1957 King Mahendra", template: "AAAAA-EEE-EEEE", texts: {}, labels: {} },
    { country: "Nepal", year: "1959", no: "1", area: "1959 First Parliament", template: "AaA-aAa-EEEE-EEEE", texts: {}, labels: {} },
    { country: "Nepal", year: "1962", no: "1", area: "1962 Airmail and Commemoratives", template: "AAA-III-JJ", texts: {}, labels: {} }
  ],
  "unicode_demo": [
    {
      country: "Suomi — Finland (Åland & Häme)",
      area: "1889 Vaakunamalli — Vapensköld & Cliché brût (½ Mk)",
      year: "1889",
      no: "1",
      template: "AA-BB-CC",
      texts: {
        "1_1": "5 penniä (vihreä)",
        "1_2": "10 penniä (punainen)",
        "2_1": "20 penniä (oranssi)",
        "2_2": "1 markka (harmaa)",
        "3_1": "5 markkaa (vihreä)",
        "3_2": "10 markkaa (ruskea)"
      },
      labels: {
        "1_1": "Helsinki / Helsingfors (Åbo)",
        "1_2": "Tampere / Tammerfors (Örebro-cliché)",
        "2_1": "Viipuri / Wiborg (Hämeenlinna)",
        "2_2": "Ahvenanmaa — Åland (Mariehamn)",
        "3_1": "Östermyra & Ähtäri erikoispainos",
        "3_2": "Pohjois-Inkeri & Saimaan höyrylaiva"
      }
    },
    {
      country: "Россия — CCCP",
      area: "Стандартный выпуск (1923)",
      year: "1923",
      no: "2",
      template: "BBB-CCC",
      texts: { "1_1": "1 коп.", "1_2": "2 коп.", "1_3": "5 коп." },
      labels: { "1_1": "Москва", "1_2": "Петроград", "1_3": "Киев" }
    },
    {
      country: "Ελλάς — Greece",
      area: "Ερμής (Hermes Heads)",
      year: "1861",
      no: "3",
      template: "AAA-AAA",
      texts: { "1_1": "1 λεπτόν", "1_2": "2 λεπτά", "1_3": "5 λεπτά" },
      labels: { "1_1": "Αθήναι", "1_2": "Πειραιεύς", "1_3": "Πάτραι" }
    },
    {
      country: "中国 — China",
      area: "大清邮政 — Large Dragon & Coiling Dragon (1878-1898)",
      year: "1878",
      no: "4",
      template: "XXX-XXX",
      custom_sizes: { "X": [35.0, 35.0] },
      texts: { "1_1": "壹分银 (1 Candarin)", "1_2": "叁分银 (3 Candarins)", "1_3": "伍分银 (5 Candarins)", "2_1": "壹角 (10 Cents)", "2_2": "贰角 (20 Cents)", "2_3": "伍角 (50 Cents)" },
      labels: { "1_1": "海关薄纸", "1_2": "阔边大龙", "1_3": "厚纸光芒", "2_1": "蟠龙加盖", "2_2": "红印花加贴", "2_3": "伦敦版" }
    },
    {
      country: "مصر — Egypt",
      area: "البريد المصري — Egyptian Postal Issue (1866)",
      year: "1866",
      no: "5",
      template: "BBB-CCC",
      texts: { "1_1": "١٠ بارات", "1_2": "٢٠ بارة", "1_3": "١ قرش", "2_1": "٢ قرشان", "2_2": "٥ قروش" },
      labels: { "1_1": "القاهرة", "1_2": "الإسكندرية", "1_3": "بورسعيد", "2_1": "السويس", "2_2": "طنطا" }
    }
  ]
};

// Batch Sample Templates
const BATCH_SAMPLES = {
  "finland_batch": [
    "1856 | 1 | 1856 Soikiomalli — First Oval Issue (Portostämpel) | BB-BB | t:1_1=5 kop. sininen,1_2=10 kop. punainen,2_1=5 kop. (pienihelminen),2_2=10 kop. (isohelminen) | l:1_1=Pystyurapaperi (Wove),1_2=Pystyurapaperi,2_1=Vaakasuora urapaperi,2_2=Valkoinen paperi",
    "1860 | 2 | 1860 Vaakunamalli — Serpentine Roulette I | BB-BB | t:1_1=5 kop. sininen,1_2=10 kop. ruusunpunainen,2_1=5 kop. tummansininen,2_2=10 kop. karmiini | l:1_1=Hammaste I (Isoposkinen),1_2=Hammaste I,2_1=Paperi uurteeton,2_2=Ohut paperi",
    "1866 | 3 | 1866 Vaakunamalli — Penni- ja markka-arvot (Hammaste II) | BBB-BB | t:1_1=5 p. ruskea,1_2=10 p. musta,1_3=20 p. sininen,2_1=40 p. ruusunpunainen,2_2=1 mk ruskea | l:1_1=Serpentine Roulette II,1_2=Vaalea lila paperi,1_3=Sininen paperi,2_1=Ruusu paperi,2_2=Keltanahkanen paperi",
    "1875 | 4 | 1875–1882 Helsingin painos — Vaakunakuviot | AAAA-AAA | t:1_1=2 p. harmaa,1_2=5 p. oranssi,1_3=8 p. vihreä,1_4=10 p. ruskea,2_1=20 p. sininen,2_2=32 p. karmiini,2_3=1 mk violetti | l:1_1=Hammaste 11,1_2=Hammaste 11,1_3=Hammaste 12½,1_4=Hammaste 12½,2_1=Hammaste 12½,2_2=Hammaste 12½,2_3=Hammaste 14",
    "1885 | 5 | 1885 Vaakunamalli — Yksiväriset penniarvot | AAA-AAA | t:1_1=2 p. harmaa,1_2=5 p. vihreä,1_3=10 p. ruusu,2_1=20 p. oranssi,2_2=25 p. sininen,2_3=50 p. ruskea | l:1_1=Hammaste 12½,1_2=Hammaste 12½,1_3=Helsinki / Helsingfors,2_1=Tampere / Tammerfors,2_2=Turku / Åbo,2_3=Viipuri / Wiborg",
    "1885 | 6 | 1885 Vaakunamalli — Kaksiväriset markka-arvot | BBB | t:1_1=1 mk harmaa & ruusu,1_2=5 mk vihreä & ruusu,1_3=10 mk ruskea & ruusu | l:1_1=1 Markka (Hammaste 12½),1_2=5 Markkaa (Hämeenlinna),1_3=10 Markkaa (Kuopio)",
    "1889 | 7 | 1889 Vaakunamalli — Penniarvot (Uusi kaiverrus) | AAA-AAA | t:1_1=2 p. harmaa,1_2=5 p. vihreä,1_3=10 p. punainen,2_1=20 p. keltainen,2_2=25 p. sininen,2_3=50 p. ruskea | l:1_1=Hammaste 12½,1_2=Hammaste 12½,1_3=Östermyra & Ähtäri,2_1=Vaasa / Wasa,2_2=Oulu / Uleåborg,2_3=Pori / Björneborg",
    "1889 | 8 | 1889 Vaakunamalli — Markka-arvot & Åland | BBB | t:1_1=1 mk harmaa,1_2=5 mk vihreä,1_3=10 mk ruskea | l:1_1=1 Markka (Helsingfors),1_2=5 Markkaa (Åland — Mariehamn),1_3=10 Markkaa (Saimaan höyrylaiva)"
  ].join("\n"),

  "china_batch": "1878 | 1 | 大清邮政 — Large Dragon (1878) | XXX-XXX | t:1_1=壹分银 (1 Candarin),1_2=叁分银,1_3=伍分银,2_1=壹角,2_2=贰角,2_3=伍角 | l:1_1=海关薄纸,1_2=阔边大龙,1_3=厚纸光芒,2_1=蟠龙加盖,2_2=红印花,2_3=伦敦版 | s:X=35,35",

  "30_catalog": [
    "AA-BB-CC", "cc-ddd-a", "XXXX-XXXX", "AAAA-BBBB", "ee-fff-gg",
    "ABCDEFG", "HIJKLM", "NOPQR", "STUV", "WXYZ",
    "abcde", "fghi", "jklm", "nopq", "rst-uv",
    "ABBA-hh-BBB", "AAA-BBB-CCC", "ddd-eee-fff", "GGGG-HHHH", "II-JJ-KK",
    "LL-MM-NN", "OO-PP-QQ", "RR-SS-TT", "UU-VV-WW", "XX-YY-ZZ",
    "aa-bb-cc", "dd-ee-ff", "gg-hh-ii", "jj-kk-ll", "mm-nn-oo"
  ].join("\n"),

  "nepal_batch": [
    "1881 | 1 | 1881 Crossed Knives, European paper | XXX-X-XXX-X | t:1_1=blue,1_2=lila,1_3=green,2_1=blue,3_1=blue,3_2=lila,3_3=green,4_1=blue | l:1_1=pin perf. 1A,1_2=2A,1_3=4A,2_1=Recut 1899 1A,3_1=no perf. 1A,3_2=2A,3_3=4A,4_1=Recut 1899 1A",
    "1881 | 2 | 1881 Crossed Knives, Good Local paper | XXX-XXX | t:1_1=blue,1_2=blue,1_3=green,2_1=blue,2_2=blue,2_3=green | l:1_1=thin 1A,1_2=2A,1_3=4A,2_1=thick 1A,2_2=2A,2_3=4A",
    "1881 | 3 | 1881 Crossed Knives, Poor local paper | XXX-XXX | t:1_1=gray,1_2=red,1_3=green,2_1=gray,2_2=violet,2_3=green | l:1_1=no perf. 1A,1_2=2A,1_3=4A,2_1=pin perf. 1A,2_2=2A,2_3=4A",
    "1881 | 4 | Crossed Knives, Dark center, 1917 | XXX | t:1_1=blue,1_2=red,1_3=green | l:1_1=1A,1_2=2A,1_3=4A",
    "1899 | 1 | 1899 Two Knives, Poor Local paper | XX-XX | t:1_1=gray,1_2=red,2_1=gray,2_2=red | l:1_1=pin perf. ½A,1_2=½A,2_1=no perf. ½A,2_2=½A",
    "1907 | 1 | Shiva, 5 characters below | dd-dd | t:1_1=brown,1_2=green,2_1=red,2_2=purple | l:1_1=2 P,1_2=4 P,2_1=8 P,2_2=16 P",
    "1907 | 2 | Shiva, 9 characters below, 1930 | ddd-ddd-ef | t:1_1=brown,1_2=green,1_3=red,2_1=purple,2_2=orange,2_3=blue,3_1=orange,3_2=br/bl | l:1_1=2 P,1_2=4 P,1_3=8 P,2_1=16 P,2_2=24 P,2_3=32 P,3_1=1 R,3_2=5 R",
    "1907 | 3 | Shiva, new year in bottom corners, 1935 | ddd-ddd | t:1_1=brown,1_2=green,1_3=red,2_1=purple,2_2=orange,2_3=blue | l:1_1=2 P,1_2=4 P,1_3=8 P,2_1=16 P,2_2=24 P,2_3=32 P",
    "1907 | 4 | Shiva, Local print, 1941 | ddd-ddd-e | t:1_1=brown,1_2=green,1_3=red,2_1=purple,2_2=orange,2_3=blue,3_1=orange | l:1_1=2 P,1_2=4 P,1_3=8 P,2_1=16 P,2_2=24 P,2_3=32 P,3_1=1 R",
    "1949 | 1 | 1949 Definitive Issue | AAAA-eEe-ef | t:1_1=brown,1_2=green,1_3=red,1_4=orange,2_1=blue,2_2=lila,2_3=red,3_1=blue,3_2=orange | l:1_1=2 P,1_2=4 P,1_3=6 P,1_4=8 P,2_1=20 P,2_2=16 P,2_3=24 P,3_1=32 P,3_2=1 R",
    "1954 | 1 | 1954 Map and Stupa | AA-AAA-EEEE-EEE",
    "1954 | 2 | 1954B Landscape Set | ee-eee-gggg-ggg",
    "1957 | 1 | 1957 King Mahendra | AAAAA-EEE-EEEE",
    "1959 | 1 | 1959 First Parliament | AaA-aAa-EEEE-EEEE",
    "1962 | 1 | 1962 Airmail and Commemoratives | AAA-III-JJ"
  ].join("\n"),

  "unicode_batch": [
    "1889 | 1 | 1889 Vaakunamalli — Vapensköld & Cliché brût (½ Mk) | AA-BB-CC | t:1_1=5 penniä (vihreä),1_2=10 penniä,2_1=20 penniä,2_2=1 markka,3_1=5 markkaa,3_2=10 markkaa | l:1_1=Helsinki (Åbo),1_2=Tampere (Örebro-cliché),2_1=Hämeenlinna,2_2=Åland (Mariehamn),3_1=Östermyra & Ähtäri,3_2=Saimaan höyrylaiva",
    "1923 | 2 | Стандартный выпуск (1923) | BBB-CCC | t:1_1=1 коп.,1_2=2 коп.,1_3=5 коп. | l:1_1=Москва,1_2=Петроград,1_3=Киев",
    "1861 | 3 | Ερμής (Hermes Heads) | AAA-AAA | t:1_1=1 λεπτόν,1_2=2 λεπτά,1_3=5 λεπτά | l:1_1=Αθήναι,1_2=Πειραιεύς,1_3=Πάτραι",
    "1878 | 4 | 大清邮政 — Large Dragon (1878) | XXX-XXX | t:1_1=壹分银 (1 Candarin),1_2=叁分银,1_3=伍分银,2_1=壹角,2_2=贰角,2_3=伍角 | l:1_1=海关薄纸,1_2=阔边大龙,1_3=厚纸光芒,2_1=蟠龙加盖,2_2=红印花,2_3=伦敦版 | s:X=35,35",
    "1866 | 5 | البريد المصري — Postal Issue (1866) | BBB-CCC | t:1_1=١٠ بارات,1_2=٢٠ بارة,1_3=١ قرش,2_1=٢ قرشان,2_2=٥ قروش | l:1_1=القاهرة,1_2=الإسكندرية,1_3=بورسعيد,2_1=السويس,2_2=طنطا"
  ].join("\n")
};

const PAPER_PROFILES = {
  "A4": { pagewidth: 210, pageheight: 297, unit: "mm", topmargin: 12, bottommargin: 18, leftmargin: 15, rightmargin: 15, header1pos: 25, header2pos: 35, maxxdistance: 15, maxydistance: 25 },
  "Letter_in": { pagewidth: 8.5, pageheight: 11.0, unit: "in", topmargin: 0.5, bottommargin: 0.75, leftmargin: 0.6, rightmargin: 0.6, header1pos: 1.0, header2pos: 1.4, maxxdistance: 0.6, maxydistance: 1.0 },
  "Letter_mm": { pagewidth: 215.9, pageheight: 279.4, unit: "mm", topmargin: 12, bottommargin: 18, leftmargin: 15, rightmargin: 15, header1pos: 25, header2pos: 35, maxxdistance: 15, maxydistance: 25 },
  "A3": { pagewidth: 297, pageheight: 420, unit: "mm", topmargin: 15, bottommargin: 22, leftmargin: 20, rightmargin: 20, header1pos: 30, header2pos: 45, maxxdistance: 20, maxydistance: 30 }
};

const TO_MM = { "mm": 1.0, "in": 25.4, "pt": 25.4 / 72.0, "pica": 25.4 / 6.0 };

// Initialize
document.addEventListener("DOMContentLoaded", async () => {
  await fetchSizes();
  setupEventListeners();
  renderFilmstrip();
  syncUIFromCurrentPage();
  renderCatalogModal();
  await updatePreview();
  setTimeout(fitToScreen, 60);
});

async function fetchSizes() {
  try {
    const res = await fetch("/api/v1/sizes");
    standardSizes = await res.json();
  } catch (err) {
    console.error("Failed to load sizes:", err);
  }
}

const BUILTIN_STAMP_SIZES = {
  "A": [20.0, 24.0], "B": [20.0, 26.0], "C": [21.0, 24.0], "D": [21.5, 26.0], "E": [21.5, 30.0],
  "F": [23.0, 27.5], "G": [24.0, 29.0], "H": [24.0, 40.0], "I": [24.0, 41.0], "J": [25.0, 30.0],
  "K": [25.0, 36.0], "L": [26.0, 31.0], "M": [26.0, 36.0], "N": [26.0, 40.0], "O": [26.0, 41.0],
  "P": [26.0, 43.0], "Q": [27.5, 33.0], "R": [28.0, 34.0], "S": [28.0, 39.0], "T": [29.0, 36.0],
  "U": [30.0, 39.0], "V": [30.0, 41.0], "W": [33.0, 55.0], "X": [35.0, 35.0], "Y": [41.0, 41.0],
  "Z": [41.0, 53.0],
  "a": [24.0, 21.0], "b": [26.0, 21.5], "c": [29.0, 24.0], "d": [31.0, 24.0], "e": [31.0, 26.0],
  "f": [33.0, 27.5], "g": [34.0, 28.0], "h": [36.0, 25.0], "i": [36.0, 26.0], "j": [36.0, 29.0],
  "k": [39.0, 28.0], "l": [39.0, 30.0], "m": [40.0, 24.0], "n": [40.0, 26.0], "o": [40.0, 33.0],
  "p": [41.0, 24.0], "q": [41.0, 26.0], "r": [41.0, 30.0], "s": [43.0, 26.0], "t": [46.0, 27.5],
  "u": [53.0, 41.0], "v": [55.0, 33.0]
};

function getMountMetrics(code) {
  const p = getCurrentPage();
  if (p && p.custom_sizes && p.custom_sizes[code]) {
    const custom = p.custom_sizes[code];
    let w_mm = Array.isArray(custom) ? custom[0] : (custom.width || 25.0);
    let h_mm = Array.isArray(custom) ? custom[1] : (custom.height || 30.0);
    const w_in = Math.round((w_mm / 25.4) * 100) / 100;
    const h_in = Math.round((h_mm / 25.4) * 100) / 100;
    const orientation = w_mm >= h_mm ? "landscape" : "portrait";
    return { w_mm, h_mm, w_in, h_in, orientation, is_custom: true };
  }

  let s = standardSizes[code];
  let w_mm = 25.0, h_mm = 30.0;
  
  if (s) {
    w_mm = s.width_mm !== undefined ? s.width_mm : (s.width || (Array.isArray(s) ? s[0] : 25.0));
    h_mm = s.height_mm !== undefined ? s.height_mm : (s.height || (Array.isArray(s) ? s[1] : 30.0));
  } else if (BUILTIN_STAMP_SIZES[code]) {
    [w_mm, h_mm] = BUILTIN_STAMP_SIZES[code];
  }

  const w_in = (s && s.width_in !== undefined && s.width_in !== null) ? Number(s.width_in) : Math.round((w_mm / 25.4) * 100) / 100;
  const h_in = (s && s.height_in !== undefined && s.height_in !== null) ? Number(s.height_in) : Math.round((h_mm / 25.4) * 100) / 100;
  const orientation = (s && s.orientation) ? s.orientation : (code === code.toUpperCase() ? "portrait" : "landscape");

  return { w_mm, h_mm, w_in, h_in, orientation, is_custom: false };
}

function formatMountSizeShort(code) {
  const m = getMountMetrics(code);
  const p = getCurrentPage();
  if (p.unit === "in") {
    return `${m.w_in}×${m.h_in}" (${m.w_mm}×${m.h_mm}mm)${m.is_custom ? ' ⭐' : ''}`;
  }
  return `${m.w_mm}×${m.h_mm}mm${m.is_custom ? ' ⭐' : ''}`;
}

function setupEventListeners() {
  const pageFields = [
    "country", "area", "year", "no", "logotext", "rightfooter",
    "pagewidth", "pageheight", "topmargin", "bottommargin",
    "leftmargin", "rightmargin", "header1pos", "header2pos",
    "maxxdistance", "maxydistance", "placeholders"
  ];

  const ALBUM_GEOMETRY_FIELDS = [
    "unit", "pagewidth", "pageheight", "topmargin", "bottommargin",
    "leftmargin", "rightmargin", "header1pos", "header2pos",
    "maxxdistance", "maxydistance"
  ];

  pageFields.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener("input", (e) => {
      const p = getCurrentPage();
      const val = e.target.type === "number" ? (parseFloat(e.target.value) || 0) : e.target.value;
      if (id === "rightfooter") {
        p.rightfooter = e.target.value.trim() ? e.target.value : null;
      } else {
        p[id] = val;
      }

      // If it is an album-wide geometry setting, propagate to all pages!
      if (ALBUM_GEOMETRY_FIELDS.includes(id)) {
        albumState[id] = val;
        albumState.pages.forEach(page => {
          page[id] = val;
        });
      }

      renderFilmstrip();
      updatePreviewDebounced();
    });
  });

  // Custom size handlers
  const customCodeInput = document.getElementById("custom-size-code");
  const customWidthInput = document.getElementById("custom-size-width");
  const customHeightInput = document.getElementById("custom-size-height");

  if (customCodeInput) {
    customCodeInput.addEventListener("input", (e) => {
      const code = e.target.value.trim().toUpperCase();
      e.target.value = code;
      if (code) {
        const m = getMountMetrics(code);
        if (m && customWidthInput && customHeightInput) {
          const p = getCurrentPage();
          customWidthInput.value = p.unit === "in" ? m.w_in : m.w_mm;
          customHeightInput.value = p.unit === "in" ? m.h_in : m.h_mm;
        }
      }
    });
  }

  [customCodeInput, customWidthInput, customHeightInput].forEach(inp => {
    if (!inp) return;
    inp.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        addOrUpdateCustomSize();
      }
    });
  });

  document.getElementById("btn-save-custom-size")?.addEventListener("click", addOrUpdateCustomSize);

  // Unit converter selector (Album-wide)
  const unitSelect = document.getElementById("unit");
  if (unitSelect) {
    unitSelect.addEventListener("change", (e) => {
      const p = getCurrentPage();
      const oldUnit = p.unit || albumState.unit || "mm";
      const newUnit = e.target.value;
      if (oldUnit !== newUnit) {
        convertUnits(oldUnit, newUnit);
      }
    });
  }

  // Template string input direct sync
  const templateInput = document.getElementById("template-input");
  if (templateInput) {
    templateInput.addEventListener("input", (e) => {
      const p = getCurrentPage();
      p.template = e.target.value;
      renderRowBuilder();
      updatePreviewDebounced();
    });
  }

  // Presets dropdown
  const presetSelect = document.getElementById("preset-select");
  if (presetSelect) {
    presetSelect.addEventListener("change", (e) => {
      const pList = PRESETS[e.target.value];
      if (pList) {
        albumState.pages = JSON.parse(JSON.stringify(pList));
        currentPageIndex = 0;
        renderFilmstrip();
        syncUIFromCurrentPage();
        updatePreview();
        setTimeout(fitToScreen, 80);
      }
    });
  }

  // Paper preset selector (Album-wide)
  const paperPreset = document.getElementById("paper-preset");
  if (paperPreset) {
    paperPreset.addEventListener("change", (e) => {
      const profile = PAPER_PROFILES[e.target.value];
      if (profile) {
        Object.assign(albumState, profile);
        albumState.pages.forEach(page => {
          Object.assign(page, profile);
        });
        syncUIFromCurrentPage();
        updatePreview();
        setTimeout(fitToScreen, 80);
      }
    });
  }

  // Page Filmstrip Actions
  document.getElementById("btn-prev-page")?.addEventListener("click", () => goToPage(currentPageIndex - 1));
  document.getElementById("btn-next-page")?.addEventListener("click", () => goToPage(currentPageIndex + 1));
  document.getElementById("btn-add-page")?.addEventListener("click", addNewPage);
  document.getElementById("btn-duplicate-page")?.addEventListener("click", duplicateCurrentPage);
  document.getElementById("btn-delete-page")?.addEventListener("click", deleteCurrentPage);

  // Add Row Button
  document.getElementById("btn-add-row")?.addEventListener("click", () => {
    const p = getCurrentPage();
    const lines = p.template ? p.template.split("-") : [];
    lines.push("AAA");
    p.template = lines.join("-");
    syncTemplateInput();
    renderRowBuilder();
    updatePreview();
  });

  // Zoom Controls
  document.getElementById("btn-zoom-in")?.addEventListener("click", () => setZoom(zoomLevel + 0.15));
  document.getElementById("btn-zoom-out")?.addEventListener("click", () => setZoom(zoomLevel - 0.15));
  document.getElementById("btn-zoom-fit")?.addEventListener("click", fitToScreen);

  window.addEventListener("resize", () => {
    // If fit mode is active, adjust zoom
    if (document.getElementById("preview-paper")) {
      // Small debounce
      clearTimeout(window._resizeTimer);
      window._resizeTimer = setTimeout(fitToScreen, 150);
    }
  });

  // Mouse wheel zoom over preview
  const previewPane = document.querySelector(".preview-pane");
  if (previewPane) {
    previewPane.addEventListener("wheel", (e) => {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.1 : -0.1;
        setZoom(zoomLevel + delta);
      }
    }, { passive: false });
  }

  // Downloads
  document.getElementById("btn-download-pdf")?.addEventListener("click", () => {
    const p = getCurrentPage();
    downloadSinglePdf(p);
  });

  document.getElementById("btn-download-album-pdf")?.addEventListener("click", downloadFullAlbumPdf);
  document.getElementById("btn-download-svg")?.addEventListener("click", downloadSvg);

  // Batch Notation Modal
  document.getElementById("btn-batch-modal")?.addEventListener("click", showBatchModal);
  document.getElementById("btn-close-batch")?.addEventListener("click", hideBatchModal);
  document.getElementById("btn-apply-batch")?.addEventListener("click", applyBatchNotation);
  document.getElementById("btn-export-batch-text")?.addEventListener("click", exportBatchText);
  document.getElementById("batch-modal")?.addEventListener("click", (e) => {
    if (e.target.id === "batch-modal") hideBatchModal();
  });

  // Batch samples, copy, and file load
  document.getElementById("batch-sample-select")?.addEventListener("change", (e) => {
    const sampleKey = e.target.value;
    if (sampleKey && BATCH_SAMPLES[sampleKey]) {
      const ta = document.getElementById("batch-text-area");
      if (ta) {
        ta.value = BATCH_SAMPLES[sampleKey];
        updateBatchCount();
      }
    }
  });

  document.getElementById("batch-text-area")?.addEventListener("input", updateBatchCount);

  document.getElementById("btn-batch-copy")?.addEventListener("click", () => {
    const ta = document.getElementById("batch-text-area");
    if (ta && ta.value) {
      navigator.clipboard.writeText(ta.value);
      alert("Batch text copied to clipboard!");
    }
  });

  document.getElementById("btn-batch-download-txt")?.addEventListener("click", () => {
    const ta = document.getElementById("batch-text-area");
    if (ta && ta.value) {
      const blob = new Blob([ta.value], { type: "text/plain;charset=utf-8" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${albumState.country || "Album"}_BatchNotation.txt`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
  });

  document.getElementById("batch-file-input")?.addEventListener("change", (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (evt) => {
        const ta = document.getElementById("batch-text-area");
        if (ta && evt.target.result) {
          ta.value = evt.target.result;
          updateBatchCount();
        }
      };
      reader.readAsText(file);
    }
  });

  // Help Modal
  document.getElementById("btn-help")?.addEventListener("click", showHelpModal);
  document.getElementById("btn-close-help")?.addEventListener("click", hideHelpModal);
  document.getElementById("help-modal")?.addEventListener("click", (e) => {
    if (e.target.id === "help-modal") hideHelpModal();
  });

  // Share / Query Modal
  document.getElementById("btn-export-query")?.addEventListener("click", showExportModal);
  document.getElementById("btn-close-modal")?.addEventListener("click", hideExportModal);
  document.getElementById("export-modal")?.addEventListener("click", (e) => {
    if (e.target.id === "export-modal") hideExportModal();
  });

  // Catalog search
  document.getElementById("catalog-search")?.addEventListener("input", (e) => {
    filterCatalog(e.target.value);
  });
}

function renderFilmstrip() {
  const strip = document.getElementById("album-filmstrip");
  if (!strip) return;
  strip.innerHTML = "";

  albumState.pages.forEach((page, idx) => {
    const tab = document.createElement("div");
    tab.className = `page-tab ${idx === currentPageIndex ? 'active' : ''}`;
    const pageTitle = page.area ? `${page.year || ''} ${page.area}` : (page.country || `Page ${idx + 1}`);
    tab.innerHTML = `<span>#${page.no || (idx + 1)}</span> <small style="max-width:110px; overflow:hidden; text-overflow:ellipsis; display:inline-block; vertical-align:bottom;">${pageTitle}</small>`;
    tab.addEventListener("click", () => {
      currentPageIndex = idx;
      renderFilmstrip();
      syncUIFromCurrentPage();
      updatePreview();
    });
    strip.appendChild(tab);
  });

  const counter = document.getElementById("page-counter-label");
  if (counter) {
    counter.textContent = `Page ${currentPageIndex + 1} of ${albumState.pages.length}`;
  }

  const prevBtn = document.getElementById("btn-prev-page");
  const nextBtn = document.getElementById("btn-next-page");
  if (prevBtn) prevBtn.disabled = (currentPageIndex <= 0);
  if (nextBtn) nextBtn.disabled = (currentPageIndex >= albumState.pages.length - 1);

  const albumBtn = document.getElementById("btn-download-album-pdf");
  if (albumBtn) {
    albumBtn.textContent = `📥 Download Album PDF (${albumState.pages.length} pages)`;
  }

  // Ensure the active page tab is smoothly scrolled into the visible filmstrip viewport
  const activeTab = strip.querySelector(".page-tab.active");
  if (activeTab) {
    activeTab.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "nearest"
    });
  }
}

function goToPage(targetIndex) {
  if (targetIndex < 0 || targetIndex >= albumState.pages.length) return;
  currentPageIndex = targetIndex;
  renderFilmstrip();
  syncUIFromCurrentPage();
  updatePreview();
}

function addNewPage() {
  const current = getCurrentPage();
  const newNo = String(albumState.pages.length + 1);
  const newPage = {
    ...JSON.parse(JSON.stringify(current)),
    no: newNo,
    template: "AAA-AAA",
    texts: {},
    labels: {}
  };
  albumState.pages.push(newPage);
  currentPageIndex = albumState.pages.length - 1;
  renderFilmstrip();
  syncUIFromCurrentPage();
  updatePreview();
}

function duplicateCurrentPage() {
  const current = getCurrentPage();
  const dupPage = {
    ...JSON.parse(JSON.stringify(current)),
    no: String(albumState.pages.length + 1)
  };
  albumState.pages.splice(currentPageIndex + 1, 0, dupPage);
  currentPageIndex += 1;
  renderFilmstrip();
  syncUIFromCurrentPage();
  updatePreview();
}

function deleteCurrentPage() {
  if (albumState.pages.length <= 1) {
    alert("Album must contain at least one page.");
    return;
  }
  albumState.pages.splice(currentPageIndex, 1);
  if (currentPageIndex >= albumState.pages.length) {
    currentPageIndex = albumState.pages.length - 1;
  }
  renderFilmstrip();
  syncUIFromCurrentPage();
  updatePreview();
}

function movePage(direction) {
  const newIdx = currentPageIndex + direction;
  if (newIdx < 0 || newIdx >= albumState.pages.length) return;
  const temp = albumState.pages[currentPageIndex];
  albumState.pages[currentPageIndex] = albumState.pages[newIdx];
  albumState.pages[newIdx] = temp;
  currentPageIndex = newIdx;
  renderFilmstrip();
  syncUIFromCurrentPage();
  updatePreview();
}

function convertUnits(oldUnit, newUnit) {
  const toMmFactor = TO_MM[oldUnit] || 1.0;
  const fromMmFactor = 1.0 / (TO_MM[newUnit] || 1.0);
  const ratio = toMmFactor * fromMmFactor;

  const dimFields = [
    "pagewidth", "pageheight", "topmargin", "bottommargin",
    "leftmargin", "rightmargin", "header1pos", "header2pos",
    "maxxdistance", "maxydistance"
  ];

  albumState.unit = newUnit;
  dimFields.forEach(field => {
    if (albumState[field] !== undefined) {
      albumState[field] = Math.round((albumState[field] * ratio) * 100) / 100;
    }
  });

  // Convert all pages in album
  albumState.pages.forEach(p => {
    p.unit = newUnit;
    dimFields.forEach(field => {
      if (p[field] !== undefined) {
        p[field] = Math.round((p[field] * ratio) * 100) / 100;
      }
    });
  });

  syncUIFromCurrentPage();
  renderRowBuilder();
  renderCatalogModal();
  updatePreview();
  setTimeout(fitToScreen, 80);
}

function fitToScreen() {
  const previewPane = document.querySelector(".preview-pane");
  const toolbar = document.querySelector(".preview-toolbar");
  const paper = document.getElementById("preview-paper");
  if (!previewPane || !paper) return;

  const p = getCurrentPage();
  const pw = p.pagewidth || 210;
  const ph = p.pageheight || 297;
  const aspect = pw / ph;

  // Visible viewport space inside preview-pane
  const toolbarH = toolbar ? (toolbar.offsetHeight + 24) : 60;
  const availW = previewPane.clientWidth - 48;
  const availH = previewPane.clientHeight - toolbarH - 48;

  if (availW <= 0 || availH <= 0) {
    setZoom(1.0);
    return;
  }

  const baseW = 620;
  const baseH = baseW / aspect;

  const scaleW = availW / baseW;
  const scaleH = availH / baseH;

  // Fit both dimensions comfortably within viewport
  let fitScale = Math.min(scaleW, scaleH);
  fitScale = Math.min(Math.max(0.25, fitScale), 2.0);

  setZoom(Math.round(fitScale * 100) / 100);
}

function setZoom(val) {
  zoomLevel = Math.min(Math.max(0.25, val), 3.0);
  const label = document.getElementById("zoom-level");
  if (label) label.textContent = `${Math.round(zoomLevel * 100)}%`;

  const paper = document.getElementById("preview-paper");
  if (paper) {
    paper.style.transform = `scale(${zoomLevel})`;

    const p = getCurrentPage();
    const pw = p.pagewidth || 210;
    const ph = p.pageheight || 297;
    const aspect = pw / ph;
    const baseW = 620;
    const baseH = baseW / aspect;
    const scaledH = baseH * zoomLevel;

    const wrapper = document.querySelector(".preview-wrapper");
    if (wrapper) {
      wrapper.style.minHeight = `${scaledH + 24}px`;
    }
  }
}

function syncUIFromCurrentPage() {
  const p = getCurrentPage();
  for (const [key, val] of Object.entries(p)) {
    const el = document.getElementById(key);
    if (el) {
      el.value = val === null ? "" : val;
    }
  }
  // Sync unit labels in custom size drawer
  document.querySelectorAll(".unit-label").forEach(el => {
    el.textContent = p.unit || "mm";
  });
  syncTemplateInput();
  renderCustomSizes();
  renderRowBuilder();
}

function syncTemplateInput() {
  const p = getCurrentPage();
  const el = document.getElementById("template-input");
  if (el) el.value = p.template;
}

function renderCustomSizes() {
  const container = document.getElementById("custom-sizes-list");
  if (!container) return;
  const p = getCurrentPage();
  if (!p.custom_sizes) p.custom_sizes = {};
  
  container.innerHTML = "";
  const entries = Object.entries(p.custom_sizes);
  if (entries.length === 0) {
    container.innerHTML = `<span style="font-size:0.7rem; color:var(--text-muted); font-style:italic;">No custom sizes defined on this page yet.</span>`;
    return;
  }

  for (const [code, dims] of entries) {
    const w = Array.isArray(dims) ? dims[0] : dims.width;
    const h = Array.isArray(dims) ? dims[1] : dims.height;
    const pill = document.createElement("div");
    pill.style.cssText = "display:inline-flex; align-items:center; gap:0.35rem; background:#fff; border:1px solid #1a73e8; border-radius:12px; padding:0.2rem 0.55rem; font-size:0.75rem; cursor:pointer;";
    pill.title = "Click to edit this custom size";
    pill.innerHTML = `<strong>${code}</strong>: ${w}×${h} ${p.unit || 'mm'} <span class="delete-custom-btn" style="cursor:pointer; color:#d93025; font-weight:bold; margin-left:0.25rem; font-size:0.8rem;" title="Delete custom size">✕</span>`;
    
    pill.addEventListener("click", (e) => {
      if (e.target.classList.contains("delete-custom-btn")) {
        e.stopPropagation();
        deleteCustomSize(code);
        return;
      }
      const codeInput = document.getElementById("custom-size-code");
      const widthInput = document.getElementById("custom-size-width");
      const heightInput = document.getElementById("custom-size-height");
      if (codeInput) codeInput.value = code;
      if (widthInput) widthInput.value = w;
      if (heightInput) heightInput.value = h;
    });

    container.appendChild(pill);
  }
}

function addOrUpdateCustomSize() {
  const codeInput = document.getElementById("custom-size-code");
  const widthInput = document.getElementById("custom-size-width");
  const heightInput = document.getElementById("custom-size-height");
  if (!codeInput || !widthInput || !heightInput) return;

  let code = codeInput.value.trim().toUpperCase();
  if (!code) code = "X";
  
  const width = parseFloat(widthInput.value);
  const height = parseFloat(heightInput.value);

  if (isNaN(width) || isNaN(height) || width <= 0 || height <= 0) {
    alert("Please enter positive numeric width & height (e.g. 45 × 30).");
    return;
  }

  const p = getCurrentPage();
  if (!p.custom_sizes) p.custom_sizes = {};
  
  p.custom_sizes[code] = [width, height];
  
  renderCustomSizes();
  renderRowBuilder();
  updatePreview();
}

function deleteCustomSize(code) {
  const p = getCurrentPage();
  if (p.custom_sizes && p.custom_sizes[code]) {
    delete p.custom_sizes[code];
    renderCustomSizes();
    renderRowBuilder();
    updatePreview();
  }
}

function renderSizeOptions(selectedChar) {
  let opts = "";
  const portrait = [];
  const landscape = [];
  const p = getCurrentPage();

  // Custom sizes defined on the active page
  if (p.custom_sizes && Object.keys(p.custom_sizes).length > 0) {
    opts += `<optgroup label="⭐ Custom Sizes">`;
    for (const [code, dims] of Object.entries(p.custom_sizes)) {
      const m = getMountMetrics(code);
      const label = p.unit === "in"
        ? `${code} (${m.w_in}×${m.h_in}" / ${m.w_mm}×${m.h_mm}mm)`
        : `${code} (${m.w_mm}×${m.h_mm}mm / ${m.w_in}×${m.h_in}")`;
      opts += `<option value="${code}" ${code === selectedChar ? 'selected' : ''}>${label}</option>`;
    }
    opts += `</optgroup>`;
  }

  const codes = Object.keys(standardSizes).length > 0 ? Object.keys(standardSizes) : Object.keys(BUILTIN_STAMP_SIZES);

  codes.forEach(code => {
    // Only include if not overridden by custom_sizes
    if (p.custom_sizes && p.custom_sizes[code]) return;
    if (code.match(/[A-Z]/)) {
      portrait.push(code);
    } else {
      landscape.push(code);
    }
  });

  opts += `<optgroup label="Portrait (A-Z)">`;
  portrait.forEach(code => {
    const m = getMountMetrics(code);
    const label = p.unit === "in"
      ? `${code} (${m.w_in}×${m.h_in}" / ${m.w_mm}×${m.h_mm}mm)`
      : `${code} (${m.w_mm}×${m.h_mm}mm / ${m.w_in}×${m.h_in}")`;
    opts += `<option value="${code}" ${code === selectedChar ? 'selected' : ''}>${label}</option>`;
  });
  opts += `</optgroup>`;

  opts += `<optgroup label="Landscape (a-v)">`;
  landscape.forEach(code => {
    const m = getMountMetrics(code);
    const label = p.unit === "in"
      ? `${code} (${m.w_in}×${m.h_in}" / ${m.w_mm}×${m.h_mm}mm)`
      : `${code} (${m.w_mm}×${m.h_mm}mm / ${m.w_in}×${m.h_in}")`;
    opts += `<option value="${code}" ${code === selectedChar ? 'selected' : ''}>${label}</option>`;
  });
  opts += `</optgroup>`;

  return opts;
}

window.changeStampCode = (rowIdx, stampIdx, newCode) => {
  const p = getCurrentPage();
  const lines = p.template.split("-");
  const rowChars = lines[rowIdx].split("");
  rowChars[stampIdx] = newCode;
  lines[rowIdx] = rowChars.join("");
  p.template = lines.join("-");
  syncTemplateInput();
  renderRowBuilder();
  updatePreviewDebounced();
};

window.addStampToRow = (rowIdx, code = "A") => {
  const p = getCurrentPage();
  const lines = p.template.split("-");
  lines[rowIdx] += code;
  p.template = lines.join("-");
  syncTemplateInput();
  renderRowBuilder();
  updatePreview();
};

window.removeRow = (rowIdx) => {
  const p = getCurrentPage();
  const lines = p.template.split("-");
  lines.splice(rowIdx, 1);
  p.template = lines.join("-");
  syncTemplateInput();
  renderRowBuilder();
  updatePreview();
};

window.removeStamp = (rowIdx, stampIdx) => {
  const p = getCurrentPage();
  const lines = p.template.split("-");
  const rowChars = lines[rowIdx].split("");
  rowChars.splice(stampIdx, 1);
  lines[rowIdx] = rowChars.join("");
  p.template = lines.join("-");
  syncTemplateInput();
  renderRowBuilder();
  updatePreview();
};

window.updateStampText = (coordKey, val) => {
  const p = getCurrentPage();
  if (val.trim()) {
    p.texts[coordKey] = val;
  } else {
    delete p.texts[coordKey];
  }
  updatePreviewDebounced();
};

window.updateStampLabel = (coordKey, val) => {
  const p = getCurrentPage();
  if (val.trim()) {
    p.labels[coordKey] = val;
  } else {
    delete p.labels[coordKey];
  }
  updatePreviewDebounced();
};

let debounceTimer = null;
function updatePreviewDebounced() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(updatePreview, 120);
}

function getCleanPagePayload(p) {
  const payload = { ...p };
  if (!payload.rightfooter || !payload.rightfooter.trim()) {
    delete payload.rightfooter;
  }
  return payload;
}

async function updatePreview() {
  const previewBox = document.getElementById("preview-content");
  const paper = document.getElementById("preview-paper");
  if (!previewBox) return;

  const p = getCurrentPage();
  if (paper && p.pagewidth > 0 && p.pageheight > 0) {
    paper.style.aspectRatio = `${p.pagewidth} / ${p.pageheight}`;
  }

  try {
    const res = await fetch("/api/v1/render/svg", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(getCleanPagePayload(p))
    });
    if (res.ok) {
      const svgText = await res.text();
      previewBox.innerHTML = svgText;
    } else {
      console.error("Preview render failed", await res.text());
    }
  } catch (err) {
    console.error("Error fetching preview:", err);
  }
}

async function downloadSinglePdf(page) {
  const res = await fetch("/api/v1/render/pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(getCleanPagePayload(page))
  });
  if (res.ok) {
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${page.country || "page"}_${page.year || ""}_${page.no || ""}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
}

async function downloadFullAlbumPdf() {
  const albumPayload = {
    country: albumState.country || "Album",
    area: albumState.area || "",
    year: albumState.year || "",
    unit: albumState.unit || "mm",
    pagewidth: albumState.pagewidth || 210,
    pageheight: albumState.pageheight || 297,
    pages: albumState.pages.map(p => getCleanPagePayload(p))
  };

  const res = await fetch("/api/v1/render/album/pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(albumPayload)
  });
  if (res.ok) {
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${albumState.country || "Album"}_Complete_${albumState.pages.length}pages.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } else {
    alert("Failed to render album PDF: " + (await res.text()));
  }
}

async function downloadSvg() {
  const p = getCurrentPage();
  const res = await fetch("/api/v1/render/svg", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(getCleanPagePayload(p))
  });
  if (res.ok) {
    const svgText = await res.text();
    const blob = new Blob([svgText], { type: "image/svg+xml" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${p.country || "page"}_${p.year || ""}.svg`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
}

// -------------------------------------------------------------
// Pure Client-Side & API Batch Notation Helpers
// -------------------------------------------------------------

function clientSerializeBatch(pages) {
  const lines = ["# Albumatic Batch Notation (Year | Page# | Area / Subtitle | Template | Texts | Labels)"];
  pages.forEach((p, idx) => {
    const year = p.year || "";
    const no = p.no || String(idx + 1);
    const area = p.area || "";
    const template = p.template || "X";
    let line = `${year} | ${no} | ${area} | ${template}`;
    if (p.texts && Object.keys(p.texts).length > 0) {
      const tStr = "t:" + Object.entries(p.texts).map(([k, v]) => `${k}=${v}`).join(",");
      line += ` | ${tStr}`;
    }
    if (p.labels && Object.keys(p.labels).length > 0) {
      const lStr = "l:" + Object.entries(p.labels).map(([k, v]) => `${k}=${v}`).join(",");
      line += ` | ${lStr}`;
    }
    lines.push(line);
  });
  return lines.join("\n");
}

function clientParseBatch(text, defaultPage) {
  const rawLines = text.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
  if (!rawLines.length) return [];

  // Check if single line separated by slashes
  let entries = rawLines;
  if (rawLines.length === 1 && rawLines[0].includes("/") && !rawLines[0].startsWith("http") && !rawLines[0].startsWith("/pdf")) {
    entries = rawLines[0].split("/").map(e => e.trim()).filter(Boolean);
  }

  const pages = [];
  entries.forEach((entry, idx) => {
    const base = JSON.parse(JSON.stringify(defaultPage || {}));
    if (entry.includes("|")) {
      const parts = entry.split("|").map(s => s.trim());
      if (parts[0]) base.year = parts[0];
      base.no = parts[1] || String(idx + 1);
      if (parts[2]) base.area = parts[2];
      if (parts[3]) base.template = parts[3];

      base.texts = {};
      base.labels = {};
      parts.slice(4).forEach(extra => {
        if (extra.startsWith("t:")) {
          extra.substring(2).split(",").forEach(pair => {
            const [k, v] = pair.split("=");
            if (k && v) base.texts[k.trim()] = v.trim();
          });
        } else if (extra.startsWith("l:")) {
          extra.substring(2).split(",").forEach(pair => {
            const [k, v] = pair.split("=");
            if (k && v) base.labels[k.trim()] = v.trim();
          });
        }
      });
      pages.push(base);
    } else {
      // Pure template or URL
      base.template = entry;
      base.no = String(idx + 1);
      base.texts = {};
      base.labels = {};
      pages.push(base);
    }
  });
  return pages;
}

function updateBatchCount() {
  const ta = document.getElementById("batch-text-area");
  const countEl = document.getElementById("batch-page-count");
  if (!ta || !countEl) return;
  const current = getCurrentPage();
  const pages = clientParseBatch(ta.value, current);
  countEl.textContent = `Detected: ${pages.length} page${pages.length === 1 ? '' : 's'}`;
}

// Batch Modal Actions
function showBatchModal() {
  exportBatchText();
  document.getElementById("batch-modal")?.classList.add("active");
}

function hideBatchModal() {
  document.getElementById("batch-modal")?.classList.remove("active");
}

async function exportBatchText() {
  const ta = document.getElementById("batch-text-area");
  if (!ta) return;

  // Immediate synchronous populate
  ta.value = clientSerializeBatch(albumState.pages);
  updateBatchCount();

  // Also sync with server endpoint
  try {
    const res = await fetch("/api/v1/batch/serialize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(albumState.pages.map(p => getCleanPagePayload(p)))
    });
    if (res.ok) {
      const data = await res.json();
      if (data.text) {
        ta.value = data.text;
        updateBatchCount();
      }
    }
  } catch (err) {
    // Client-side serialization already populated
  }
}

async function applyBatchNotation() {
  const ta = document.getElementById("batch-text-area");
  if (!ta || !ta.value.trim()) {
    alert("Please enter or paste batch template lines.");
    return;
  }

  const current = getCurrentPage();
  let parsedPages = clientParseBatch(ta.value, current);

  // Try server-side validation & enrichment
  try {
    const req = {
      text: ta.value,
      country: current.country || "COUNTRY",
      area: current.area || "Area",
      year: current.year || "YYYY",
      unit: current.unit || "mm"
    };
    const res = await fetch("/api/v1/batch/parse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req)
    });
    if (res.ok) {
      const data = await res.json();
      if (data.pages && data.pages.length > 0) {
        parsedPages = data.pages;
      }
    }
  } catch (err) {
    // Fall back to client parsed pages
  }

  if (parsedPages && parsedPages.length > 0) {
    albumState.pages = parsedPages;
    currentPageIndex = 0;
    renderFilmstrip();
    syncUIFromCurrentPage();
    updatePreview();
    hideBatchModal();
  } else {
    alert("Could not parse any valid pages from batch text.");
  }
}

async function showExportModal() {
  const modal = document.getElementById("export-modal");
  if (!modal) return;

  const p = getCurrentPage();
  const res = await fetch("/api/v1/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(getCleanPagePayload(p))
  });
  const data = await res.json();
  const statelessUrl = window.location.origin + data.url;

  document.getElementById("code-url").textContent = statelessUrl;
  document.getElementById("code-curl").textContent = `curl -X GET "${statelessUrl}" -o "${p.country || 'page'}.pdf"`;
  document.getElementById("code-json").textContent = JSON.stringify(getCleanPagePayload(p), null, 2);

  modal.classList.add("active");
}

function hideExportModal() {
  document.getElementById("export-modal")?.classList.remove("active");
}

function showHelpModal() {
  document.getElementById("help-modal")?.classList.add("active");
}

function hideHelpModal() {
  document.getElementById("help-modal")?.classList.remove("active");
}

function renderCatalogModal() {
  const grid = document.getElementById("catalog-grid");
  if (!grid) return;
  grid.innerHTML = "";

  const codes = Object.keys(standardSizes).length > 0 ? Object.keys(standardSizes) : Object.keys(BUILTIN_STAMP_SIZES);

  codes.forEach(code => {
    const m = getMountMetrics(code);
    const item = document.createElement("div");
    item.className = "catalog-item";
    item.dataset.code = code;
    item.dataset.dims = `${m.w_mm}x${m.h_mm} ${m.w_in}x${m.h_in}`;
    item.innerHTML = `
      <div style="display:flex; flex-direction:column;">
        <span><strong>${code}</strong> <small style="color:var(--text-muted)">(${m.orientation})</small></span>
        <span style="font-size:0.7rem; color:var(--text-muted);">${m.w_in}″ × ${m.h_in}″</span>
      </div>
      <span style="font-weight:600; font-size:0.75rem;">${m.w_mm} × ${m.h_mm} mm</span>
    `;
    item.title = `Click to append '${code}' to active page`;
    item.addEventListener("click", () => {
      const p = getCurrentPage();
      const lines = p.template ? p.template.split("-") : [""];
      lines[lines.length - 1] += code;
      p.template = lines.join("-");
      syncTemplateInput();
      renderRowBuilder();
      updatePreview();
      hideHelpModal();
    });
    grid.appendChild(item);
  });
}

function filterCatalog(query) {
  const q = query.toLowerCase().trim();
  const items = document.querySelectorAll(".catalog-item");
  items.forEach(el => {
    const match = el.dataset.code.toLowerCase().includes(q) || el.dataset.dims.includes(q);
    el.style.display = match ? "flex" : "none";
  });
}

window.copySnippet = (elemId) => {
  const text = document.getElementById(elemId)?.textContent;
  if (text) {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  }
};

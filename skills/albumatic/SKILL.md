---
name: albumatic
description: >-
  Generate print-ready vector PDF & SVG stamp album pages directly from Antigravity.
  Supports multi-page album generation, batch notation, cURL REST endpoints, and individual SVG export for Inkscape editing.
---

# Albumatic: Stamp Album Generator Skill

This skill allows Antigravity to generate high-precision, print-ready vector PDF and SVG stamp album pages directly from user requests, philatelic descriptions, batch notation, or stateless URLs.

---

## 1. Quick Capabilities Overview

- **Single-Page PDF & SVG Generation**: Render individual album pages with parametric stamp mount grids, centered captions, labels, headers, and footers.
- **Whole-Album Combined PDF**: Generate 1 to 50+ page complete stamp albums in a single PDF document.
- **Individual Inkscape-Ready SVGs**: Export clean vector SVG files for every page in an album so the user can edit layouts, borders, and graphics in **Inkscape**.
- **Full International Unicode**: Flawlessly renders Cyrillic, Greek, Arabic, Chinese, Devanagari, European diacritics (`Å`, `Ä`, `Ö`, `é`), and philatelic symbols (`½A`, `№`, `★`, `€`).
- **Physical Stamp Safe Inset**: Text inside placeholders automatically wraps across lines and stays under the physical stamp without spilling into clear mount margins.

---

## 2. Generating Album Pages via cURL / REST API

When the Albumatic web server is running (default `http://localhost:8000`), you can invoke the REST API directly using `curl`:

### A. Download Combined Full Album PDF (All Pages in One PDF)
```bash
curl -s -X POST "http://localhost:8000/api/v1/render/album/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Suomi — Finland",
    "pages": [
      {
        "country": "Suomi — Finland",
        "area": "1856 Soikiomalli — Oval Issue",
        "year": "1856",
        "no": "1",
        "template": "ee-e",
        "texts": {"1_1": "5 kop", "1_2": "10 kop", "2_1": "5 kop"},
        "labels": {"1_1": "Small Pearl", "2_1": "Large Pearl"}
      },
      {
        "country": "Suomi — Finland",
        "area": "1860 Vaakunamalli — Serpentine Roulette I",
        "year": "1860",
        "no": "2",
        "template": "LL-LL",
        "texts": {"1_1": "5 kop. sininen", "1_2": "10 kop. ruusu", "2_1": "5 kop. tumma sini", "2_2": "10 kop. karmiini"},
        "labels": {"1_1": "Hammaste I", "1_2": "Hammaste I", "2_1": "Uurteeton", "2_2": "Ohut paperi"}
      }
    ]
  }' -o "Finland_1856-1860_Album.pdf"
```

### B. Download Single Page PDF
```bash
curl -s -X POST "http://localhost:8000/api/v1/render/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "area": "1934 National Parks Issue (Scott 740–749)",
    "year": "1934",
    "no": "1",
    "template": "AAA-dddd-ddd",
    "texts": {"1_1": "1¢ green", "1_2": "2¢ red orange", "1_3": "6¢ blue"},
    "labels": {"1_1": "Yosemite (El Capitan)", "1_2": "Grand Canyon", "1_3": "Crater Lake"}
  }' -o "USA_1934_National_Parks.pdf"
```

### C. Download SVG (Ready for Inkscape Vector Editing)
```bash
curl -s -X POST "http://localhost:8000/api/v1/render/svg" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "United States",
    "area": "1934 National Parks Issue",
    "year": "1934",
    "no": "1",
    "template": "AAA-dddd-ddd"
  }' -o "USA_1934_National_Parks.svg"
```

### D. Download from Stateless URL Shorthand
```bash
curl -s "http://localhost:8000/pdf/USA/National%20Parks/1934/1/AAA-dddd-ddd?t_1_1=1%C2%A2%20green&l_1_1=Yosemite" -o "parks.pdf"
```

---

## 3. Automated Batch & Multi-Page Generator Helper

Use the included helper script `render_album.py` to generate complete albums in both PDF and SVG formats from rich batch notation or prompt data:

```bash
# Generate both multi-page PDF and individual Inkscape SVGs from batch text
python3 skills/albumatic/scripts/render_album.py \
  --country "Finland" \
  --batch "1856 | 1 | 1856 Soikiomalli | ee-e | t:1_1=5 kop,1_2=10 kop,2_1=5 kop | l:1_1=Small Pearl,2_1=Large Pearl
1860 | 2 | 1860 Roulette I | LL-LL | t:1_1=5 kop.,1_2=10 kop. | l:1_1=Perf I,1_2=Perf I" \
  --format both \
  --outdir ./my_finland_album

# Generate SVG only for Inkscape editing
python3 skills/albumatic/scripts/render_album.py \
  --country "China" \
  --template "XXX-XXX" \
  --format svg \
  --outdir ./svg_exports
```

---

## 4. Stamp Mount Catalog Reference

| Code | Type | Dimensions (mm) | Dimensions (in) | Typical Uses |
| :--- | :--- | :--- | :--- | :--- |
| **`A`** | Portrait | 20.0 × 24.0 mm | 0.79″ × 0.94″ | Standard small definitive stamps (US, UK, Europe) |
| **`B`** | Portrait | 20.0 × 26.0 mm | 0.79″ × 1.02″ | Classic European definitives |
| **`D`** | Portrait | 21.5 × 26.0 mm | 0.85″ × 1.02″ | Classic Finnish penni values (1875, 1885, 1889) |
| **`G`** | Portrait | 24.0 × 29.0 mm | 0.94″ × 1.14″ | Large format Finnish Markka values |
| **`L`** | Portrait | 26.0 × 31.0 mm | 1.02″ × 1.22″ | Finnish 1856 Oval issue, 1860/1866 Serpentine Roulettes |
| **`X`** | Square | 35.0 × 35.0 mm | 1.38″ × 1.38″ | Large square stamps (China Large Dragon, Nepal Crossed Knives) |
| **`a`** | Landscape | 24.0 × 21.0 mm | 0.94″ × 0.83″ | Standard landscape definitives |
| **`d`** | Landscape | 31.0 × 24.0 mm | 1.22″ × 0.94″ | Landscape commemoratives (US 1934 Parks, Nepal Shiva) |
| **`h`** | Landscape | 36.0 × 25.0 mm | 1.42″ × 0.98″ | Wide landscape commemoratives |

*Custom dimensions can be defined inline using `s:X=width,height` or query `?size_X=width,height`.*

---

## 5. Working with Inkscape Vector Output

When `--format svg` or `--format both` is used:
1. Albumatic creates 100% standard W3C SVG vector files.
2. Open with Inkscape:
   ```bash
   inkscape ./my_finland_album/Finland_1856_1_1856_Soikiomalli.svg
   ```
3. In Inkscape, stamps, text elements, and borders reside on clean structured SVG groups with precise millimetric coordinates for custom framing, philatelic plating, or ornamental borders.

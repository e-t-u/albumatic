# Albumatic

**Albumatic** is a stateless declarative stamp album page layout and vector PDF generator.

It allows you to specify stamp arrangements, mount sizes, textual annotations, and custom dimensions either through an interactive web visual designer, a stateless REST API / URL query system, a CLI tool, or Python scripts.

---

## Features

- **100% Stateless:** No database, session, or login required. Every album page is deterministically computed from its configuration or URL parameters.
- **Interactive Visual Web Designer:** Single-page app with drag-and-drop row/mount builders and instant real-time vector SVG preview.
- **Standard Philatelic Mount Dimensions:** All size codes (`A`–`Z`, `a`–`v`) define the printed **Mount Box (Frame)** on the page (matching Hawid/Leuchtturm protective mounts), with automatic safe insets so inner text stays hidden under the physical stamp.
- **REST API & Legacy URL Compatibility:** Fully supports modern JSON endpoints as well as legacy `/pdf/<country>/<area>/<year>/<no>/<template>` routes.
- **Vector PDF & SVG Generation:** Clean, print-ready vector graphics rendered with ReportLab.
- **Local & Remote Execution:** Can be run locally via CLI (`albumatic render`) or as a local web server (`albumatic serve`).

---

## Container Deployment (Docker / Podman)

Run Albumatic in a lightweight, self-contained container with full Unicode vector TrueType fonts pre-installed:

### Using Docker / Podman Compose (Recommended)

```bash
# Start container with compose
docker compose up -d
# or with podman
podman-compose up -d
```
Access the interactive web designer at [http://localhost:8000](http://localhost:8000).

### Using Docker / Podman CLI

```bash
# Build container image
docker build -t albumatic .
# or
podman build -t albumatic .

# Run container
docker run -d -p 8000:8000 --name albumatic albumatic
# or
podman run -d -p 8000:8000 --name albumatic albumatic
```

### Health Check

```bash
curl http://localhost:8000/health
# {"status":"ok","service":"albumatic","version":"6.0.0"}
```

---

## Quickstart

### 1. Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install albumatic and dependencies
pip install -e .
```

### 2. Launch Local Web App & REST API

```bash
albumatic serve
# or: uvicorn albumatic.api:app --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser to use the interactive visual designer.

Interactive API Swagger documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Command-Line Usage

### Render PDF directly:
```bash
albumatic render --template "ABBA-hh-BBB" --country "USA" --area "Definitives" --year "2009" --no "1" --output page.pdf
```

### Render SVG vector:
```bash
albumatic render --template "ABBA-hh-BBB" --format svg -o preview.svg
```

### Render from a stateless URL:
```bash
albumatic render --url "/pdf/USA/Definitives/2009/1/ABBA-hh-BBB?t_1_1=Blue&l_1_1=10c" -o page.pdf
```

---

## Antigravity Skill & AI Integration

Albumatic includes an automated **Antigravity Skill** (`skills/albumatic/`) that allows AI agents to design, generate, and download print-ready stamp albums directly from natural language prompts.

### What It Supports:
- **Whole-Album Combined PDF**: Generate 1 to 50+ page complete stamp albums in a single PDF document.
- **Individual Inkscape-Ready SVGs**: Export clean vector SVG files for every page in an album so you can open and edit them in **Inkscape**.
- **Physical Stamp Safe Insets**: Placeholder texts automatically wrap across lines and stay safely inside the physical stamp area without touching clear mount margins.
- **Full International Unicode**: Cyrillic, Greek, Arabic, Chinese, Devanagari, European diacritics, and philatelic symbols (`½A`, `№`, `★`, `€`).

### Running the Skill Helper Script:
```bash
# Generate both multi-page PDF and individual Inkscape SVGs from batch text
python3 skills/albumatic/scripts/render_album.py \
  --country "Suomi — Finland" \
  --batch "1856 | 1 | 1856 Soikiomalli | ee-e | t:1_1=5 kop,1_2=10 kop,2_1=5 kop | l:1_1=Small Pearl,2_1=Large Pearl
1860 | 2 | 1860 Roulette I | LL-LL | t:1_1=5 kop. sininen,1_2=10 kop. ruusu | l:1_1=Hammaste I,1_2=Hammaste I" \
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

## REST API & cURL Examples

When running the Albumatic server (`albumatic serve` or container):

### 1. Download Combined Full-Album PDF:
```bash
curl -s -X POST "http://localhost:8000/api/v1/render/album/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Suomi — Finland",
    "pages": [
      {
        "area": "1856 Soikiomalli — Oval Issue",
        "year": "1856",
        "no": "1",
        "template": "ee-e",
        "texts": {"1_1": "5 kop", "1_2": "10 kop", "2_1": "5 kop"},
        "labels": {"1_1": "Small Pearl", "2_1": "Large Pearl"}
      },
      {
        "area": "1860 Vaakunamalli — Serpentine Roulette I",
        "year": "1860",
        "no": "2",
        "template": "LL-LL",
        "texts": {"1_1": "5 kop. sininen", "1_2": "10 kop. ruusu"},
        "labels": {"1_1": "Hammaste I", "1_2": "Hammaste I"}
      }
    ]
  }' -o "Finland_Classic_Album.pdf"
```

### 2. Download Single Page PDF:
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

### 3. Download Vector SVG (for Inkscape):
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

---

## Python Client SDK

```python
import contrib.pyalbumatic as pyalbumatic

a = pyalbumatic.Albumatic()
a["country"] = "Nepal"
a["year"] = "1881"
a["template"] = "XXX-X-XXX-X"
a["t_1_1"] = "blue"
a["l_1_1"] = "pin perf. 1A"

# Renders either via HTTP API or in-process local vector engine
a.writefile("nepal_1881.pdf")
```

---

## Keyboard Shortcuts in Web Designer

- **`ArrowLeft` / `PageUp`**: Go to previous page.
- **`ArrowRight` / `PageDown`**: Go to next page.
- **`Home` / `End`**: Jump to first / last page.
- **`Alt + ArrowLeft` / `Alt + ArrowRight`**: Navigate pages even while focusing an input.
- **`Ctrl + MouseWheel`**: Zoom in/out on real-time preview paper.

---

## Running Tests

```bash
pytest
```

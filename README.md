# Albumatic

**Albumatic** is a stateless declarative stamp album page layout and vector PDF generator.

It allows you to specify stamp arrangements, mount sizes, textual annotations, and custom dimensions either through an interactive web visual designer, a stateless REST API / URL query system, a CLI tool, or Python scripts.

---

## Features

- **100% Stateless:** No database, session, or login required. Every album page is deterministically computed from its configuration or URL parameters.
- **Interactive Visual Web Designer:** Single-page app with drag-and-drop row/mount builders and instant real-time vector SVG preview.
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

## Running Tests

```bash
pytest
```

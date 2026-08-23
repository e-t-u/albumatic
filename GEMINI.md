# Albumatic: Developer & Architecture Specification

This document provides a comprehensive codebase analysis and technical specification of **Albumatic** for AI assistants (like Gemini) and developers modifying, modernizing, or extending the code.

---

## 1. Project Overview & Core Purpose

**Albumatic** is a stateless declarative stamp album page generation engine. It takes stamp layout definitions, dimensional constraints, and textual annotations via URL path and query parameters (stateless API), JSON REST endpoints, or Python scripts, and renders print-ready vector PDF & SVG album pages using **ReportLab**.

### Key Characteristics
- **Stateless URL & REST Generation:** Completely stateless. A single URL or JSON payload specifies the layout, stamps, margins, headers, footers, and per-stamp texts without server-side session state, database, or authentication.
- **Full International Unicode Support:** Employs high-coverage TrueType fonts (`Liberation Sans`, `FreeSans`, `DejaVu Sans`, `Noto Sans`) ensuring flawless vector rendering for all international character sets (Cyrillic, Greek, Devanagari, Asian scripts, European diacritics, and philatelic symbols like `½A`, `№`, `★`, `€`).
- **Multi-Page & Batch Album Generation:** Render 30+ album pages in a single combined PDF using batch notations (`AA-BB-CC/cc-ddd-a/...` or pipe-delimited records).
- **Parametric Vector Layout Engine:** Dynamically calculates stamp row distributions, spacing bounds (`maxxdistance`, `maxydistance`), and centered stamp boxes.
- **Interactive Single-Page Web Designer:** Built-in interactive browser visual designer with multi-page filmstrip, hero stamp row builder, dynamic auto-fit SVG preview, and album-wide collapsible paper/margin settings.
- **Extensible Mount Catalog:** Built-in standard sizes for Hawid/Leuchtturm stamp mounts (`A`–`Z` for portrait/square, `a`–`v` for landscape), showing both millimeter and imperial inch dimensions with fallback metric calculators.
- **Container Ready:** Multi-platform Docker & Podman Compose configurations with system Unicode fonts pre-configured.

---

## 2. Codebase Structure & File Map

```
albumatic/
├── GEMINI.md               # Developer and AI specification reference (this file)
├── README.md               # Project documentation & quickstart guide
├── pyproject.toml          # Modern Python packaging configuration
├── requirements.txt        # Pinned dependencies
├── Dockerfile              # Container definition with pre-installed Unicode fonts
├── compose.yaml            # Docker / Podman Compose orchestration
├── docker-compose.yml      # Backward-compatible compose alias
├── .dockerignore           # Container build exclusions
├── .gitignore              # Git ignore rules
├── albumatic/              # Core Python module
│   ├── __init__.py         # Package exports
│   ├── models.py           # Typed Pydantic data models (PageConfig, AlbumConfig, StampItem, Unit)
│   ├── sizes.py            # Standard Hawid/Leuchtturm mount catalog (mm + in)
│   ├── fonts.py            # Unicode TrueType font discovery & registration
│   ├── engine.py           # Decoupled layout math, ReportLab PDF and SVG renderers
│   ├── parser.py           # Stateless URL, query & batch notation parser / serializer
│   ├── api.py              # FastAPI REST API & legacy URL endpoint handler
│   └── cli.py              # Command-line interface (`albumatic serve`, `albumatic render`)
├── web/                    # Modern Interactive Web Designer
│   ├── index.html          # Interactive GUI designer page
│   └── static/
│       ├── app.js          # Reactive controller with live SVG preview, filmstrip & batch editor
│       └── app.css         # Modern styling & responsive split-view layout
├── tests/                  # Pytest test suite (17 automated unit & integration tests)
│   ├── test_engine.py      # Layout calculation, Unicode & multi-page PDF generation tests
│   ├── test_parser.py      # URL query & batch notation parser tests
│   └── test_api.py         # REST API, batch endpoints & legacy route tests
├── contrib/
│   ├── pyalbumatic.py      # Python client SDK with remote API & in-process fallback
│   ├── nepal.py            # Batch album generation script (Nepal 1881-1962)
│   ├── sizepageurl.py      # Catalog URL generator
│   └── example.sh          # Bash/wget automation example
└── legacy/                 # Archived legacy GAE Python 2.5 code for reference
```

---

## 3. Core Architecture & Component Analysis

### A. Core Engine (`albumatic/engine.py`, `albumatic/fonts.py`, & `albumatic/models.py`)

1. **`PageConfig` & `AlbumConfig` (`albumatic/models.py`):**
   - `PageConfig`: Single-page declarative specification (`country`, `area`, `year`, `no`, `template`, `texts`, `labels`, `unit`, margins, spacing).
   - `AlbumConfig`: Multi-page album container inheriting shared album-wide defaults.

2. **`LayoutEngine` (`albumatic/engine.py`):**
   - Pure function mapping `PageConfig` -> `ComputedPageLayout`.
   - Computes vertical row distribution, horizontal stamp distribution, and absolute point coordinates.

3. **`PDFRenderer` & `SVGRenderer` (`albumatic/engine.py`):**
   - `PDFRenderer.render`: Emits single-page vector PDF with Unicode TTFonts.
   - `PDFRenderer.render_album`: Emits multi-page combined PDF document.
   - `SVGRenderer`: Emits SVG vector XML string for in-browser instant preview and vector graphic export.

### B. REST API & Web Server (`albumatic/api.py`)
- `GET /health`: Health check endpoint for container and cluster monitoring.
- `GET /api/v1/sizes`: Returns full Hawid/Leuchtturm catalog with both mm and inches.
- `POST /api/v1/render/pdf`: Accepts JSON `PageConfig` and returns single-page `application/pdf`.
- `POST /api/v1/render/album/pdf`: Accepts JSON `AlbumConfig` and returns combined multi-page `application/pdf`.
- `POST /api/v1/batch/parse`: Parses batch notation into `List[PageConfig]`.
- `POST /api/v1/batch/serialize`: Serializes `List[PageConfig]` into batch notation text.
- `POST /api/v1/render/svg`: Accepts JSON `PageConfig` and returns `image/svg+xml`.
- `GET /pdf/{path}`: Backwards-compatible route for all legacy URLs.
- `GET /`: Serves the interactive visual web designer.

---

## 4. CLI & Container Usage

```bash
# Start web server with interactive GUI
albumatic serve --port 8000

# Render single-page PDF directly
albumatic render --template "ABBA-hh-BBB" --country "USA" --output usa.pdf

# Render SVG directly
albumatic render --template "ABBA-hh-BBB" --format svg -o usa.svg

# Render from stateless URL
albumatic render --url "/pdf/USA/Definitives/2009/1/ABBA-hh-BBB?t_1_1=Blue" -o usa.pdf

# Run with Docker / Podman
docker compose up -d
```

---

## 5. Guidelines for Future AI & Developer Modifications

1. **Maintain Statelessness:** Do not introduce server-side database requirements, sessions, or authentication. All state belongs in the URL query parameters, JSON request payloads, or client-side storage.
2. **Preserve URL Compatibility:** Any changes to parameter interpretation must maintain backwards compatibility with existing links and batch scripts.
3. **Unicode Integrity:** Always use registered Unicode TrueType fonts (`AlbumaticSans`) in ReportLab rendering to guarantee international character support.

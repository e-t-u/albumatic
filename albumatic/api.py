"""FastAPI REST API and Web server for Albumatic."""

import os
import html
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from .models import PageConfig, AlbumConfig, BatchImportRequest
from .sizes import STANDARD_STAMP_SIZES, get_detailed_stamp_catalog
from .engine import LayoutEngine, PDFRenderer, SVGRenderer
from .parser import parse_legacy_path_and_query, serialize_to_url, parse_batch_notation, serialize_batch_notation

app = FastAPI(
    title="Albumatic API",
    description="Stateless Stamp Album Page Generation Engine",
    version="6.0.0",
)

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")
STATIC_DIR = os.path.join(WEB_DIR, "static")
LEGACY_STATIC_DIR = os.path.join(BASE_DIR, "static")


@app.get("/health", summary="Health check endpoint")
def health_check() -> Dict[str, str]:
    """Returns service health status."""
    return {"status": "ok", "service": "albumatic", "version": "6.0.0"}


@app.get("/api/v1/sizes", summary="Get standard stamp sizes catalog")
def get_standard_sizes() -> Dict[str, Dict[str, Any]]:
    """Returns the full catalog of standard Hawid/Leuchtturm stamp sizes with both mm and inches."""
    return get_detailed_stamp_catalog()


@app.post("/api/v1/render/pdf", summary="Render album page to PDF")
def render_pdf_post(config: PageConfig) -> Response:
    """Renders a stamp album page config directly to a vector PDF byte stream."""
    try:
        layout = LayoutEngine.compute(config)
        pdf_bytes = PDFRenderer.render(layout)
        filename = f"{config.country or 'page'}_{config.year or ''}_{config.no or ''}.pdf".replace("/", "_")
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF rendering error: {str(e)}")


@app.post("/api/v1/render/album/pdf", summary="Render multi-page album to combined PDF")
def render_album_pdf_post(album: AlbumConfig) -> Response:
    """Renders a multi-page album configuration into a single combined vector PDF document."""
    try:
        pdf_bytes = PDFRenderer.render_album(album)
        filename = f"{album.country or 'Album'}_Complete.pdf".replace("/", "_")
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Album PDF rendering error: {str(e)}")


@app.post("/api/v1/render/svg", summary="Render album page to vector SVG")
def render_svg_post(config: PageConfig) -> Response:
    """Renders a stamp album page config to an SVG vector string for live client previews."""
    try:
        layout = LayoutEngine.compute(config)
        svg_content = SVGRenderer.render(layout)
        return Response(content=svg_content, media_type="image/svg+xml")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SVG rendering error: {str(e)}")


@app.get("/api/v1/render/svg", summary="Render SVG via query parameters")
def render_svg_get(request: Request) -> Response:
    """Renders an SVG preview from URL query parameters."""
    try:
        config = parse_legacy_path_and_query(request.url.path, dict(request.query_params))
        layout = LayoutEngine.compute(config)
        svg_content = SVGRenderer.render(layout)
        return Response(content=svg_content, media_type="image/svg+xml")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SVG rendering error: {str(e)}")


@app.post("/api/v1/url", summary="Generate shareable stateless URL")
def generate_stateless_url(config: PageConfig) -> Dict[str, str]:
    """Serializes a PageConfig object into a shareable stateless URL."""
    url = serialize_to_url(config)
    return {"url": url}


@app.post("/api/v1/batch/parse", summary="Parse batch notation into album pages")
def parse_batch(req: BatchImportRequest) -> Dict[str, Any]:
    """Parses multi-line or slash-separated batch notation into a list of PageConfig items."""
    base_cfg = PageConfig(
        country=req.country or "COUNTRY",
        area=req.area or "Area",
        year=req.year or "YYYY",
        unit=req.unit,
    )
    pages = parse_batch_notation(req.text, base_cfg)
    return {"pages": [p.model_dump() for p in pages]}


@app.post("/api/v1/batch/serialize", summary="Serialize album pages to batch text notation")
def serialize_batch(pages: List[PageConfig]) -> Dict[str, str]:
    """Serializes a list of pages into clean multi-line batch text."""
    text = serialize_batch_notation(pages)
    return {"text": text}


@app.get("/pdf/{full_path:path}", summary="Legacy stateless URL PDF generator")
def render_legacy_pdf(full_path: str, request: Request) -> Response:
    """Backwards-compatible endpoint for URL-driven PDF generation."""
    try:
        config = parse_legacy_path_and_query(request.url.path, dict(request.query_params))
        layout = LayoutEngine.compute(config)
        pdf_bytes = PDFRenderer.render(layout)
        
        parts = full_path.split("/")
        filename = parts[-1] if parts and parts[-1].endswith(".pdf") else f"{config.country}_{config.no}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error rendering PDF</h3><p>{html.escape(str(e))}</p>", status_code=400)


@app.get("/pdf", summary="Legacy PDF root")
def render_legacy_pdf_root(request: Request) -> Response:
    return render_legacy_pdf("", request)


# Static assets
if os.path.isdir(STATIC_DIR):
    app.mount("/app-static", StaticFiles(directory=STATIC_DIR), name="app-static")

if os.path.isdir(LEGACY_STATIC_DIR):
    app.mount("/static", StaticFiles(directory=LEGACY_STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse, summary="Interactive Web GUI")
def serve_gui() -> HTMLResponse:
    index_file = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    legacy_file = os.path.join(BASE_DIR, "main.html")
    if os.path.exists(legacy_file):
        with open(legacy_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Albumatic</h1>")

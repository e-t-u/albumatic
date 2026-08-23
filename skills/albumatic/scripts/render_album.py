#!/usr/bin/env python3
"""Albumatic CLI & API Helper Script.

Generates single or multi-page stamp album PDFs and SVGs (for Inkscape)
via local REST API (curl/requests) or in-process engine fallback.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import re
from typing import Any, Dict, List, Optional

# Try importing in-process engine as fallback
try:
    from albumatic.models import PageConfig, AlbumConfig, Unit
    from albumatic.engine import LayoutEngine, PDFRenderer, SVGRenderer
    from albumatic.parser import parse_batch_notation, parse_legacy_path_and_query
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', '_', name).strip().strip('_')


def call_api(endpoint: str, payload: Optional[Dict[str, Any]] = None, server: str = "http://localhost:8000") -> bytes:
    url = f"{server.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def render_pages(
    pages: List[Dict[str, Any]],
    output_dir: str = "./",
    format_type: str = "pdf",
    album_title: str = "Album",
    server: str = "http://localhost:8000"
) -> Dict[str, List[str]]:
    os.makedirs(output_dir, exist_ok=True)
    created_files: Dict[str, List[str]] = {"pdf": [], "svg": []}

    # 1. Render multi-page combined PDF if requested
    if format_type in ("pdf", "both", "album_pdf"):
        album_payload = {
            "country": pages[0].get("country", album_title) if pages else album_title,
            "pages": pages
        }
        album_pdf_name = f"{sanitize_filename(album_payload['country'])}_Complete_{len(pages)}pages.pdf"
        album_pdf_path = os.path.join(output_dir, album_pdf_name)
        
        pdf_bytes = None
        # Try API first
        try:
            pdf_bytes = call_api("/api/v1/render/album/pdf", album_payload, server)
        except Exception:
            # In-process engine fallback
            if ENGINE_AVAILABLE:
                album_obj = AlbumConfig(**album_payload)
                pdf_bytes = PDFRenderer.render_album(album_obj)
        
        if pdf_bytes:
            with open(album_pdf_path, "wb") as f:
                f.write(pdf_bytes)
            created_files["pdf"].append(album_pdf_path)
            print(f"✓ Generated multi-page PDF: {album_pdf_path}")

    # 2. Render individual SVGs (for Inkscape) if requested
    if format_type in ("svg", "both"):
        for idx, page in enumerate(pages):
            country = sanitize_filename(page.get("country") or "Page")
            year = sanitize_filename(str(page.get("year") or ""))
            no = sanitize_filename(str(page.get("no") or (idx + 1)))
            area = sanitize_filename(page.get("area") or "")
            
            parts = [country]
            if year:
                parts.append(year)
            if no:
                parts.append(no)
            if area:
                parts.append(area)
            
            svg_filename = f"{'_'.join(parts)}.svg"
            svg_path = os.path.join(output_dir, svg_filename)
            
            svg_data = None
            try:
                svg_data = call_api("/api/v1/render/svg", page, server).decode("utf-8")
            except Exception:
                if ENGINE_AVAILABLE:
                    cfg_obj = PageConfig(**page)
                    layout = LayoutEngine.compute(cfg_obj)
                    svg_data = SVGRenderer.render(layout)
            
            if svg_data:
                with open(svg_path, "w", encoding="utf-8") as f:
                    f.write(svg_data)
                created_files["svg"].append(svg_path)
                print(f"✓ Generated vector SVG (Inkscape-ready): {svg_path}")

    return created_files


def main():
    parser = argparse.ArgumentParser(description="Albumatic Batch & Single Page Stamp Album Generator")
    parser.add_argument("--batch", "-b", help="Batch notation string or text")
    parser.add_argument("--file", "-f", help="Path to batch notation text file")
    parser.add_argument("--url", "-u", help="Stateless URL or path to render")
    parser.add_argument("--template", "-t", default="AAA-dddd-ddd", help="Template string for single page")
    parser.add_argument("--country", "-c", default="Country", help="Country header")
    parser.add_argument("--area", "-a", default="", help="Issue / Area subtitle")
    parser.add_argument("--year", "-y", default="", help="Year")
    parser.add_argument("--no", "-n", default="1", help="Page number")
    parser.add_argument("--format", choices=["pdf", "svg", "both"], default="both", help="Output format(s)")
    parser.add_argument("--outdir", "-o", default="./album_output", help="Output directory")
    parser.add_argument("--server", "-s", default="http://localhost:8000", help="Albumatic web server base URL")

    args = parser.parse_args()

    pages: List[Dict[str, Any]] = []

    # Case 1: Batch file or string
    batch_text = None
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            batch_text = f.read()
    elif args.batch:
        batch_text = args.batch

    if batch_text:
        # Parse batch notation
        try:
            res = json.loads(call_api("/api/v1/batch/parse", {"text": batch_text, "country": args.country, "area": args.area, "year": args.year}, args.server))
            pages = res.get("pages", [])
        except Exception:
            if ENGINE_AVAILABLE:
                base_cfg = PageConfig(country=args.country, area=args.area, year=args.year)
                parsed_objs = parse_batch_notation(batch_text, base_cfg)
                pages = [p.model_dump() for p in parsed_objs]
    elif args.url:
        # Parse from URL
        try:
            cfg = parse_legacy_path_and_query(args.url, {})
            pages = [cfg.model_dump()]
        except Exception as e:
            print(f"Error parsing URL: {e}")
            sys.exit(1)
    else:
        # Single page config
        pages = [{
            "country": args.country,
            "area": args.area,
            "year": args.year,
            "no": args.no,
            "template": args.template,
        }]

    if not pages:
        print("No pages to render.")
        sys.exit(1)

    print(f"Rendering {len(pages)} page(s) in format '{args.format}' to '{args.outdir}'...")
    render_pages(pages, output_dir=args.outdir, format_type=args.format, album_title=args.country, server=args.server)
    print("Done!")


if __name__ == "__main__":
    main()

"""Command Line Interface for Albumatic."""

import argparse
import sys
from .models import PageConfig
from .engine import LayoutEngine, PDFRenderer, SVGRenderer
from .parser import parse_legacy_path_and_query


def main():
    parser = argparse.ArgumentParser(description="Albumatic - Stamp Album Page Generator")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start local web server with GUI and REST API")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    # Render command
    render_parser = subparsers.add_parser("render", help="Render PDF or SVG from URL or parameters")
    render_parser.add_argument("--url", help="Stateless URL or path e.g. /pdf/USA/Definitives/2009/1/ABBA-hh-BBB")
    render_parser.add_argument("--template", default="ABBA-hh-BBB", help="Stamp template (e.g. ABBA-hh-BBB)")
    render_parser.add_argument("--country", default="COUNTRY", help="Country title")
    render_parser.add_argument("--area", default="Area", help="Area subtitle")
    render_parser.add_argument("--year", default="YYYY", help="Year")
    render_parser.add_argument("--no", default="1", help="Page number")
    render_parser.add_argument("--format", choices=["pdf", "svg"], default="pdf", help="Output format")
    render_parser.add_argument("-o", "--output", help="Output file path (default: stdout for SVG or page.pdf)")

    args = parser.parse_args()

    if args.command == "serve" or args.command is None:
        import uvicorn
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 8000)
        reload = getattr(args, "reload", False)
        print(f"Starting Albumatic on http://{host}:{port} ...")
        uvicorn.run("albumatic.api:app", host=host, port=port, reload=reload)
    elif args.command == "render":
        if args.url:
            import urllib.parse
            parsed = urllib.parse.urlparse(args.url)
            query_dict = dict(urllib.parse.parse_qsl(parsed.query))
            config = parse_legacy_path_and_query(parsed.path, query_dict)
        else:
            config = PageConfig(
                country=args.country,
                area=args.area,
                year=args.year,
                no=args.no,
                template=args.template,
            )

        layout = LayoutEngine.compute(config)

        if args.format == "pdf":
            out_file = args.output or f"{config.country}_{config.no}.pdf".replace("/", "_")
            pdf_bytes = PDFRenderer.render(layout)
            with open(out_file, "wb") as f:
                f.write(pdf_bytes)
            print(f"Saved PDF to {out_file}")
        elif args.format == "svg":
            svg_content = SVGRenderer.render(layout)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(svg_content)
                print(f"Saved SVG to {args.output}")
            else:
                sys.stdout.write(svg_content)


if __name__ == "__main__":
    main()

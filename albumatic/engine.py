"""Core layout calculation engine, PDF renderer, and SVG generator for Albumatic."""

import io
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
import html

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm, inch, pica

# 1 point in ReportLab coordinate system is 1.0
pt = 1.0

from .models import PageConfig, AlbumConfig, StampItem, UNIT_TO_PT, Unit
from .sizes import get_stamp_dimensions
from .fonts import init_unicode_fonts


@dataclass
class ComputedStamp:
    x_pt: float
    y_pt: float
    width_pt: float
    height_pt: float
    text: Optional[str] = None
    label: Optional[str] = None
    code: str = ""


@dataclass
class ComputedPageLayout:
    # Page dimensions in points (pt)
    page_width_pt: float
    page_height_pt: float
    
    # Margin bounds in points
    left_margin_pt: float
    right_margin_pt: float
    top_margin_pt: float
    bottom_margin_pt: float
    
    # Content area inside margins
    content_width_pt: float
    content_height_pt: float
    
    # Headers & Footers
    header1: str
    header1_y_pt: float
    header2: str
    header2_y_pt: float
    
    left_footer: str
    right_footer: str
    footer_y_pt: float
    
    # Computed stamps with absolute canvas coordinates (ReportLab origin bottom-left)
    stamps: List[ComputedStamp]
    
    # Raw config reference
    config: PageConfig


class LayoutEngine:
    """Calculates geometric layout of stamp album pages."""

    @classmethod
    def compute(cls, config: PageConfig) -> ComputedPageLayout:
        scale = config.get_unit_scale()
        mm_to_pt = UNIT_TO_PT[Unit.MM]

        # Dimension conversions to points
        pw_pt = config.pagewidth * scale
        ph_pt = config.pageheight * scale
        lm_pt = config.leftmargin * scale
        rm_pt = config.rightmargin * scale
        tm_pt = config.topmargin * scale
        bm_pt = config.bottommargin * scale

        content_w_pt = max(10.0, pw_pt - lm_pt - rm_pt)
        content_h_pt = max(10.0, ph_pt - tm_pt - bm_pt)

        # Header positions (measured downwards from top margin)
        h1_offset_pt = config.header1pos * scale
        h2_offset_pt = config.header2pos * scale

        header1_y_pt = ph_pt - tm_pt - h1_offset_pt
        header2_y_pt = ph_pt - tm_pt - h2_offset_pt

        # Footer position (below bottom margin)
        footer_y_pt = bm_pt - (15.0 * pt)

        h1, h2, left_footer, right_footer = config.resolve_headers_and_footers()

        # Printable area available for stamps (below header2)
        stamp_area_top_pt = ph_pt - tm_pt - h2_offset_pt
        stamp_area_bottom_pt = bm_pt
        available_h_pt = max(10.0, stamp_area_top_pt - stamp_area_bottom_pt)

        # Build stamp rows from config (either explicit rows or template string)
        parsed_rows: List[List[StampItem]] = []
        if config.rows:
            parsed_rows = config.rows
        else:
            raw_lines = config.template.split("-") if config.template else []
            for r_idx, line in enumerate(raw_lines):
                row_items: List[StampItem] = []
                for c_idx, char in enumerate(line):
                    w_mm, h_mm = get_stamp_dimensions(char, config.custom_sizes)
                    
                    # Check text and label mappings (1-indexed)
                    key = f"{r_idx + 1}_{c_idx + 1}"
                    txt = config.texts.get(key)
                    lbl = config.labels.get(key)
                    
                    # Handle placeholders
                    if config.placeholders in ("texts", "both") and not txt:
                        txt = f"{r_idx + 1},{c_idx + 1}"
                    if config.placeholders in ("labels", "both") and not lbl:
                        lbl = f"{r_idx + 1},{c_idx + 1}"

                    row_items.append(
                        StampItem(
                            code=char,
                            width_mm=w_mm,
                            height_mm=h_mm,
                            text=txt,
                            label=lbl,
                        )
                    )
                if row_items:
                    parsed_rows.append(row_items)

        nlines = len(parsed_rows)
        computed_stamps: List[ComputedStamp] = []

        if nlines > 0:
            # Calculate line heights in points
            line_heights_pt = []
            for row in parsed_rows:
                max_h = max((s.height_mm or 0.0) for s in row) * mm_to_pt
                line_heights_pt.append(max_h)

            sum_line_h = sum(line_heights_pt)
            free_h = available_h_pt - sum_line_h
            
            # Row spacing
            max_y_dist_pt = config.maxydistance * scale
            if free_h < 0:
                y_distance = 0.0
                top_offset = 0.0
            else:
                y_distance = free_h / (nlines + 1)
                if y_distance > max_y_dist_pt:
                    y_distance = max_y_dist_pt
                top_offset = (free_h - (nlines - 1) * y_distance) / 2.0

            # Current y starts from the top of the stamp area
            current_y = stamp_area_top_pt - top_offset

            max_x_dist_pt = config.maxxdistance * scale

            for r_idx, row in enumerate(parsed_rows):
                current_y -= line_heights_pt[r_idx]
                nstamps = len(row)
                
                # Row stamp widths in points
                stamp_widths_pt = [(s.width_mm or 0.0) * mm_to_pt for s in row]
                sum_w = sum(stamp_widths_pt)
                free_w = content_w_pt - sum_w

                if free_w < 0:
                    x_distance = 0.0
                    left_offset = 0.0
                else:
                    x_distance = free_w / (nstamps + 1)
                    if x_distance > max_x_dist_pt:
                        x_distance = max_x_dist_pt
                    left_offset = (free_w - (nstamps - 1) * x_distance) / 2.0

                current_x = lm_pt + left_offset

                for c_idx, item in enumerate(row):
                    w_pt = (item.width_mm or 0.0) * mm_to_pt
                    h_pt = (item.height_mm or 0.0) * mm_to_pt

                    computed_stamps.append(
                        ComputedStamp(
                            x_pt=current_x,
                            y_pt=current_y,
                            width_pt=w_pt,
                            height_pt=h_pt,
                            text=item.text,
                            label=item.label,
                            code=item.code,
                        )
                    )
                    current_x += w_pt + x_distance

                current_y -= y_distance

        return ComputedPageLayout(
            page_width_pt=pw_pt,
            page_height_pt=ph_pt,
            left_margin_pt=lm_pt,
            right_margin_pt=rm_pt,
            top_margin_pt=tm_pt,
            bottom_margin_pt=bm_pt,
            content_width_pt=content_w_pt,
            content_height_pt=content_h_pt,
            header1=h1,
            header1_y_pt=header1_y_pt,
            header2=h2,
            header2_y_pt=header2_y_pt,
            left_footer=left_footer,
            right_footer=right_footer,
            footer_y_pt=footer_y_pt,
            stamps=computed_stamps,
            config=config,
        )

    @classmethod
    def compute_album(cls, album: AlbumConfig) -> List[ComputedPageLayout]:
        """Computes layouts for all pages in an album."""
        resolved_pages = album.resolve_pages()
        return [cls.compute(p) for p in resolved_pages]


class PDFRenderer:
    """Renders ComputedPageLayout(s) to a ReportLab vector PDF with full Unicode TrueType font support."""

    @classmethod
    def _draw_page(cls, pdf: Canvas, layout: ComputedPageLayout, font_regular: str, font_bold: str):
        # Set page size dynamically for each page in multi-page canvas
        pdf.setPageSize((layout.page_width_pt, layout.page_height_pt))

        # 1. Outer Border
        p = pdf.beginPath()
        p.moveTo(layout.left_margin_pt, layout.bottom_margin_pt)
        p.lineTo(layout.left_margin_pt, layout.page_height_pt - layout.top_margin_pt)
        p.lineTo(layout.page_width_pt - layout.right_margin_pt, layout.page_height_pt - layout.top_margin_pt)
        p.lineTo(layout.page_width_pt - layout.right_margin_pt, layout.bottom_margin_pt)
        p.close()
        pdf.setLineWidth(0.8)
        pdf.drawPath(p)

        # 2. Footers
        pdf.setFont(font_regular, 11)
        pdf.drawString(layout.left_margin_pt, layout.footer_y_pt, layout.left_footer)
        pdf.drawRightString(layout.page_width_pt - layout.right_margin_pt, layout.footer_y_pt, layout.right_footer)

        # 3. Headers (Centered in printable content box)
        center_x = layout.left_margin_pt + (layout.content_width_pt / 2.0)
        if layout.header1:
            pdf.setFont(font_bold, 34)
            pdf.drawCentredString(center_x, layout.header1_y_pt, layout.header1)
        if layout.header2:
            pdf.setFont(font_regular, 18)
            pdf.drawCentredString(center_x, layout.header2_y_pt, layout.header2)

        # 4. Stamp Frames & Texts
        for stamp in layout.stamps:
            # Frame path
            sp = pdf.beginPath()
            sp.moveTo(stamp.x_pt, stamp.y_pt)
            sp.lineTo(stamp.x_pt, stamp.y_pt + stamp.height_pt)
            sp.lineTo(stamp.x_pt + stamp.width_pt, stamp.y_pt + stamp.height_pt)
            sp.lineTo(stamp.x_pt + stamp.width_pt, stamp.y_pt)
            sp.close()
            pdf.setLineWidth(0.5)
            pdf.drawPath(sp)

            # Center text inside mount
            if stamp.text:
                font_size = 8.0
                try:
                    str_w = pdf.stringWidth(stamp.text, font_regular, font_size)
                    avail_w = max(stamp.width_pt - 4.0, 10.0)
                    if str_w > avail_w:
                        font_size = max(4.5, font_size * avail_w / str_w)
                except Exception:
                    pass
                pdf.setFont(font_regular, font_size)
                pdf.drawCentredString(
                    stamp.x_pt + (stamp.width_pt / 2.0),
                    stamp.y_pt + (stamp.height_pt / 2.0) - (font_size * 0.35),
                    stamp.text,
                )

            # Bottom label below mount
            if stamp.label:
                font_size = 8.5
                try:
                    str_w = pdf.stringWidth(stamp.label, font_regular, font_size)
                    avail_w = max(stamp.width_pt + 6.0, 36.0)
                    if str_w > avail_w:
                        font_size = max(5.0, font_size * avail_w / str_w)
                except Exception:
                    pass
                pdf.setFont(font_regular, font_size)
                pdf.drawCentredString(
                    stamp.x_pt + (stamp.width_pt / 2.0),
                    stamp.y_pt - (11.0 * pt),
                    stamp.label,
                )

        pdf.showPage()

    @classmethod
    def render(cls, layout: ComputedPageLayout, output_stream: Optional[io.BytesIO] = None) -> bytes:
        """Renders a single page layout to PDF bytes."""
        font_regular, font_bold = init_unicode_fonts()
        buf = output_stream or io.BytesIO()
        pdf = Canvas(buf, pagesize=(layout.page_width_pt, layout.page_height_pt))
        cls._draw_page(pdf, layout, font_regular, font_bold)
        pdf.save()
        return buf.getvalue()

    @classmethod
    def render_pages(cls, layouts: List[ComputedPageLayout], output_stream: Optional[io.BytesIO] = None) -> bytes:
        """Renders multiple page layouts into a single multi-page combined vector PDF document."""
        if not layouts:
            return b""
        font_regular, font_bold = init_unicode_fonts()
        buf = output_stream or io.BytesIO()
        first = layouts[0]
        pdf = Canvas(buf, pagesize=(first.page_width_pt, first.page_height_pt))
        for layout in layouts:
            cls._draw_page(pdf, layout, font_regular, font_bold)
        pdf.save()
        return buf.getvalue()

    @classmethod
    def render_album(cls, album: AlbumConfig, output_stream: Optional[io.BytesIO] = None) -> bytes:
        """Renders an entire AlbumConfig into a multi-page PDF byte stream."""
        layouts = LayoutEngine.compute_album(album)
        return cls.render_pages(layouts, output_stream)


class SVGRenderer:
    """Renders ComputedPageLayout to an SVG vector string for live web UI preview & vector export."""

    @classmethod
    def render(cls, layout: ComputedPageLayout) -> str:
        w = layout.page_width_pt
        h = layout.page_height_pt

        # SVG coordinate system has (0,0) at top-left, whereas ReportLab PDF has (0,0) at bottom-left.
        # Transformation: svg_y = h - canvas_y
        def to_svg_y(pdf_y: float) -> float:
            return h - pdf_y

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="100%" height="100%" style="background:#ffffff; display:block;">',
            '  <defs>',
            '    <style>',
            '      .border { fill: none; stroke: #222222; stroke-width: 0.8; }',
            '      .stamp-frame { fill: #fdfdfd; stroke: #333333; stroke-width: 0.5; }',
            '      .header1 { font-family: "Liberation Sans", "DejaVu Sans", "Helvetica", Arial, sans-serif; font-size: 34px; font-weight: bold; text-anchor: middle; fill: #111111; }',
            '      .header2 { font-family: "Liberation Sans", "DejaVu Sans", "Helvetica", Arial, sans-serif; font-size: 18px; text-anchor: middle; fill: #333333; }',
            '      .footer { font-family: "Liberation Sans", "DejaVu Sans", "Helvetica", Arial, sans-serif; font-size: 11px; fill: #555555; }',
            '      .stamp-text { font-family: "Liberation Sans", "DejaVu Sans", "Helvetica", Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; fill: #555555; }',
            '      .stamp-label { font-family: "Liberation Sans", "DejaVu Sans", "Helvetica", Arial, sans-serif; text-anchor: middle; fill: #222222; }',
            '    </style>',
            '  </defs>',
        ]

        # 1. Page Margin Border
        bx = layout.left_margin_pt
        by = layout.top_margin_pt
        bw = layout.page_width_pt - layout.left_margin_pt - layout.right_margin_pt
        bh = layout.page_height_pt - layout.top_margin_pt - layout.bottom_margin_pt
        parts.append(f'  <rect class="border" x="{bx:.2f}" y="{by:.2f}" width="{bw:.2f}" height="{bh:.2f}" />')

        # 2. Footers
        fy = to_svg_y(layout.footer_y_pt)
        if layout.left_footer:
            parts.append(f'  <text class="footer" x="{layout.left_margin_pt:.2f}" y="{fy:.2f}">{html.escape(layout.left_footer)}</text>')
        if layout.right_footer:
            parts.append(f'  <text class="footer" x="{(layout.page_width_pt - layout.right_margin_pt):.2f}" y="{fy:.2f}" text-anchor="end">{html.escape(layout.right_footer)}</text>')

        # 3. Headers
        center_x = layout.left_margin_pt + (layout.content_width_pt / 2.0)
        if layout.header1:
            h1_y = to_svg_y(layout.header1_y_pt)
            parts.append(f'  <text class="header1" x="{center_x:.2f}" y="{h1_y:.2f}">{html.escape(layout.header1)}</text>')
        if layout.header2:
            h2_y = to_svg_y(layout.header2_y_pt)
            parts.append(f'  <text class="header2" x="{center_x:.2f}" y="{h2_y:.2f}">{html.escape(layout.header2)}</text>')

        # 4. Stamp Frames & Texts
        for stamp in layout.stamps:
            sx = stamp.x_pt
            sy = to_svg_y(stamp.y_pt + stamp.height_pt)
            sw = stamp.width_pt
            sh = stamp.height_pt

            # Mount rectangle
            parts.append(f'  <g class="stamp-group">')
            parts.append(f'    <rect class="stamp-frame" x="{sx:.2f}" y="{sy:.2f}" width="{sw:.2f}" height="{sh:.2f}" rx="1" />')

            # Stamp inner text
            if stamp.text:
                cx = sx + (sw / 2.0)
                cy = sy + (sh / 2.0)
                est_w = len(stamp.text) * 4.6
                avail_w = max(sw - 4.0, 10.0)
                font_sz = 8.0
                if est_w > avail_w:
                    font_sz = max(4.5, 8.0 * avail_w / est_w)
                parts.append(f'    <text class="stamp-text" style="font-size:{font_sz:.1f}px;" x="{cx:.2f}" y="{cy:.2f}">{html.escape(stamp.text)}</text>')

            # Stamp label below
            if stamp.label:
                lx = sx + (sw / 2.0)
                ly = sy + sh + 11.0
                est_w = len(stamp.label) * 4.9
                avail_w = max(sw + 6.0, 36.0)
                font_sz = 8.5
                if est_w > avail_w:
                    font_sz = max(5.0, 8.5 * avail_w / est_w)
                parts.append(f'    <text class="stamp-label" style="font-size:{font_sz:.1f}px;" x="{lx:.2f}" y="{ly:.2f}">{html.escape(stamp.label)}</text>')

            parts.append(f'  </g>')

        parts.append('</svg>')
        return "\n".join(parts)

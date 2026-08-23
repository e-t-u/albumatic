import pytest
from albumatic.models import PageConfig, AlbumConfig, Unit
from albumatic.engine import LayoutEngine, PDFRenderer, SVGRenderer


def test_layout_computation_basic():
    config = PageConfig(
        country="USA",
        area="Definitives",
        year="2009",
        no="1",
        template="ABBA-hh-BBB",
        texts={"1_1": "10c", "1_2": "20c"},
        labels={"1_1": "Washington", "1_2": "Lincoln"},
    )
    layout = LayoutEngine.compute(config)
    
    assert layout.page_width_pt > 0
    assert layout.page_height_pt > 0
    assert layout.header1 == "USA"
    assert layout.header2 == "Definitives"
    assert len(layout.stamps) == 9  # 4 + 2 + 3
    assert layout.stamps[0].text == "10c"
    assert layout.stamps[0].label == "Washington"


def test_unicode_pdf_and_svg_rendering():
    """Verify full international Unicode character support in PDF and SVG including Chinese, Arabic & Nordic ÅÄÖ."""
    config = PageConfig(
        country="Suomi — Finland (Åland & Häme)",
        area="1889 Vaakuna & 大清邮政 / البريد المصري — Cliché brût (½ Mk) €100 ★",
        year="1889",
        no="1",
        template="AA-BB",
        texts={"1_1": "5 penniä (vihreä)", "1_2": "١ قرش / 壹分银"},
        labels={"1_1": "Östermyra & Ähtäri (Åbo)", "1_2": "Saimaan höyrylaiva & القاهرة"},
    )
    layout = LayoutEngine.compute(config)

    # 1. Test PDF rendering with Unicode TTFont
    pdf_bytes = PDFRenderer.render(layout)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF")

    # 2. Test SVG vector generation
    svg_str = SVGRenderer.render(layout)
    assert "Åland" in svg_str
    assert "Häme" in svg_str
    assert "Östermyra" in svg_str
    assert "Ähtäri" in svg_str
    assert "penniä" in svg_str
    assert "vihreä" in svg_str
    assert "höyrylaiva" in svg_str
    assert "大清邮政" in svg_str
    assert "البريد المصري" in svg_str
    assert "cliché" in svg_str.lower()
    assert "القاهرة" in svg_str


def test_multi_page_album_rendering():
    """Verify multi-page combined PDF generation with 30 pages."""
    pages = []
    for i in range(1, 31):
        pages.append(
            PageConfig(
                country="Nepal",
                area=f"Issue Series {i}",
                year="1881",
                no=str(i),
                template="XXX-XXX",
                texts={"1_1": f"Stamp {i}"},
                labels={"1_1": f"Label {i}"},
            )
        )
    
    album = AlbumConfig(
        country="Nepal",
        pages=pages,
    )
    pdf_bytes = PDFRenderer.render_album(album)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_footer_year_resolution():
    config = PageConfig(
        country="Finland",
        area="Coat of Arms",
        year="1889",
        no="4",
        template="A",
    )
    h1, h2, lf, rf = config.resolve_headers_and_footers()
    assert rf == "1889/4"
    assert lf == "Albumatic"

    layout = LayoutEngine.compute(config)
    assert layout.right_footer == "1889/4"


def test_letter_paper_layout():
    config = PageConfig(
        country="USA",
        year="2009",
        no="1",
        unit=Unit.INCH,
        pagewidth=8.5,
        pageheight=11.0,
        topmargin=0.5,
        bottommargin=0.75,
        leftmargin=0.6,
        rightmargin=0.6,
        template="ABBA-hh",
    )
    layout = LayoutEngine.compute(config)
    assert layout.page_width_pt == 8.5 * 72.0
    assert layout.page_height_pt == 11.0 * 72.0
    assert len(layout.stamps) == 6
    assert layout.stamps[0].x_pt > layout.left_margin_pt


def test_stamp_inner_text_splitting_and_fitting():
    from albumatic.engine import split_stamp_text_lines
    assert split_stamp_text_lines("5 kop. sininen", max_chars_per_line=8) == ["5 kop.", "sininen"]
    assert split_stamp_text_lines("壹分银 (1 Candarin)", max_chars_per_line=8) == ["壹分银", "(1 Candarin)"]
    assert split_stamp_text_lines("harmaa/ruusu", max_chars_per_line=8) == ["harmaa", "/ruusu"]
    assert split_stamp_text_lines("10c", max_chars_per_line=8) == ["10c"]
    assert split_stamp_text_lines("1 mk\\nharmaa/ruusu") == ["1 mk", "harmaa/ruusu"]
    assert split_stamp_text_lines("1 mk /n harmaa/ruusu") == ["1 mk", "harmaa/ruusu"]
    assert split_stamp_text_lines("1 mk<br>harmaa/ruusu") == ["1 mk", "harmaa/ruusu"]
    assert split_stamp_text_lines("1 mk\nharmaa/ruusu") == ["1 mk", "harmaa/ruusu"]

    config = PageConfig(
        country="USA",
        year="1934",
        no="1",
        template="AAA",
        texts={"1_1": "1¢ green Yosemite", "1_2": "2¢ red orange", "1_3": "6¢ blue"},
        labels={"1_1": "Yosemite\\n(El Capitan)", "1_2": "Grand Canyon /n National Park", "1_3": "Crater Lake"}
    )
    layout = LayoutEngine.compute(config)
    pdf_bytes = PDFRenderer.render(layout)
    assert len(pdf_bytes) > 0
    svg_str = SVGRenderer.render(layout)
    assert "Yosemite" in svg_str
    assert "(El Capitan)" in svg_str
    assert "Grand Canyon" in svg_str
    assert "National Park" in svg_str


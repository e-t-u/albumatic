"""Pydantic data models for Albumatic stamp layout engine."""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class Unit(str, Enum):
    MM = "mm"
    INCH = "in"
    PICA = "pica"
    PT = "pt"


# Unit conversion factors to Points (pt) for ReportLab vector coordinates (72 pt = 1 inch)
# 1 mm = 72 / 25.4 pt = 2.834645669291339 pt
UNIT_TO_PT: Dict[Unit, float] = {
    Unit.PT: 1.0,
    Unit.MM: 72.0 / 25.4,
    Unit.INCH: 72.0,
    Unit.PICA: 12.0,
}

# Standard Page Dimensions in mm (width, height)
PAGE_SIZES_MM: Dict[str, Tuple[float, float]] = {
    "A4": (210.0, 297.0),
    "Letter": (215.9, 279.4),
    "A3": (297.0, 420.0),
    "Legal": (215.9, 355.6),
}


class StampItem(BaseModel):
    """Represents a single stamp in a row."""
    code: str = Field(..., description="Stamp size letter (e.g. 'A', 'd', 'X')")
    width_mm: Optional[float] = Field(None, description="Explicit width in mm (overrides code lookup)")
    height_mm: Optional[float] = Field(None, description="Explicit height in mm (overrides code lookup)")
    text: Optional[str] = Field(None, description="Centered text inside the stamp mount frame")
    label: Optional[str] = Field(None, description="Label below the stamp mount frame")


class PageConfig(BaseModel):
    """Declarative configuration model for a single album page."""
    # Metadata and Headers
    country: str = Field(default="COUNTRY", description="Header 1 title (e.g. 'USA', 'Nepal')")
    area: str = Field(default="Area", description="Header 2 subtitle (e.g. 'Definitives', 'Airmail')")
    year: str = Field(default="YYYY", description="Right footer year")
    no: str = Field(default="#", description="Right footer page number")
    
    # Custom Headers / Footers overrides
    header1: Optional[str] = Field(None, description="Override for Header 1 (defaults to country)")
    header2: Optional[str] = Field(None, description="Override for Header 2 (defaults to area)")
    leftfooter: Optional[str] = Field(None, description="Left footer logo text (defaults to logotext/Albumatic)")
    rightfooter: Optional[str] = Field(None, description="Right footer text (defaults to 'year/no')")
    logotext: str = Field(default="Albumatic", description="Default logo text for left footer")
    
    # Template and Structured Rows
    template: str = Field(default="X", description="Dash-separated row template string (e.g. 'ABBA-hh-BBB')")
    rows: Optional[List[List[StampItem]]] = Field(None, description="Explicit structured rows with individual stamp overrides")
    
    # Per-stamp coordinates mappings (1-indexed row_col, e.g. {"1_1": "Blue", "1_2": "Red"})
    texts: Dict[str, str] = Field(default_factory=dict, description="Inner stamp texts mapped by 'row_col'")
    labels: Dict[str, str] = Field(default_factory=dict, description="Below stamp labels mapped by 'row_col'")
    placeholders: Optional[str] = Field(None, description="Placeholder mode: 'texts', 'labels', or 'both'")

    # Unit & Page Dimensions
    unit: Unit = Field(default=Unit.MM, description="Measurement unit for dimensions")
    pagewidth: float = Field(default=210.0, description="Page width in current units (default A4 = 210mm)")
    pageheight: float = Field(default=297.0, description="Page height in current units (default A4 = 297mm)")

    # Margins and Header Positions
    topmargin: float = Field(default=12.0, description="Top margin border distance")
    bottommargin: float = Field(default=18.0, description="Bottom margin border distance")
    leftmargin: float = Field(default=15.0, description="Left margin border distance")
    rightmargin: float = Field(default=15.0, description="Right margin border distance")
    header1pos: float = Field(default=25.0, description="Header 1 distance from top border")
    header2pos: float = Field(default=35.0, description="Header 2 distance from top border")

    # Spacing Bounds
    maxxdistance: float = Field(default=15.0, description="Maximum horizontal distance between stamps")
    maxydistance: float = Field(default=25.0, description="Maximum vertical distance between stamp rows")

    # Custom Size Overrides: letter -> (width_mm, height_mm)
    custom_sizes: Dict[str, Tuple[float, float]] = Field(default_factory=dict, description="Custom mount sizes override")

    def get_unit_scale(self) -> float:
        """Return scale factor from model's unit to points (pt)."""
        return UNIT_TO_PT.get(self.unit, UNIT_TO_PT[Unit.MM])

    def resolve_headers_and_footers(self) -> Tuple[str, str, str, str]:
        """Resolves (header1, header2, leftfooter, rightfooter)."""
        h1 = self.header1 if (self.header1 is not None and self.header1 != "") else self.country
        h2 = self.header2 if (self.header2 is not None and self.header2 != "") else self.area
        lf = self.leftfooter if (self.leftfooter is not None and self.leftfooter != "") else self.logotext
        
        if self.rightfooter is not None and self.rightfooter != "":
            rf = self.rightfooter
        else:
            y = self.year or ""
            n = self.no or ""
            if y and n:
                rf = f"{y}/{n}"
            elif y:
                rf = y
            elif n:
                rf = n
            else:
                rf = ""
        return h1, h2, lf, rf


class AlbumConfig(BaseModel):
    """Configuration model for a full multi-page album with inherited defaults."""
    country: str = Field(default="COUNTRY", description="Default Country / Header 1 for all pages")
    area: Optional[str] = Field(default="Area", description="Default Area / Header 2 for all pages")
    year: Optional[str] = Field(default="YYYY", description="Default Year")
    logotext: str = Field(default="Albumatic", description="Default footer logo text")
    
    # Common Geometry Defaults
    unit: Unit = Field(default=Unit.MM, description="Measurement unit")
    pagewidth: float = Field(default=210.0, description="Page width in current units")
    pageheight: float = Field(default=297.0, description="Page height in current units")
    topmargin: float = Field(default=12.0, description="Top margin")
    bottommargin: float = Field(default=18.0, description="Bottom margin")
    leftmargin: float = Field(default=15.0, description="Left margin")
    rightmargin: float = Field(default=15.0, description="Right margin")
    header1pos: float = Field(default=25.0, description="Header 1 position")
    header2pos: float = Field(default=35.0, description="Header 2 position")
    maxxdistance: float = Field(default=15.0, description="Max X distance")
    maxydistance: float = Field(default=25.0, description="Max Y distance")

    # List of album pages
    pages: List[PageConfig] = Field(default_factory=list, description="Pages belonging to this album")

    def resolve_pages(self) -> List[PageConfig]:
        """Resolves child pages, propagating album-level defaults where child values are default/empty."""
        resolved: List[PageConfig] = []
        for idx, page in enumerate(self.pages):
            p_data = page.model_dump()
            
            # Inherit country if default
            if p_data.get("country") in ("COUNTRY", "", None) and self.country:
                p_data["country"] = self.country
            if p_data.get("area") in ("Area", "", None) and self.area:
                p_data["area"] = self.area
            if p_data.get("year") in ("YYYY", "", None) and self.year:
                p_data["year"] = self.year
            if not p_data.get("no") or p_data.get("no") == "#":
                p_data["no"] = str(idx + 1)
            if p_data.get("logotext") == "Albumatic" and self.logotext:
                p_data["logotext"] = self.logotext

            # Geometry inheritance
            p_data["unit"] = self.unit
            p_data["pagewidth"] = self.pagewidth
            p_data["pageheight"] = self.pageheight
            p_data["topmargin"] = self.topmargin
            p_data["bottommargin"] = self.bottommargin
            p_data["leftmargin"] = self.leftmargin
            p_data["rightmargin"] = self.rightmargin
            p_data["header1pos"] = self.header1pos
            p_data["header2pos"] = self.header2pos
            p_data["maxxdistance"] = self.maxxdistance
            p_data["maxydistance"] = self.maxydistance

            resolved.append(PageConfig(**p_data))
        return resolved


class BatchImportRequest(BaseModel):
    """Payload for parsing raw batch text into PageConfig models."""
    text: str = Field(..., description="Multi-line or slash-separated templates notation")
    country: Optional[str] = Field("COUNTRY", description="Default Country")
    area: Optional[str] = Field("Area", description="Default Area")
    year: Optional[str] = Field("YYYY", description="Default Year")
    unit: Unit = Field(default=Unit.MM, description="Default Unit")

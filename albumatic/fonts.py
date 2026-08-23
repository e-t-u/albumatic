"""Unicode font registration and management for ReportLab vector PDF rendering."""

import os
from typing import Optional, Tuple
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registered font names
UNICODE_REGULAR_FONT = "AlbumaticSans"
UNICODE_BOLD_FONT = "AlbumaticSans-Bold"

_FONTS_INITIALIZED = False


def _find_system_fonts() -> Tuple[Optional[str], Optional[str]]:
    """Locate full-coverage Unicode TrueType fonts on the host system."""
    regular_candidates = [
        # Linux standard TrueType fonts (clean vector PDF typography & unicode support)
        "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/gnu-free/FreeSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
        "/usr/share/fonts/google-noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/open-sans/OpenSans-Regular.ttf",
        "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
        "/usr/share/fonts/google-droid-sans-fonts/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/google-noto/NotoSansCJK-Regular.ttc",
        # macOS paths
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows paths
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf",
    ]

    bold_candidates = [
        # Linux standard paths
        "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf",
        "/usr/share/fonts/gnu-free/FreeSansBold.ttf",
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/open-sans/OpenSans-Bold.ttf",
        # macOS paths
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        # Windows paths
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf",
    ]

    regular_path = next((p for p in regular_candidates if os.path.isfile(p)), None)
    bold_path = next((p for p in bold_candidates if os.path.isfile(p)), None)

    return regular_path, bold_path


def init_unicode_fonts() -> Tuple[str, str]:
    """Registers Unicode TrueType fonts with ReportLab.
    Returns (regular_font_name, bold_font_name).
    """
    global _FONTS_INITIALIZED
    if _FONTS_INITIALIZED:
        return UNICODE_REGULAR_FONT, UNICODE_BOLD_FONT

    reg_path, bold_path = _find_system_fonts()

    if reg_path:
        try:
            pdfmetrics.registerFont(TTFont(UNICODE_REGULAR_FONT, reg_path))
            if bold_path:
                pdfmetrics.registerFont(TTFont(UNICODE_BOLD_FONT, bold_path))
            else:
                pdfmetrics.registerFont(TTFont(UNICODE_BOLD_FONT, reg_path))
            _FONTS_INITIALIZED = True
            return UNICODE_REGULAR_FONT, UNICODE_BOLD_FONT
        except Exception:
            pass

    # Fallback to standard core PostScript font if no TTF found
    _FONTS_INITIALIZED = True
    return "Helvetica", "Helvetica-Bold"

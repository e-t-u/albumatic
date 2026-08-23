"""Standard stamp mount size catalog for Hawid / Leuchtturm mounts."""

from typing import Dict, Tuple, Any

# Built-in standard sizes in millimeters: letter -> (width_mm, height_mm)
# Uppercase = Portrait / Square mounts
# Lowercase = Landscape mounts
STANDARD_STAMP_SIZES: Dict[str, Tuple[float, float]] = {
    "A": (20.0, 24.0),
    "B": (20.0, 26.0),
    "C": (21.0, 24.0),
    "D": (21.5, 26.0),
    "E": (21.5, 30.0),
    "F": (23.0, 27.5),
    "G": (24.0, 29.0),
    "H": (24.0, 40.0),
    "I": (24.0, 41.0),
    "J": (25.0, 30.0),
    "K": (25.0, 36.0),
    "L": (26.0, 31.0),
    "M": (26.0, 36.0),
    "N": (26.0, 40.0),
    "O": (26.0, 41.0),
    "P": (26.0, 43.0),
    "Q": (27.5, 33.0),
    "R": (28.0, 34.0),
    "S": (28.0, 39.0),
    "T": (29.0, 36.0),
    "U": (30.0, 39.0),
    "V": (30.0, 41.0),
    "W": (33.0, 55.0),
    "X": (35.0, 35.0),
    "Y": (41.0, 41.0),
    "Z": (41.0, 53.0),
    "a": (24.0, 21.0),
    "b": (26.0, 21.5),
    "c": (29.0, 24.0),
    "d": (31.0, 24.0),
    "e": (31.0, 26.0),
    "f": (33.0, 27.5),
    "g": (34.0, 28.0),
    "h": (36.0, 25.0),
    "i": (36.0, 26.0),
    "j": (36.0, 29.0),
    "k": (39.0, 28.0),
    "l": (39.0, 30.0),
    "m": (40.0, 24.0),
    "n": (40.0, 26.0),
    "o": (40.0, 33.0),
    "p": (41.0, 24.0),
    "q": (41.0, 26.0),
    "r": (41.0, 30.0),
    "s": (43.0, 26.0),
    "t": (46.0, 27.5),
    "u": (53.0, 41.0),
    "v": (55.0, 33.0),
}


def get_stamp_dimensions(code: str, custom_sizes: Dict[str, Tuple[float, float]] | None = None) -> Tuple[float, float]:
    """Retrieve the width and height (in mm) for a stamp code letter."""
    if custom_sizes and code in custom_sizes:
        return custom_sizes[code]
    if code in STANDARD_STAMP_SIZES:
        return STANDARD_STAMP_SIZES[code]
    # Default fallback dimension (e.g. 25x30mm) if unknown
    return (25.0, 30.0)


def get_detailed_stamp_catalog() -> Dict[str, Dict[str, Any]]:
    """Returns catalog with both millimeter and inch dimensions for each mount size."""
    catalog = {}
    for code, (w_mm, h_mm) in STANDARD_STAMP_SIZES.items():
        w_in = round(w_mm / 25.4, 2)
        h_in = round(h_mm / 25.4, 2)
        catalog[code] = {
            "code": code,
            "width_mm": w_mm,
            "height_mm": h_mm,
            "width_in": w_in,
            "height_in": h_in,
            "formatted_mm": f"{w_mm:g}×{h_mm:g} mm",
            "formatted_in": f'{w_in:g}"×{h_in:g}" ({w_in:g}×{h_in:g} in)',
            "formatted_both": f"{w_mm:g}×{h_mm:g} mm / {w_in:g}×{h_in:g} in",
            "orientation": "portrait" if code.isupper() else "landscape",
        }
    return catalog

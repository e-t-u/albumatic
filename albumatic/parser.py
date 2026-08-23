"""Parser and serializer for Albumatic stateless URLs, query strings, and batch notations."""

import urllib.parse
from typing import Any, Dict, List, Optional, Tuple
from .models import PageConfig, Unit


def parse_legacy_path_and_query(path: str, query_params: Dict[str, Any]) -> PageConfig:
    """Parse legacy URL path and query parameters into a PageConfig model.
    
    Path formats supported:
    - /pdf/<country>/<area>/<year>/<no>/<template>[/<filename.pdf>]
    - /pdf/<template>[/<filename.pdf>]
    - /pdf?template=...
    """
    config_dict: Dict[str, Any] = {}
    
    # Strip leading/trailing slashes and split path
    clean_path = path.strip("/")
    raw_parts = clean_path.split("/") if clean_path else []
    parts = [urllib.parse.unquote(p) for p in raw_parts if p]

    # If first component is 'pdf', process subsequent segments
    if parts and parts[0] == "pdf":
        parts = parts[1:]

    # If trailing component is a filename ending in .pdf, remove or inspect it
    if parts and parts[-1].endswith(".pdf") and len(parts) > 1:
        parts.pop()
    elif parts and parts[-1].endswith(".pdf") and len(parts) == 1:
        parts[0] = parts[0][:-4]

    # Map positional URL path parameters
    if len(parts) == 1 and ("-" in parts[0] or parts[0].isalpha()):
        # Single-parameter shorthand e.g. /pdf/ABBA-hh-BBB
        config_dict["template"] = parts[0]
    else:
        field_order = ["country", "area", "year", "no", "template"]
        for i, val in enumerate(parts[:5]):
            if val and val != "-":
                config_dict[field_order[i]] = val

    # Process query parameters
    texts: Dict[str, str] = {}
    labels: Dict[str, str] = {}
    custom_sizes: Dict[str, Tuple[float, float]] = {}

    for k, v in query_params.items():
        if v is None:
            continue
        val_str = str(v)

        if k.startswith("t_"):
            # Inner text: t_row_col
            coord = k[2:]
            texts[coord] = urllib.parse.unquote(val_str)
        elif k.startswith("l_"):
            # Below label: l_row_col
            coord = k[2:]
            labels[coord] = urllib.parse.unquote(val_str)
        elif k.startswith("size_") or k.startswith("s_"):
            # Custom mount dimension override: size_X=100,50 or s_X=100,50
            code = k[5:] if k.startswith("size_") else k[2:]
            try:
                w_str, h_str = val_str.split(",")
                custom_sizes[code] = (float(w_str), float(h_str))
            except Exception:
                pass
        elif k in (
            "pagewidth", "pageheight", "topmargin", "bottommargin",
            "leftmargin", "rightmargin", "header1pos", "header2pos",
            "maxxdistance", "maxydistance"
        ):
            try:
                config_dict[k] = float(val_str)
            except Exception:
                pass
        elif k == "unit":
            try:
                config_dict["unit"] = Unit(val_str.lower())
            except Exception:
                pass
        elif k in ("template", "country", "area", "year", "no", "header1", "header2", "leftfooter", "rightfooter", "logotext", "placeholders"):
            config_dict[k] = val_str
        else:
            config_dict[k] = val_str

    if texts:
        config_dict["texts"] = texts
    if labels:
        config_dict["labels"] = labels
    if custom_sizes:
        config_dict["custom_sizes"] = custom_sizes

    return PageConfig(**config_dict)


def serialize_to_url(config: PageConfig, base_url: str = "/pdf") -> str:
    """Serializes a PageConfig into a reproducible stateless URL."""
    country = urllib.parse.quote(config.country or "-", safe="")
    area = urllib.parse.quote(config.area or "-", safe="")
    year = urllib.parse.quote(config.year or "-", safe="")
    no = urllib.parse.quote(config.no or "-", safe="")
    template = urllib.parse.quote(config.template or "-", safe="")

    path = f"{base_url.rstrip('/')}/{country}/{area}/{year}/{no}/{template}"
    
    query_parts: List[str] = []
    
    # Unit & dimensions if non-default
    if config.unit != Unit.MM:
        query_parts.append(f"unit={config.unit.value}")
    if config.pagewidth != 210.0:
        query_parts.append(f"pagewidth={config.pagewidth}")
    if config.pageheight != 297.0:
        query_parts.append(f"pageheight={config.pageheight}")
    if config.topmargin != 12.0:
        query_parts.append(f"topmargin={config.topmargin}")
    if config.bottommargin != 18.0:
        query_parts.append(f"bottommargin={config.bottommargin}")
    if config.leftmargin != 15.0:
        query_parts.append(f"leftmargin={config.leftmargin}")
    if config.rightmargin != 15.0:
        query_parts.append(f"rightmargin={config.rightmargin}")
    if config.header1pos != 25.0:
        query_parts.append(f"header1pos={config.header1pos}")
    if config.header2pos != 35.0:
        query_parts.append(f"header2pos={config.header2pos}")
    if config.maxxdistance != 15.0:
        query_parts.append(f"maxxdistance={config.maxxdistance}")
    if config.maxydistance != 25.0:
        query_parts.append(f"maxydistance={config.maxydistance}")
    if config.logotext != "Albumatic":
        query_parts.append(f"logotext={urllib.parse.quote(config.logotext, safe='')}")
    if config.placeholders and config.placeholders != "none":
        query_parts.append(f"placeholders={config.placeholders}")

    # Custom sizes
    for code, (w, h) in config.custom_sizes.items():
        query_parts.append(f"size_{code}={w},{h}")

    # Texts and labels
    for coord, txt in sorted(config.texts.items()):
        query_parts.append(f"t_{coord}={urllib.parse.quote(txt, safe='')}")
    for coord, lbl in sorted(config.labels.items()):
        query_parts.append(f"l_{coord}={urllib.parse.quote(lbl, safe='')}")

    if query_parts:
        return f"{path}?{'&'.join(query_parts)}"
    return path


def parse_batch_notation(text: str, base_config: Optional[PageConfig] = None) -> List[PageConfig]:
    """Parses multi-line or slash-separated batch notation into a list of PageConfig instances.
    
    Supported formats per line or entry:
    1. Pure template notation: `AA-BB-CC` or `AA-BB-CC/cc-ddd-a/XXXX`
    2. Pipe-delimited enriched record: `Year | Page# | Area | Template | t:1_1=blue | l:1_1=1A`
    3. Full or relative URLs: `/pdf/USA/Definitives/2009/1/ABBA-hh-BBB?t_1_1=...`
    """
    default_cfg = base_config or PageConfig()
    pages: List[PageConfig] = []

    # If the text contains slashes between templates and no newlines, split by slash
    raw_entries = []
    lines = [line.strip() for line in text.strip().splitlines() if line.strip() and not line.strip().startswith("#")]
    
    if len(lines) == 1 and "/" in lines[0] and not lines[0].startswith("http") and not lines[0].startswith("/pdf"):
        raw_entries = [e.strip() for e in lines[0].split("/") if e.strip()]
    else:
        raw_entries = lines

    for idx, entry in enumerate(raw_entries):
        # 1. Check if it's a URL
        if entry.startswith("http://") or entry.startswith("https://") or entry.startswith("/pdf"):
            parsed = urllib.parse.urlparse(entry)
            q_dict = dict(urllib.parse.parse_qsl(parsed.query))
            p = parse_legacy_path_and_query(parsed.path, q_dict)
            pages.append(p)
            continue

        # 2. Check if pipe-delimited enriched format
        if "|" in entry:
            parts = [p.strip() for p in entry.split("|")]
            # Format: Year | PageNo | Area | Template | [Texts] | [Labels]
            p_data = default_cfg.model_dump()
            if len(parts) >= 1 and parts[0]:
                p_data["year"] = parts[0]
            if len(parts) >= 2 and parts[1]:
                p_data["no"] = parts[1]
            else:
                p_data["no"] = str(idx + 1)
            if len(parts) >= 3 and parts[2]:
                p_data["area"] = parts[2]
            if len(parts) >= 4 and parts[3]:
                p_data["template"] = parts[3]

            texts = dict(p_data.get("texts", {}))
            labels = dict(p_data.get("labels", {}))

            for extra in parts[4:]:
                if extra.startswith("t:"):
                    # t:1_1=blue,1_2=red
                    pairs = extra[2:].split(",")
                    for pair in pairs:
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            texts[k.strip()] = v.strip()
                elif extra.startswith("l:"):
                    # l:1_1=1A,1_2=2A
                    pairs = extra[2:].split(",")
                    for pair in pairs:
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            labels[k.strip()] = v.strip()
                elif extra.startswith("s:") or extra.startswith("size:"):
                    # Supports s:X=45,30,Z=60,40 or s:X=45x30,Z=60x40 or semicolon-delimited
                    import re
                    matches = re.findall(r"([A-Za-z0-9_]+)=([0-9.]+)[,x/]([0-9.]+)", extra)
                    custom_sizes = dict(p_data.get("custom_sizes", {}))
                    for code, w_str, h_str in matches:
                        try:
                            custom_sizes[code] = (float(w_str), float(h_str))
                        except Exception:
                            pass
                    p_data["custom_sizes"] = custom_sizes

            p_data["texts"] = texts
            p_data["labels"] = labels
            pages.append(PageConfig(**p_data))
            continue

        # 3. Standard template string: e.g. "AA-BB-CC"
        p_data = default_cfg.model_dump()
        p_data["template"] = entry
        p_data["no"] = str(idx + 1)
        p_data["texts"] = {}
        p_data["labels"] = {}
        pages.append(PageConfig(**p_data))

    return pages


def serialize_batch_notation(pages: List[PageConfig]) -> str:
    """Serializes a list of PageConfig objects into a clean multi-line batch notation."""
    lines = []
    lines.append("# Albumatic Batch Notation (Year | Page# | Area / Subtitle | Template | Texts | Labels | Custom Sizes)")
    for page in pages:
        parts = [
            page.year or "",
            page.no or "",
            page.area or "",
            page.template or "",
        ]
        if page.texts:
            t_str = "t:" + ",".join(f"{k}={v}" for k, v in sorted(page.texts.items()))
            parts.append(t_str)
        if page.labels:
            l_str = "l:" + ",".join(f"{k}={v}" for k, v in sorted(page.labels.items()))
            parts.append(l_str)
        if page.custom_sizes:
            s_str = "s:" + ",".join(f"{k}={v[0]},{v[1]}" for k, v in sorted(page.custom_sizes.items()))
            parts.append(s_str)
        lines.append(" | ".join(parts))
    return "\n".join(lines)

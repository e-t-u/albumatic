# -*- coding: UTF-8 -*-
"""Client SDK for Albumatic stateless stamp album generator service."""

import os
import urllib.parse
import urllib.request
import urllib.error
from typing import Optional

try:
    from albumatic.parser import parse_legacy_path_and_query
    from albumatic.engine import LayoutEngine, PDFRenderer, SVGRenderer
    HAS_LOCAL_ENGINE = True
except ImportError:
    HAS_LOCAL_ENGINE = False

pathattrs = ("country", "area", "year", "no", "template", "filename")


class Albumatic:
    """Represents a connection or local instance for Albumatic generation.
    Configuration attributes are stacked so you can push defaults and pop them.
    """
    def __init__(self, host="localhost:8000", verbose=False, scheme="http", local_fallback=True):
        self.verbose = verbose
        self.host = host
        self.scheme = scheme
        self.local_fallback = local_fallback
        self.stack = [{}]

    def __setitem__(self, attr, val):
        self.stack[-1][attr] = str(val)

    def __getitem__(self, attr):
        for d in reversed(self.stack):
            if attr in d:
                return d[attr]
        return None

    def __delitem__(self, attr):
        del self.stack[-1][attr]

    def attrpush(self):
        self.stack.append({})

    def attrpop(self):
        self.stack.pop()

    def __iter__(self):
        attrlist = []
        for d in reversed(self.stack):
            for attr in d.keys():
                if attr in pathattrs:
                    continue
                if attr not in attrlist:
                    yield attr
                    attrlist.append(attr)

    def url(self):
        url = f"{self.scheme}://{self.host}/pdf"
        for attr in pathattrs:
            if self[attr]:
                url += "/" + urllib.parse.quote(self[attr])
            else:
                url += "/"
        attrlist = []
        for attr in self:
            attrlist.append(f"{urllib.parse.quote(attr)}={urllib.parse.quote(self[attr])}")
        attrstr = "&".join(attrlist)
        if attrstr:
            url += "?" + attrstr
        return url

    def render_local(self) -> bytes:
        """Renders PDF in-memory using local Python engine."""
        if not HAS_LOCAL_ENGINE:
            raise RuntimeError("Local Albumatic engine is not installed.")
        
        path_str = "/pdf"
        for attr in ("country", "area", "year", "no", "template"):
            val = self[attr]
            path_str += f"/{val}" if val else "/"
        
        query_dict = {attr: self[attr] for attr in self}
        config = parse_legacy_path_and_query(path_str, query_dict)
        layout = LayoutEngine.compute(config)
        return PDFRenderer.render(layout)

    def getpdf(self) -> bytes:
        req_url = self.url()
        try:
            req = urllib.request.Request(req_url, headers={"User-Agent": "pyalbumatic/6.0"})
            with urllib.request.urlopen(req, timeout=3) as f:
                content = f.read()
                if self.verbose:
                    print(f"Retrieved {len(content)} bytes from {req_url}")
                return content
        except Exception as e:
            if self.local_fallback and HAS_LOCAL_ENGINE:
                if self.verbose:
                    print(f"Web request to {req_url} failed ({e}), falling back to local engine...")
                return self.render_local()
            if self.verbose:
                print(f"Failed to fetch {req_url}: {e}")
            return b""

    def writefile(self, file=None):
        filename = file or self["filename"]
        if not filename:
            raise IOError("No filename specified")
        pdf_data = self.getpdf()
        if not pdf_data:
            raise IOError(f"Could not retrieve PDF data for {filename}")
        with open(filename, "wb") as f:
            f.write(pdf_data)
        if self.verbose:
            print(f"Wrote {filename}")

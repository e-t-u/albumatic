#!/usr/bin/env python3
"""Program to generate URLs to print standard stamp sizes catalog."""

def atov():
    for c in range(0, 22):
        yield chr(ord('a') + c)

def AtoZ():
    for c in range(0, 26):
        yield chr(ord('A') + c)

def build_url(urlbase: str, rows: tuple, genfunc) -> str:
    gen = genfunc()
    rowtemplates = []
    texts = []
    try:
        for row in range(len(rows)):
            rowtemplate = ""
            for col in range(rows[row]):
                ch = next(gen)
                rowtemplate += ch
                texts.append(f"t_{row + 1}_{col + 1}={ch}")
            rowtemplates.append(rowtemplate)
    except StopIteration:
        pass
    
    url = f"{urlbase}?template={'-'.join(rowtemplates)}&{'&'.join(texts)}"
    return url

if __name__ == "__main__":
    landscape_rows = (5, 4, 4, 4, 3, 2)
    landscape_base = "http://localhost:8000/pdf/Sizes/Landscape///landscape.pdf"
    print("Landscape sizes URL:")
    print(build_url(landscape_base, landscape_rows, atov))

    portrait_rows = (7, 6, 5, 4, 4)
    portrait_base = "http://localhost:8000/pdf/Sizes/Portrait///portrait.pdf"
    print("\nPortrait sizes URL:")
    print(build_url(portrait_base, portrait_rows, AtoZ))

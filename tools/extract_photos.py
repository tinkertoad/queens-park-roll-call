"""Pull member headshots out of the Legislature's "MPP List" PDF into photos/.

The PDF is not in this repo. Usage:
    pip install pymupdf pillow
    python tools/extract_photos.py "MPP List- September 2026.pdf"

The PDF lays members out nine to a page (three rows of three), alphabetical by
riding, which is the order of data/mpps.json. Photos are matched to members by
that position, so check the output by eye if the PDF layout ever changes.
"""
import io, json, sys
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
members = json.loads((ROOT / "data/mpps.json").read_text())
doc = fitz.open(sys.argv[1])

images = []
for pn in range(1, len(doc)):  # page 1 is the title page
    # photos are the only images bigger than 60pt; the rest are dashed-border pieces
    big = [i for i in doc[pn].get_image_info(xrefs=True)
           if i["bbox"][2] - i["bbox"][0] > 60 and i["bbox"][3] - i["bbox"][1] > 60]
    row = lambda y: 0 if y < 200 else 1 if y < 450 else 2
    big.sort(key=lambda i: (row(i["bbox"][1]), i["bbox"][0]))
    images += [i["xref"] for i in big]
assert len(images) == len(members), (len(images), len(members))

for xref, m in zip(images, members):
    pix = fitz.Pixmap(doc, xref)
    if pix.colorspace is None or pix.colorspace.n != 3:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    smask = doc.extract_image(xref).get("smask", 0)
    if smask:  # transparent cut-outs: put them on white rather than black
        mask = Image.open(io.BytesIO(fitz.Pixmap(doc, smask).tobytes("png"))).convert("L").resize(im.size)
        bg = Image.new("RGB", im.size, "white"); bg.paste(im, (0, 0), mask); im = bg
    im.thumbnail((300, 360))
    im.save(ROOT / m["photo"], "JPEG", quality=72, optimize=True)
print(f"wrote {len(members)} photos")

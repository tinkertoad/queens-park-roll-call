"""Build index.html: src/app.html with the member data and photos inlined.

The result is one self-contained file, so it works opened straight from disk,
on GitHub Pages, or pasted anywhere else. Run after editing src/ or data/:
    python3 build.py
"""
import base64, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,-apple-system,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
</head>
<body>
"""

mpps = json.loads((ROOT / "data/mpps.json").read_text())
for m in mpps:
    m["photo"] = "data:image/jpeg;base64," + base64.b64encode((ROOT / m["photo"]).read_bytes()).decode()
cabinet = (ROOT / "data/cabinet.json").read_text()

app = (ROOT / "src/app.html").read_text()
assert "/*MPPS*/[]" in app and "/*CABINET*/[]" in app
app = app.replace("/*MPPS*/[]", json.dumps(mpps, ensure_ascii=False)).replace("/*CABINET*/[]", cabinet)
(ROOT / "index.html").write_text(HEAD + app + "\n</body>\n</html>\n")
print(f"index.html: {len(mpps)} members, {(ROOT / 'index.html').stat().st_size // 1024} KB")

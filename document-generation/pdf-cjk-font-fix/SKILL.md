---
name: pdf-cjk-font-fix
description: Fix CJK/Chinese text rendering in reportlab PDFs — garbled ■ characters instead of Chinese glyphs. Triggered when generating PDFs with Chinese, Japanese, or Korean content using minimax-pdf or any reportlab-based pipeline.
---

# PDF CJK Font Fix — STHeiti for macOS

## Symptom

Chinese text (or any CJK) renders as `■` squares in PDF output, even when the text is correct in the source.

## Root Cause

reportlab defaults to Latin fonts (Times, Helvetica, Courier) which have no CJK glyph coverage. The document body's text may use a registered STHeiti, but **headings (`h1`/`h2`/`h3`) and table cells typically use the display/body Latin font**, causing them to show as `■`.

## Fix

### 1. Register STHeiti at module load time

In `render_body.py` (or whichever script builds the PDF body), add font registration **before** `make_styles()` is called:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_paths = [
    ("STHeiti",      "/System/Library/Fonts/STHeiti Medium.ttc",  0),
    ("STHeiti-Bold", "/System/Library/Fonts/STHeiti Medium.ttc",  0),
    ("STHeiti-Light","/System/Library/Fonts/STHeiti Light.ttc",   0),
]
for name, path, idx in font_paths:
    try:
        pdfmetrics.registerFont(TTFont(name, path, (idx,)))
    except Exception:
        pass
```

The `idx` parameter `(0,)` is required for TTC (TrueType Collection) files on macOS — without it, you get `index out of range`.

### 2. Override make_styles() CJK block

In `make_styles()`, replace the font assignments so **all** text types that might contain CJK use STHeiti:

```python
_cjk_regular = "STHeiti"     if "STHeiti"     in pdfmetrics.getRegisteredFontNames() else bf
_cjk_bold    = "STHeiti-Bold" if "STHeiti-Bold" in pdfmetrics.getRegisteredFontNames() else bfb
_cjk_display = _cjk_bold   # headings need CJK too

# In the styles dict:
"h1":            ParagraphStyle(..., fontName=_cjk_display, ...),
"h2":            ParagraphStyle(..., fontName=_cjk_display, ...),
"h3":            ParagraphStyle(..., fontName=_cjk_bold,     ...),
"body":          ParagraphStyle(..., fontName=_cjk_regular,  ...),
"bullet":        ParagraphStyle(..., fontName=_cjk_regular,  ...),
"numbered":      ParagraphStyle(..., fontName=_cjk_regular,  ...),
"callout":       ParagraphStyle(..., fontName=_cjk_bold,     ...),
"table_header":  ParagraphStyle(..., fontName=_cjk_bold,     ...),
"table_cell":    ParagraphStyle(..., fontName=_cjk_regular,  ...),
```

### 3. Fix page header/footer

In `_decorate()` (the `onPage` callback), the header uses `font_body_rl` which is Outfit — also no CJK. Override:

```python
_hdr_font = "STHeiti" if "STHeiti" in pdfmetrics.getRegisteredFontNames() else t["font_body_rl"]
canv.setFont(_hdr_font, t["size_meta"])
canv.drawString(lm, top + 16, t["title"])   # no .upper() — STHeiti handles CJK
```

## Verification

```python
import pypdf
reader = pypdf.PdfReader("output.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if "■" in text:
        print(f"Page {i+1}: garbled text detected")
    else:
        print(f"Page {i+1}: OK — {text[:80]}")
```

## Files Modified (this session)

- `/Users/jiang/.hermes/skills/openclaw-imports/minimax-pdf/scripts/render_body.py`
  - CJK font registration at top (TTC index fix)
  - `make_styles()`: h1/h2 → `_cjk_display`, h3 → `_cjk_bold`, table_header/cell fixed
  - `_decorate()`: header uses STHeiti with no `.upper()`

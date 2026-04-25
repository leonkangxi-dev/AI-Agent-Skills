---
name: paddleocr-on-macos
description: Run PaddleOCR v3.5 on macOS for Chinese/English OCR on scanned PDFs. Environment setup, v3.5 API changes, and scanned PDF pipeline.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [OCR, PaddleOCR, PDF, Chinese, scanned, ebook]
prerequisites:
  python: "3.12 or 3.13 (NOT 3.14 — many ML packages incompatible)"
  packages: [paddlepaddle, paddleocr, pymupdf]
---

# PaddleOCR v3.5 on macOS

## Environment Setup

```bash
# Use Python 3.12 or 3.13 (avoid Python 3.14 — incompatible with most ML packages)
# PEP 668 blocks system pip — use a venv
/usr/local/bin/python3.13 -m venv ~/.paddleocr-venv
~/.paddleocr-venv/bin/pip install paddlepaddle paddleocr pymupdf
```

## PaddleOCR v3.5 API (important changes from v2)

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='ch')  # Chinese

# ⚠️ These parameters were REMOVED in v3.5:
#   show_log, use_angle_cls, use_gpu, use_textline_orientation
# If you see: "ValueError: Unknown argument: X" — the param was removed

# ⚠️ ocr.ocr() is deprecated, use ocr.predict()
result = ocr.predict(image_path)  # returns list of OCR results

# ⚠️ cls= kwarg was removed from predict()
# If you see: "TypeError: predict() got an unexpected keyword argument 'cls'"
# — just remove cls=True
```

## Scanned PDF → OCR → Text Pipeline

Scanned PDFs (no selectable text) must be converted to images first, then OCR'd.

```python
import fitz  # pymupdf
from PIL import Image
import io
import os
from paddleocr import PaddleOCR

def ocr_scanned_pdf(pdf_path, dpi=200):
    ocr = PaddleOCR(lang='ch')
    
    # Step 1: PDF pages → PIL Images
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        mat = fitz.Matrix(dpi/72, dpi/72)  # DPI scaling
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
    doc.close()
    
    # Step 2: OCR each image page
    all_text = []
    for img in images:
        tmp_path = "/tmp/ocr_page.png"
        img.save(tmp_path)
        result = ocr.predict(tmp_path)
        for line in result:
            if line and len(line) >= 2:
                text = line[1][0] if isinstance(line[1], (list, tuple)) else line[1]
                all_text.append(text)
    
    return "\n".join(all_text)

# Usage
text = ocr_scanned_pdf("/path/to/scanned.pdf")
open("/tmp/output.txt", "w", encoding="utf-8").write(text)
```

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: Unknown argument: show_log` | Param removed in v3.5 | Remove the param |
| `ValueError: Unknown argument: use_angle_cls` | Param deprecated/removed | Remove the param |
| `ValueError: Unknown argument: use_gpu` | Param removed | Remove the param |
| `TypeError: predict() got an unexpected keyword argument 'cls'` | `cls=` not valid for predict() | Remove `cls=True` |
| `DeprecationWarning: use predict() instead` | `ocr.ocr()` deprecated | Switch to `ocr.predict()` |
| 0 text extracted from PDF | PDF is scanned images, not text | Use OCR pipeline above |
| `.mobi` file reports 0 words | May actually be a scanned PDF | Check with `file` or `pdfinfo` command |
| PaddleOCR extremely slow on CPU | PP-OCRv5 server models are heavy | Use for short docs; for long scans use Tesseract or Adobe Acrobat |
| `edge_tts.exceptions.NoAudioReceived` | Chunk too large (>~4KB for edge-tts) | Split text to ≤3,800 chars per chunk; split by sentence boundaries |
| Telegram won't send large audio | File >50MB | Split with `split -b 45M file part_` before sending |

## Tesseract on macOS — `/tmp` Path Bug

**Symptom:** `tesseract: Error: failed to open locally with tail X.png for filename /tmp/X.png`
**Cause:** Leptonica's `fopenReadStream` on macOS subprocess calls can't reliably read from `/tmp` via symlink/path translation.
**Workaround:** Always copy target files to a path under `$HOME` before running tesseract, and write output also to `$HOME`.

```python
import shutil
shutil.copy('/tmp/page.png', '/Users/jiang/page.png')
subprocess.run(['tesseract', '/Users/jiang/page.png', '/Users/jiang/out', '-l', 'chi_sim+chi_tra', '--psm', '1'])
```

## MOBI files with `.pdf` extension

Some "PDF" files are actually MOBI ebooks disguised with `.pdf` extension.
```bash
file "/path/to/file.pdf"   # If it says "Mobipocket E-book" → it's MOBI
```
Fix: convert via Calibre → `ebook-convert input.mobi /tmp/output.pdf`

## Pre-Assessment: Is OCR Worth It?

Before investing time in OCR, check if the PDF is a **coffee-table / art book** (图鉴类):
- Art books, archaeological atlases, clothing/cultural research albums → image-heavy, very little text → OCR impractical
- Academic journals, novels, history texts → text-heavy → OCR worthwhile

Check with:
```bash
file "/path/to/file.pdf"        # Is it really a PDF or a MOBI/EPUB?
pdfinfo "/path/to/file.pdf" | grep Pages  # Page count

# Quick OCR test on 1-2 pages
pdftoppm -r 150 -png -l 2 "/path/to/file.pdf" /tmp/test_page
# Then OCR the pages to assess text density before running full job
```

## When to Use

- Scanned books (古籍、学术资料) that need text extraction
- PDFs with no selectable text
- Chinese/English bilingual documents
- Batch OCR of image-based ebooks

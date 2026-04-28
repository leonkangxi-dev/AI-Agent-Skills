---
name: ebook-to-audiobook
description: Convert e-books to MP3 audiobooks using edge-tts — smart 12K char segmentation, sentence-aware splitting, Part_N naming
trigger: User asks to convert an ebook to audiobook/TTS/语音书
category: productivity
---

# ebook-to-audiobook

> **edge-tts API: v7+ required.** `edge_tts` ≥ 7.0 uses `Communicate(text, voice, rate)` + `save()`. 
> The old pattern `Communicate()` → `set_properties()` → `generate()` is **deprecated and broken**.
> Install: `pip install --break-system-packages "edge-tts>=7.0"`

## Segmentation Strategy (12K Rule)

**Threshold:** 12,000 characters ≈ 50 min audio per segment

**Split priority order:**
1. Chapter boundaries (always preserve)
2. Paragraph breaks (`\n\n`) for oversized chapters
3. Sentence endings (`。！？\n`) — **never split mid-sentence**

**Algorithm:**
```
1. Parse full text by chapters
2. For each chapter:
   - If len(chapter) <= 12,000 chars → one segment
   - Else split at paragraph boundaries, each sub-segment max 12K chars
   - If remainder < 3,000 chars → merge with next sub-segment
3. Number sequentially: BookName_Part1.mp3, BookName_Part2.mp3...
```

**TTS chunk limit:** Tested up to 12,000 chars per segment — works reliably for Chinese text with sentence-aware splitting. The old "3800 char" limit was from older edge-tts versions; 12K is verified safe with v7.2.8+.

```python
async def tts_one(text: str, out_path: str, voice: str = "zh-CN-YunxiNeural", rate: str = "-5%") -> bool:
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(out_path)
    return True
```

## Supported Formats

| Format | Tool | Status |
|--------|------|--------|
| `.pdf` | PyMuPDF (fitz) | ✅ 可用 — Must be text-based (not scanned). Scanned PDFs return 0 words. |
| `.epub` | EbookLib | ✅ 可用 — Parse `item.get_type() == 9` (EPUBtml) for text items |
| `.mobi` | `mobi.extract()` | ✅ 可用 — Returns path to extracted content (EPUB or HTML) |
| `.azw3` | `mobi.extract()` + EbookLib | ✅ 可用 — Converts to EPUB internally via `mobi.extract()`; parse result with EbookLib |
| `.txt` | Raw read | ✅ 可用 — UTF-8 |

## Critical Discoveries

### AZW3 / MOBI → EPUB
`mobi.extract(path)` returns a **path string** to the extracted content (EPUB or HTML). Parse EPUB results with EbookLib:

```python
import mobi
from ebooklib import epub

extracted_path = mobi.extract(azw3_or_mobi_path)
if extracted_path.endswith('.epub'):
    book = epub.read_epub(extracted_path)  # EbookLib
else:
    # HTML file — read directly
    with open(extracted_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
```

### MOBI Inside PDF Extension
Files named `*.pdf.mobi` are Mobipocket format. Use `file <path>` to confirm before processing.

### Chinese EPUB with Garbled Filenames (ZIP encoding bug)
System `unzip` fails with "Illegal byte sequence" when filenames contain non-ASCII chars. **Always use Python's `zipfile` module** — it handles encoding correctly:

```python
import zipfile
with zipfile.ZipFile(epub_zip, 'r') as z:
    z.extractall('/destination/')
```

### edge-tts Chinese Chunk Size: 12K Verified Safe (v7.2.8+)
Practical testing shows Chinese text up to 12,000 chars per segment works reliably with edge-tts v7.2.8+. The old "3800 char" limit was conservative. Always split on sentence boundaries (never mid-sentence):
```python
import re
def smart_split(text, max_chars=12000):
    """Split text at paragraph/sentence boundaries, max 12K chars per chunk."""
    chunks = []
    while len(text) > max_chars:
        split_pos = text.rfind('\n', 0, max_chars)
        if split_pos < max_chars // 2:
            split_pos = text.rfind('。', 0, max_chars)
        if split_pos < max_chars // 2:
            split_pos = text.rfind('，', 0, max_chars)
        if split_pos < 100:
            split_pos = max_chars
        chunk = text[:split_pos + 1].strip()
        if chunk:
            chunks.append(chunk)
        text = text[split_pos + 1:].strip()
    if text.strip():
        chunks.append(text.strip())
    return chunks
```

### Chinese Text Word Count Trap — Use Character Count
`len(text.split())` is meaningless for Chinese (returns ~word count ≈ character count / 2 for Chinese). **Always use `len(text)` (character count)** to estimate Chinese text length and audio duration.

```python
# WRONG — gives ~90 for a 134K-char book
word_count = len(text.split())  # Chinese splits on characters!

# CORRECT — character count
char_count = len(text)  # 134,000 chars ≈ 4.5 hours audio
```

### Calibre-Split EPUB Pattern
Calibre-generated EPUBs often split content across multiple files:
```
index_split_000.html — 封面/目录 (200 chars)
index_split_001.html — 第1章 (67,247 chars)
index_split_002.html — 第2章 (66,744 chars)
index_split_003.html — 尾页 (216 chars)
```
**Sum all `index_split_*.html` character counts** to get true book length. Pattern: `split_000`, `split_001`, ... sorted numerically.

### Tesseract + macOS /tmp Bug
Tesseract 5.5.2 (Homebrew) can't read files from `/tmp` on macOS — `Leptonica Error in pixRead: image file not found`. Copy to home directory first.

### PaddleOCR CPU Too Slow
PaddleOCR in CPU mode is extremely slow (~2+ min/page). Not viable for batch. Use Adobe Acrobat Pro OCR for scanned PDFs.

## EPUB Parsing with EbookLib
## EPUB Parsing with EbookLib

```python
from ebooklib import epub
def extract_text_epub(file_path: str) -> str:
    book = epub.read_epub(file_path)
    texts = []
    for item in book.get_items():
        if item.get_type() == 9:  # EPUBtml
            content = item.get_content().decode('utf-8', errors='ignore')
            t = re.sub(r'<[^>]+>', ' ', content)
            t = re.sub(r'\s{2,}', ' ', t).strip()
            if len(t) > 30:
                texts.append(t)
    return '\n\n'.join(texts)
```

## Text Cleaning

```python
def html_to_text(html: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', html)
    for old, new in [('&nbsp;', ' '), ('&amp;', '&'), ('&#\d+;', ' '),
                     ('\xa0', ' '), ('&gt;', '>'), ('&lt;', '<'),
                     ('&quot;', '"'), ('  ', ' ')]:
        text = text.replace(old, new)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
```

## Voice Selection

| Content Type | Voice | Note |
|---|---|---|
| 悬疑/侦探/惊悚小说 | YunxiNeural（低沉男声）| 用户明确偏好 |
| 其他中文内容 | XiaoxiaoNeural（女声）| 默认 |
| 英文内容 | en-US-AnaNeural / GuyNeural | 根据性别 |
| 古文/诗词 | YunxiNeural | 低沉有古韵 |

**TTS with edge-tts**

```python
VOICE = "zh-CN-YunxiNeural"  # Default for mystery/suspense
# Override: XiaoxiaoNeural for non-fiction, general content

async def tts_one(text: str, out_path: str, voice: str = VOICE, rate: str = "-5%") -> bool:
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(out_path)
    return True
```

## MP3 Merge (ffmpeg)

```python
def concat_mp3(mp3_files: list, out_path: str, tmpdir: str) -> bool:
    concat_list = os.path.join(tmpdir, "concat.txt")
    with open(concat_list, 'w') as f:
        for fp in mp3_files:
            f.write(f"file '{fp}'\n")
    result = subprocess.run(
        ['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
         '-i', concat_list, '-c', 'copy', out_path],
        capture_output=True, text=True)
    return result.returncode == 0
```

## Telegram Limit
**50 MB** per file. Split at ~45MB. For large chapters:

```bash
# Split by time (30 min per file)
ffmpeg -i large.mp3 -t 1800 -c copy part1.mp3
ffmpeg -i large.mp3 -ss 1800 -c copy part2.mp3
```

## Required Dependencies
```bash
pip install --break-system-packages edge-tts EbookLib mobi
```
> Note: `mobi` package handles both `.mobi` and `.azw3` formats (converts to EPUB internally).

## Archive Paths
- Physical: `~/Desktop/hermes/AudioBooks/{title}/`
- Obsidian: `~/Documents/Obsidian/Projects/AudioBooks/{title}.md`

## Key Pitfalls
- Scanned PDFs: PyMuPDF returns 0 text. No OCR in this pipeline — use Adobe Acrobat Pro OCR.
- AZW3: `mobi.extract()` returns EPUB path string (not tuple); parse with EbookLib.
- `mobi.extract()` returns a path string directly (verified 2026-04-28).
- Edge-tts v7+ Chinese chunk size: **12,000 chars** verified safe (v7.2.8). Old "3800 char" limit is outdated. Split on sentence boundaries.
- Chinese EPUB from ZIP: Use Python `zipfile`, NOT system `unzip` (encoding issues).
- Tesseract can't read from `/tmp` on macOS — use home directory instead.

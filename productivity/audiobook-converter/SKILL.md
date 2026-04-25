---
name: audiobook-converter
description: Convert e-books (MOBI/AZW3/EPUB/PDF/TXT) to MP3 audiobook using edge-tts, with Telegram push and Obsidian archive.
triggers:
  - e-book file received via Telegram
  - user asks to convert e-book to audio
  - user sends .mobi/.azw3/.epub/.pdf/.txt file
---

# Audiobook Converter — e-book to MP3 pipeline

## Prerequisites (macOS)
```bash
pip3 install --break-system-packages edge-tts EbookLib mobi
# edge-tts: TTS engine; EbookLib: EPUBs; mobi: .mobi + .azw3
# PyMuPDF (fitz): pre-installed for PDF
```

Voice: `zh-CN-YunxiNeural` (云希), edge-tts default for Chinese audiobooks.

## Full Pipeline

### 1. Hermes Gateway whitelist (one-time fix)
If file is rejected with "Unsupported document type", add to:
`~/.hermes/hermes-agent/gateway/platforms/base.py` → `SUPPORTED_DOCUMENT_TYPES`:
```python
".epub": "application/epub+zip",
".mobi": "application/x-mobipocket-ebook",
".azw3": "application/vnd.amazon.azw3",
```
Then: `Hermes gateway restart`

### 2. Text extraction by format
```python
# .mobi / .azw3 → mobi.extract() → HTML or EPUB
# AZW3 key insight: mobi.extract() returns (tmp_dir, book.epub)
#   → must parse with EbookLib, NOT html_to_text
# .epub → EbookLib epub.read_epub(), type==9 items only
# .pdf  → PyMuPDF: fitz.open().get_text() per page
# .txt  → open(encoding='utf-8')
```

### 3. Clean text
```python
import re
def html_to_text(html: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', html)
    for old, new in [('&nbsp;', ' '), ('&amp;', '&'), ('&#\\d+;', ' '),
                     ('\\xa0', ' '), ('&gt;', '>'), ('&lt;', '<'),
                     ('&quot;', '"'), ('  ', ' ')]:
        text = text.replace(old, new)
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    return text.strip()
```

### 4. Chapter splitting
```python
headers = list(re.finditer(
    r'(第[一二三四五六七八九十百零\\d]+[章节部篇]\\s*[：:：]?\\s*.+?)'
    r'(?=\n|　|$)', text))
```
Fallback: paragraph chunking at ~5000 chars if < 2 chapter headers.

### 5. TTS conversion (edge-tts, async)
```python
import edge_tts, asyncio
VOICE = "zh-CN-YunxiNeural"

async def tts_one(text: str, out_path: str) -> bool:
    if len(text) > 5800:
        text = text[:5800]
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(out_path)
    return True

async def convert_all(chapters: list, tmpdir: str) -> list:
    for i, chapter_text in enumerate(chapters):
        mp3_path = os.path.join(tmpdir, f"ch_{i+1:03d}.mp3")
        ok = await tts_one(chapter_text, mp3_path)
        await asyncio.sleep(0.15)  # rate limit guard
```

### 6. Merge MP3 (ffmpeg concat demuxer)
```bash
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output.mp3
```
concat.txt: `file '/path/ch_001.mp3'` per line.

### 7. Telegram send (50MB limit)
Audiobooks always exceed Telegram's 50MB limit. Split first:
- Group chapter MP3s into batches ≤ 45MB
- Merge each batch → Part1.mp3, Part2.mp3...
- Send: text notification first, then MEDIA: file path

### 8. Archive
- **Physical:** `~/Users/jiang/Desktop/hermes/AudioBooks/{书名}/`
- **Obsidian:** `~/Documents/Obsidian/Projects/AudioBooks/{书名}.md`

## Key Lessons Learned
- AZW3 via mobi.extract() returns an EPUB file — must use EbookLib to parse it, not html_to_text
- Telegram Bot API limit is 50MB for documents/audio — always split audiobooks before sending
- execute_code sandbox lacks system pip packages — run conversion scripts via terminal() with `/tmp/` path
- Chapter header regex must use raw strings: `r'第\\d'` not `'\\d'`
- mobi files may have misleading extensions (e.g., `.pdf.mobi`) — always use `file` command to check real type

## Reference Files
- Batch converter: `/tmp/audiobook_batch.py`
- Gateway whitelist: `~/.hermes/hermes-agent/gateway/platforms/base.py`

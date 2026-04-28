---
name: chinese-news-collection
description: >
  Collect Chinese-language (简体中文) news from the web when most RSS feeds
  are blocked or return errors. Tested on macOS/Linux environments behind
  typical network restrictions.
license: MIT
version: "1.0"
---

# Chinese News Collection

## Problem
Most Chinese news RSS feeds return 404s, HTML error pages, or timeouts when
fetched from non-CN networks:
- 新华社 RSS → 404 (redirects to 404 page)
- 人民日报 RSS → blocked
- 澎湃新闻 RSS → 404
- 新京报 RSS → 404
- 央视新闻 RSS → blocked
- 财新网 RSS → blocked
- 法国24中文 RSS → 404
- 半岛中文 RSS → 404

## Working Sources

### 1. BBC Chinese (RELIABLE)
**RSS**: `https://feeds.bbci.co.uk/zhongwen/simp/rss.xml`
- Returns valid XML with 38+ items
- Use `feedparser` Python module to parse
- Covers: 中国, 国际, 财经, 科技, 视频, 香港, 台湾

```python
import urllib.request, ssl, feedparser

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
    feed = feedparser.parse(resp)
    for entry in feed.entries[:15]:
        print(entry.title, entry.link)
```

**Website pages** (via browser_navigate):
- 主页: `https://www.bbc.com/zhongwen/simp`
- 国际: `https://www.bbc.com/zhongwen/simp/world`
- 中国: `https://www.bbc.com/zhongwen/simp/china`
- 财经: `https://www.bbc.com/zhongwen/simp/business`
- 科技: `https://www.bbc.com/zhongwen/simp/science_and_tech`

### 2. Twitter/X (fallback)
Search `topic=news` or `from:bbcchinese` with web search to get recent items.

## Category Mapping for BBC Chinese

| Category | BBC Section |
|---|---|
| 🏛️ 政治要闻 | 国际 + 中国 |
| 💻 科技动态 | science_and_tech (if available) |
| 💰 经济财经 | business |
| 🔥 热门事件 | 主页头条 |

## Dependencies
```bash
pip3 install feedparser --break-system-packages
```

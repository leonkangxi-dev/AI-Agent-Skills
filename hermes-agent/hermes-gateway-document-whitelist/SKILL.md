---
name: hermes-gateway-document-whitelist
description: 在 Hermes Gateway 白名单中添加新的文档类型（如电子书格式），解决 Bot 拒绝上传特定文件类型的问题
triggers:
  - Unsupported document type
  - SUPPORTED_DOCUMENT_TYPES
  - .mobi .epub .azw3 上传被拒
---

# Hermes Gateway 文档类型白名单扩展

## Problem
Telegram Bot 拒绝上传 `.mobi` / `.epub` / `.azw3` 文件，报错：
```
Unsupported document type '.mobi'. Supported types: .docx, .log, .md, .pdf, .pptx, .txt, .xlsx, .zip
```

## Root Cause
Hermes Gateway 使用硬编码白名单 `SUPPORTED_DOCUMENT_TYPES`（位于 `gateway/platforms/base.py`）过滤上传文档类型。

## Fix
在白名单中添加电子书格式：

**文件：** `~/.hermes/hermes-agent/gateway/platforms/base.py`

```python
SUPPORTED_DOCUMENT_TYPES = {
    # ... existing entries ...
    # ── E-book formats for AudioBook workflow ─────────────────────────────────
    ".epub": "application/epub+zip",
    ".mobi": "application/x-mobipocket-ebook",
    ".azw3": "application/vnd.amazon.azw3",
}
```

**MIME types 参考：**
| 格式 | MIME |
|------|------|
| .epub | application/epub+zip |
| .mobi | application/x-mobipocket-ebook |
| .azw3 | application/vnd.amazon.azw3 |

## Activation
修改后必须重启 Gateway：
```bash
Hermes gateway restart
```

## Verification
重启后，直接发送目标格式文件给 Bot 即可。

## Notes
- 搜索定位：`grep -r "SUPPORTED_DOCUMENT_TYPES" ~/.hermes/hermes-agent/gateway/`
- 白名单定义在 `gateway/platforms/base.py:589`
- 检查位置在 `gateway/platforms/telegram.py:2711`（`if ext not in SUPPORTED_DOCUMENT_TYPES`）

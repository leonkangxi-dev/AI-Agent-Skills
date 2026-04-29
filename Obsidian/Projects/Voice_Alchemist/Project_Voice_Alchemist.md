# Project Voice Alchemist - 语音炼金术

**创建时间:** 2026-04-23
**状态:** ✅ 就绪
**执行者:** 暗夜匿影 🌑

---

## 一、任务概述

将电子书转化为高质量 MP3 语音书，推送到 Telegram。

## 二、技术架构

| 组件 | 技术 |
|------|------|
| **PDF 解析** | PyMuPDF (fitz) |
| **EPUB 解析** | ebooklib |
| **MOBI/AZW3 解析** | python-mobi |
| **语音合成** | gTTS (Google TTS) |
| **文本清洗** | 正则表达式 |
| **分段策略** | 按章节或每 5000 字 |
| **推送渠道** | Telegram Bot |

## 三、核心参数

| 参数 | 值 |
|------|-----|
| **每段字数上限** | 5000 字 |
| **语速** | 1.0x |
| **语音引擎** | gTTS (zh-CN) |
| **文本编码** | UTF-8 |
| **Telegram Bot** | @leonhermesai_bot |

## 四、文件流转

```
Inbox (~/Documents/Obsidian/30_Library/Inbox/)
  ↓ 检测到新书
voice_alchemist.py
  ↓ 解析 + 清洗 + 分段
切片处理
  ↓ gTTS 合成
~/Documents/Obsidian/30_Library/Audiobooks/[书名]/
  ↓ 同时推送 Telegram
@leonhermesai_bot
```

## 五、脚本位置

| 脚本 | 路径 |
|------|------|
| **主程序** | `~/.openclaw/workspace/services/voice_alchemist.py` |
| **数据库** | `~/Documents/Obsidian/Projects/Voice_Alchemist/voice_alchemist.db` |

## 六、使用方式

```bash
# 扫描 Inbox 自动处理
python3 ~/.openclaw/workspace/services/voice_alchemist.py

# 直接处理指定书籍
python3 ~/.openclaw/workspace/services/voice_alchemist.py /path/to/book.pdf
```

## 七、进度追踪

```sql
-- 查看处理中书籍
SELECT title, total_chunks, completed_chunks, status FROM books;

-- 查看切片详情
SELECT chunk_index, audio_path, duration_sec, status FROM chunks WHERE book_id=1;
```

## 八、预计处理时间

| 因素 | 说明 |
|------|------|
| **单章节** (5000字) | ~30-60 秒 (网络 TTS 生成) |
| **整本书** (300页) | ~15-30 分钟 |
| **推送延迟** | 每章 ~5 秒 |

---

*归档时间: 2026-04-23 18:51*
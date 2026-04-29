---
title: AutoClip - AI视频智能切片
type: project
url: https://github.com/zhouxiaoka/autoclip
tags:
  - ai
  - video
  - automation
---

# AutoClip

> 基于AI的智能视频切片处理系统

## 项目信息

- **URL:** https://github.com/zhouxiaoka/autoclip
- **Stars:** 4.1k
- **技术栈:** FastAPI + React + Celery + Redis

## 核心功能

- 🎬 多平台支持 (YouTube, B站)
- 🤖 AI智能分析 (通义千问)
- ✂️ 自动切片
- 📚 智能合集
- 🚀 实时处理

## 本地部署

| 服务 | 端口 | 状态 |
|------|------|------|
| 后端 API | 8000 | ✅ |
| 前端界面 | 3000 | ✅ |
| Redis | 6379 | ✅ |

**访问:** http://localhost:3000

## 配置

在 `.env` 中设置通义千问 API Key:
```
API_DASHSCOPE_API_KEY=your_key
```

---

*记录时间: 2026-04-15*
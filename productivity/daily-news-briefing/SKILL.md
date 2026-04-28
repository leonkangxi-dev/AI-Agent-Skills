---
name: daily-news-briefing
description: >
  每日新闻简报自动化 — 抓取权威RSS/新闻源 → 生成带来源标注的结构化简报 → 
  PDF输出 → Telegram推送 → Obsidian归档。一套完整的工作流。
  触发条件：用户要求生成新闻简报、定时推送、或修改新闻任务配置。
metadata:
  version: "2.0"
  category: productivity
---

# 每日新闻简报自动化

## 架构总览

```
定时触发(每日07:00) / 手动触发
       ↓
新闻抓取（RSS + Tavily topic=news）
       ↓
结构化简报（四大板块 × 国内/国外）
       ↓
来源标注（权威媒体 | 记者 | 日期 | 链接）
       ↓
┌──────┴──────┐
↓              ↓
PDF生成        Obsidian归档
(~/Desktop/    (~/Documents/Obsidian/
 hermes/news/)  10_Nodes/Daily_News/)
       ↓
 Telegram推送（telegram:dou bao）
```

## 新闻来源（必须严格使用）

### 国内权威RSS
| 媒体 | RSS URL |
|------|---------|
| 新华社 | https://www.news.cn/rss/politics.xml |
| 人民日报 | https://paper.people.com.cn/rss/rss5.xml |
| 央视新闻 | https://www.cctv.com/rss/news.xml |
| 澎湃新闻 | https://www.thepaper.cn/rss_home.xml |
| 新京报 | https://www.bjnews.com.cn/rss/headnews.xml |
| 财新网 | http://www.caixin.com/rss/news.xml |
| 微博热搜 | 手动抓取前10 |

### 国际权威RSS
| 媒体 | RSS URL |
|------|---------|
| BBC中文 | https://feeds.bbci.co.uk/zhongwen/simp/rss.xml |
| Reuters中文 | https://www.reutersagency.com/feed/?best-topics=china&post_type=best |
| CNN中文 | https://rss.cnn.com/rss/edition_chinese.rss |
| 法国24中文 | https://www.france24.com/zh/rss |
| 半岛中文 | https://www.aljazeera.com/xml/rss最多10条.xml |

### 搜索补充（Tavily，必须加 topic=news）
- 搜索必须使用 `--topic news` 参数，限制为最近7天内
- 不加 topic 参数会返回历史旧闻（如巴黎奥运会2024年内容混入2026年简报）

## 每条新闻的来源标注格式

```
【国内】新闻标题
摘要（50-100字）
来源：媒体名称 | 记者姓名（如有） | 发布日期
链接：https://xxx.com

【国外】News Title
Summary
Source: Media Name | Journalist Name | Date
Link: https://xxx.com
```

来源优先级：
1. 权威媒体RSS（如BBC中文、Reuters、新华社等）
2. 知名媒体网站（澎湃、财新、观察者网等）
3. 社交媒体（Twitter @xxx、微博 @xxx）
4. 每条必须包含链接，没有链接的条目用「来源：整理」

## 四大板块
- 🏛️ 政治要闻
- 💻 科技动态
- 💰 经济财经
- 🔥 热门事件

每个板块分【国内】【国外】各10条。

## 文件路径约定
- PDF输出：`~/Desktop/hermes/news/YYYYMMDD_每日新闻简报.pdf`
- Obsidian归档：`~/Documents/Obsidian/10_Nodes/Daily_News/YYYY-MM-DD.md`
- 工作日志：`~/Documents/Obsidian/90_System/History_Log.md`

## Telegram 推送
- 目标：`telegram:dou bao`（不能用数字ID，要用注册的平台名称）
- 格式：`📰 *每日新闻简报 — YYYY年MM月DD日*`
- 附PDF文件发送

## Cron Job 配置
- Cron ID：`dc33224303cf`
- 技能：`minimax-pdf` + `tavily`
- 推送目标：`telegram:dou bao`

## 已知问题 & 解决方案

### Tavily 返回旧闻
**问题**：热门事件板块出现巴黎奥运会（2024）等过时内容
**原因**：搜索没有加 `topic=news` 参数
**解决**：必须加 `--topic news`，限制7天内新闻

### Telegram 推送失败
**原因**：超级群组ID格式错误
**解决**：用 `telegram:dou bao`（平台注册名称），不要用数字ID

### PDF 生成超时
**问题**：`minimax-pdf` 的 Playwright 渲染封面步骤约30-60秒
**现象**：cron session 报 `Stream stalled mid tool-call`
**影响**：PDF文件实际已生成，只是agent汇报超时
**建议**：如果PDF未生成，人工检查 `~/Desktop/hermes/news/` 目录

### 用户索取 PDF 时的查找路径
**注意**：cron 输出目录 `~/.hermes/cron/output/dc33224303cf/` 只含 `.md` 工作日志，不含 PDF
**正确路径**：`~/Desktop/hermes/news/YYYYMMDD_每日新闻简报.pdf`
**发送方式**：用 `send_message(target="telegram:dou bao")` 附带文件路径即可，无需手动查路径

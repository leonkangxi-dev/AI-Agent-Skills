# Hermes 工作记忆库

> 上次清理：2026-04-28
> 由「暗夜」触发清理，迁移至 Obsidian 长期存储

---

## 系统配置

- **GitHub 仓库**：~/Documents/GitHub/AI-Agent-Skills/
- **PAT 已存**：macOS 钥匙串（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）
- **Obsidian 库**：~/Documents/Obsidian/
- **技能路径**：~/.hermes/skills/
- **Hermes Gateway**：launchd 管理，restart 前需先 stop，正常 CPU<5%

## 用户偏好

- **TTS 音色**：悬疑/侦探/惊悚类 → YunxiNeural；其他默认 → XiaoxiaoNeural
- **文件规范**：所有文件统一存放在 `/Users/jiang/Desktop/hermes/` 下，按类型分类：
  - `media/` — 视频文件（下载的Twitter/X视频等）
  - `news/` — PDF简报（每日新闻简报等）
  - `AudioBooks/` — 有声书/MP3
  - `word/` — Word文档
  - `ppt/` — PPT演示文稿
  - `mp3/` — 独立音频文件
  - 禁止使用 /tmp/ 存放用户文件
- **视频下载**：必须确认有音轨，用 `yt-dlp -f "bestvideo+bestaudio"` 或 ffprobe 验证

## 定时任务

| 任务 | 调度 | 状态 |
|------|------|------|
| 每日新闻简报 | 每天 07:00 | ✅ 已创建（dc33224303cf） |
| 每日归档与缓存清理 | 每天 23:00 | ✅ 已创建（c628ab0f911a） |

新闻简报流程：抓取 → Obsidian归档 → PDF存 ~/Desktop/hermes/news/ → Telegram推送

## Hermes Agent 备份（2026-04-28）

- **备份版本**：v0.11.0 (2026.4.23) / commit df51ad79
- **备份位置**：~/Desktop/hermesbakup/
- **备份内容**：hermes-agent_bak_20260428/ (1.2GB)
- **恢复脚本**：restore_hermes.sh（回滚）/ restore_fresh.sh（新机器）
- **详细文档**：~/Desktop/hermesbakup/FULL_RESTORE_GUIDE.md
- **Obsidian归档**：
  - ~/Documents/Obsidian/Hermes/index.md
  - ~/Documents/Obsidian/Hermes/Hermes_Backup_Restore.md
  - ~/Documents/Obsidian/Hermes/Hermes_Agent_Info.md

## 待清理的短期记忆（可删除）

- Hermes Gateway 异常占用详细记录（已压缩至下方）
- 2026-03-15 工作日志条目（已过期）

## 问题解决备忘

**Hermes Gateway CPU 飙高（2026-04-21）**
- 根因：Kimi配额用尽→403→launchctl启动死循环→多进程累加
- 经验：restart前先stop，正常CPU<5%
- 已在HEARTBEAT添加主动监控


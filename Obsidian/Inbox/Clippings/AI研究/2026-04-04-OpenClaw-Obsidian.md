# 我用 OpenClaw + Obsidian，做了一个会自动消化链接的第二大脑

## 来源链接
https://silicon-hotpot.notion.site/OpenClaw-Obsidian-335d971b8d3780978648fe5e2ff7b076

## 核心摘要
这是一个关于如何将 OpenClaw 与 Obsidian 集成，创建自动消化链接的第二大脑系统的教程。

## 关键内容

### 安装步骤
1. 将 SKILL.md 复制粘贴给 OpenClaw 安装
2. 将 routing-model.md 复制粘贴给 OpenClaw

### Librarian Skill 功能
- 根据 URL 类型自动路由到正确的 Obsidian 位置
- 支持：普通文章、GitHub 项目、YouTube 视频、微信公众号
- 自动 URL 规范化（移除 utm_* 参数）
- 重复链接自动跳过

### 路由规则
- 普通文章 → 2-resource/clip/clips.md
- GitHub 项目 → 2-resource/github-research/owner-repo.md
- YouTube → 2-resource/youtube/
- 微信公众号 → 同普通文章

### 推荐工具路线
- 网页正文抓取 → Lightpanda
- 浏览器自动化 → bb-browser
- 搜索 → Agent-Reach + bb-browser

## 标签
#openclaw #obsidian #第二大脑 #知识管理 #skill #tutorial

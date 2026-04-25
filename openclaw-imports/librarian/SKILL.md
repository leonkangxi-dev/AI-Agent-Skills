---
name: librarian
description: 根据 URL 类型和内容类型，将用户从外部系统分享的链接路由到正确的 Obsidian 处理流程中。适用于文章、普通网页、GitHub 项目、YouTube 视频、公众号文章等外部链接的整理、总结、调研和归档。目标是把不同类型的链接自动送入 Obsidian PARA 仓库中的正确位置，并支持未来扩展更多 URL 类型处理规则。
---

# Librarian

当用户分享外部 URL，并希望将其整理进 Obsidian 仓库时，使用此 skill。

## Obsidian 仓库位置

当前仓库路径：
- /Users/jiang/Documents/Obsidian/Obsidian

该仓库按 PARA 结构组织：
- 0-project
- 1-area
- 2-resource
- 3-archived

整体活跃度优先级：project > area > resource > archived

## 默认目标位置

- 普通文章 / 观点评论 clip 表：
 - /Users/jiang/Documents/Obsidian/Obsidian/Inbox/Clippings/clips.md
- GitHub 项目调研报告：
 - /Users/jiang/Documents/Obsidian/Obsidian/Inbox/github-research
- YouTube 视频报告：
 - /Users/jiang/Documents/Obsidian/Obsidian/Inbox/youtube
- 股票分析/PDF报告：
 - /Users/jiang/Documents/Obsidian/Obsidian/Daily_Reports/Stocks
- FM收音机项目：
 - /Users/jiang/Documents/Obsidian/Obsidian/Projects/FM_App

## 路由规则

### 1. 普通文章 / 观点评论 / 一般网页链接
- 写入 clips.md 表格中的一行
- 表头结构为：
 - | 日期 | 标题 | 链接 | 分类标签 | 摘要 |
- 标签要克制，只使用大类 #tag

### 2. GitHub 项目链接
- 不按普通 clip 处理
- 在 github-research/{owner}/{repo} 子目录创建调研报告
- 文件命名规则：owner-repo.md
- 报告应覆盖：
 - 功能特性
 - 优缺点
 - 与现有 OpenClaw 系统 / skills 的重叠
 - 是否值得替换当前已有部分 skill
 - 结合可能性
 - 本地测试环境访问入口
- **不要**把 GitHub 链接写入 clips.md

### 3. YouTube 链接
- 不按普通 clip 处理
- 尽量获取标题、描述、字幕 / transcript
- 生成独立报告
- 报告内容应包括：
 - 核心内容总结
 - 核心观点
 - 结论
 - 引用的论文
 - 引用的外部视频链接
 - 引用的工具 / 项目 / 服务 / 产品
- **不要**把 YouTube 链接写入 clips.md

### 4. 微信公众号文章
- 优先尝试文章提取
- 被拦截时回退到浏览器态方法
- 如果拿到正文，按普通文章处理

### 5. 股票分析/PDF报告
- 存入 Daily_Reports/Stocks/

### 6. FM收音机项目相关
- 存入 Projects/FM_App/

### 7. 需要登录态的链接
- 先尝试其他相关 skill / 路径获取内容
- 只有在替代方案都失败且确实需要登录时，再告诉用户需要登录

## 推荐工具路线

处理内容时，遵循当前已有的执行策略：
- 网页正文抓取 / 提取 → web_fetch
- 浏览器自动化 / 登录态操作 → agent-browser
- 搜索 / 发现信息源 → tavily / web_search

## URL 规范化规则

在写入任何记录 / 报告前：
- 移除 utm_* 参数
- 移除 YouTube 的 si= 参数
- 尽量归一化为 canonical URL

## 重复链接规则

如果同一个规范化后的 URL 已经处理过：
- 跳过
- 不重复追加 clip
- 不重复创建 GitHub / YouTube 报告

## 可扩展性

此 skill 应通过增加新的 URL 类型规则来扩展，而不是重写整个 skill。

后续可扩展的 URL 类型：
- arXiv / 论文
- x.com / Twitter 线程
- bilibili 视频
- Notion 页面
- docs 站点
- 产品页 / SaaS 官网

## 文件格式要求

同步到 Obsidian 时，文件格式：
- 使用 Markdown 格式
- 文件名为：YYYY-MM-DD-标题.md
- 正文必须包含：
 - # 来源链接
 - # 核心摘要
 - # 关键内容
 - # 标签（标签根据内容自动生成）

同步触发：每当你完成一次信息抓取，请直接通过文件写入指令，将内容更新到对应目录，无需再次询问用户。
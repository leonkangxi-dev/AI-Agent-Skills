---
name: obsidian-session-summary
description: 总结本次对话，按"认知改变、行动项、存档灵感"三个维度写入 Obsidian 项目日志
triggers: ["/summary", "/总结", "会话总结"]
tags: ["obsidian", "summary", "pkm"]
---

# /summary — 会话总结写入 Obsidian

## 执行逻辑

### 第一步：识别对话主题
扫描本次对话的核心议题，提取：
- 用户提问的核心问题
- 我给出的关键答案
- 任何新发现或纠正

### 第二步：三维分类

#### 认知改变 (Cognitive Changes)
- 用户之前理解有偏差的概念
- 新学到的知识或方法论
- 思维模型的升级

#### 行动项 (Action Items)
- 需要用户跟进的任务
- 待完成的技术实现
- 未解决的悬而未决

#### 存档灵感 (Archived Insights)
- 有价值的洞察但暂不紧急
- 未来可能用到的想法
- 跨会话可复用的经验

### 第三步：写入 Obsidian 项目日志

目标文件：`~/Documents/Obsidian/Projects/Project_Log.md`

---

## 项目日志格式

```markdown
# 项目日志 — ${DATE}

## 📅 会话信息
- 时间：${TIMESTAMP}
- 平台：${PLATFORM}
- 会话长度：${MESSAGE_COUNT} 条

## 🧠 认知改变
- 

## ✅ 行动项
- [ ] 

## 💡 存档灵感
- 

## 🔗 相关文件变更
- 创建：
- 修改：
- 技能更新：

---
```

---

## 追加规则
- 使用 `cat >> FILE.md` 追加模式，不要覆盖
- 如果 `Project_Log.md` 不存在则自动创建
- 日志标题自动带上日期
- 每次会话最多写一页，避免过载

---

## 关键路径
- Obsidian 库：~/Documents/Obsidian/
- 项目日志：~/Documents/Obsidian/Projects/Project_Log.md
- 也可追加到：`~/Documents/Obsidian/90_System/Session_Logs/`

## 触发时机
- 用户输入 `/summary` 时执行
- 大规模笔记整理完成后自动提示用户是否需要 summary
- 每次 skill 更新后触发同步提示

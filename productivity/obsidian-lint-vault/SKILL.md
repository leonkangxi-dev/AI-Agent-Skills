---
name: obsidian-lint-vault
description: 检查 Obsidian 库中的孤岛笔记，生成关联建议报告存入 Inbox/Health_Report.md
triggers: ["/lint", "/健康检查", "孤岛笔记"]
tags: ["obsidian", "health-check", "pkm"]
---

# /lint — Obsidian 健康检查 & 孤岛笔记检测

## 执行逻辑

### 第一步：建立知识图谱
扫描整个 Obsidian 库：
```bash
cd ~/Documents/Obsidian
# 提取所有 .md 文件的内部链接和标签
grep -rh '\[\[' . 2>/dev/null | sed 's/\[\[\([^|\]]*\).*\]\]/[[\1]]/g' | sort | uniq > /tmp/all_links.txt
grep -rh '#' --include="*.md" . 2>/dev/null | grep -oE '#[a-zA-Z0-9_\-]+' | sort | uniq > /tmp/all_tags.txt
find . -name "*.md" -type f > /tmp/all_notes.txt
```

### 第二步：识别孤岛笔记
**孤岛笔记定义：**
- 无出链（outgoing links）的笔记
- 无标签的笔记
- 从未被其他笔记引用的笔记
- Inbox 中创建超过7天但未整理的笔记

### 第三步：生成关联建议
对每个孤岛笔记：
1. 扫描文件名和内容关键词
2. 匹配现有的 Concepts/Nodes
3. 生成具体建议：`[[建议链接到 XXX]]` 或 `#建议标签`

### 第四步：输出报告
路径：`~/Documents/Obsidian/Inbox/Health_Report.md`

---

## 健康报告模板

```markdown
# Obsidian 健康报告 — ${DATE}

## 📊 库统计
- 总笔记数：N
- 有出链笔记：N
- 孤岛笔记：N
- 孤岛率：XX%

## 🏝️ 孤岛笔记清单
| 文件 | 创建时间 | 可能关联 | 建议标签 |
|------|---------|---------|---------|
| xxx.md | YYYY-MM-DD | [[概念A]], [[概念B]] | #标签 |

## 🏷️ 未分类标签
（出现在笔记中但不属于任何已知分类的标签）

## 💡 优化建议
1. ...
2. ...
```

---

## 关键路径
- Obsidian 库：~/Documents/Obsidian/
- 输出报告：~/Documents/Obsidian/Inbox/Health_Report.md

## 判断标准
- 孤岛阈值：出链=0 且 被引用=0
- Inbox 警告：Inbox/ 下超过7天未移出的文件
- 报告自动推送到 Telegram（可选）

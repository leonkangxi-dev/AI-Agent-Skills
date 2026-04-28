---
name: obsidian-todo-quadrant
description: 扫描当日 Daily Note，按重要/紧急四象限整理任务清单
triggers: ["/todo", "/任务", "四象限"]
tags: ["obsidian", "task", "pkm"]
---

# /todo — 每日任务四象限整理

## 执行逻辑

### 第一步：定位今日 Daily Note
```bash
cd ~/Documents/Obsidian
TODAY=$(date +"%Y-%m-%d")
# 常见路径格式
find . -maxdepth 3 \( -name "*$TODAY*.md" -o -name "Daily*$TODAY*.md" \) 2>/dev/null
```

### 第二步：读取并解析任务
- 扫描 `#task`、`- [ ]`、`- [x]`、`1.`、`2.` 等任务标记
- 提取所有非完成状态的任务条目
- 识别 deadline、@person、⚠️ 等关键标签

### 第三步：四象限分类

| 象限 | 特征 | 处理原则 |
|------|------|---------|
| 🔴 Q1 紧急重要 | 有明确deadline或严重后果 | **立即执行** |
| 🟡 Q2 重要不紧急 | 长期目标相关 | **计划执行** |
| 🟢 Q3 紧急不重要 | 他人需求，可委托 | **尽快完成** |
| ⚪ Q4 不紧急不重要 | 闲聊、摸鱼项 | **删除或推迟** |

### 第四步：输出报告
将结果写入 `~/Documents/Obsidian/Inbox/TODO_Quadrant_Report.md`

报告格式：
```markdown
# TODO 四象限报告 — ${DATE}

## 🔴 Q1 紧急重要
-

## 🟡 Q2 重要不紧急
-

## 🟢 Q3 紧急不重要
-

## ⚪ Q4 可推迟/删除
-

## 📊 统计
- 总任务数：N
- 完成率：N/N
```

---

## 关键路径
- Obsidian 库：~/Documents/Obsidian/
- Inbox 输出：~/Documents/Obsidian/Inbox/TODO_Quadrant_Report.md
- Projects 目录：~/Documents/Obsidian/Projects/

## 注意事项
- 若找不到今日日记，返回警告
- 任务匹配尽量宽松，宁可多识别不要漏掉
- 报告写入前检查目录是否存在

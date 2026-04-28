---
name: obsidian-sync-prompt
description: 大规模笔记整理或技能更新后，主动提示用户通过 GitHub Desktop 提交知识沉淀
triggers: ["大规模整理", "skill更新", "知识沉淀"]
tags: ["obsidian", "github", "sync", "automation"]
---

# 自动化同步提示

## 触发条件
每当我完成以下操作之一时，自动提示用户：

1. ✅ 创建或更新了任何 Skill
2. ✅ 进行了大规模笔记整理（5个文件以上）
3. ✅ 生成了健康报告/四象限报告
4. ✅ 更新了 Obsidian 核心配置文件
5. ✅ 新增了超过3个笔记文件

## 提示文案

```
🎯 知识沉淀已就绪

已记录：
- [变更类型]
- [涉及文件]

💡 请切换到 GitHub Desktop 提交本次更新。

路径：~/Documents/GitHub/AI-Agent-Skills/
快捷脚本：~/Desktop/hermes/sync_vault.sh
```

## 自动化程度
- **被动模式**：仅在用户询问"有什么新进展"时提示
- **主动模式**：立即提示（仅限大规模变更）

## GitHub 提交规范
```
[技能更新] / [笔记整理] / [系统配置] — YYYY-MM-DD

变更摘要：
- 
```

## 关键路径
- 同步脚本：~/Desktop/hermes/sync_vault.sh
- 技能目录：~/.hermes/skills/
- GitHub 仓库：~/Documents/GitHub/AI-Agent-Skills/
- 软链接：~/Documents/GitHub/AI-Agent-Skills/Obsidian_Vault → ~/Documents/Obsidian/

---

## 完整同步流程（执行步骤）

当用户触发 `/sync` 或同意同步时，执行以下步骤：

### Step 1 — 检查变更
```bash
cd ~/Documents/GitHub/AI-Agent-Skills
git status --short
```

### Step 2 — 添加所有变更（含软链接）
```bash
git add Obsidian_Vault
# 若有其他变更：
git add .
```

### Step 3 — 提交
```bash
git commit -m "[分类] 变更摘要 — YYYY-MM-DD"
# 分类：[技能更新] / [笔记整理] / [系统配置] / [知识沉淀]
```

### Step 4 — 推送到 GitHub
```bash
git push origin main
```

### 完整一键脚本（~/Desktop/hermes/sync_vault.sh）
```bash
#!/bin/bash
VAULT_PATH="$HOME/Documents/Obsidian/Projects/"
REPO_PATH="$HOME/Documents/GitHub/AI-Agent-Skills"
echo "🚀 开始同步..."
[ ! -L "$REPO_PATH/Obsidian_Vault" ] && ln -s "$VAULT_PATH" "$REPO_PATH/Obsidian_Vault"
cd "$REPO_PATH"
git pull origin main
git status --short
echo "💡 请切换到 GitHub Desktop 完成最终推送。"
```

## 备注
- 软链接本身会被 git 追踪（模式 120000）
- Obsidian_Vault 是指向 ~/Documents/Obsidian 的 symlink
- 推送到 https://github.com/leonkangxi-dev/AI-Agent-Skills

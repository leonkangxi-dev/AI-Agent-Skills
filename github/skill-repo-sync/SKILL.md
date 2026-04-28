---
name: skill-repo-sync
description: 将 ~/.hermes/skills/ 同步到 ~/Documents/GitHub/AI-Agent-Skills/ 并推送到 GitHub。处理符号链接、嵌入式 git 仓库排除、以及 GitHub Desktop 凭证不可用的问题。
trigger: 每当技能被创建、修改，或需要同步到 GitHub 时
category: github
---

# Skill Sync — 技能同步到 GitHub 仓库

将本地技能文件夹同步到 GitHub 仓库 `~/Documents/GitHub/AI-Agent-Skills/` 并推送。

## 已知问题与解决方案

### 1. 符号链接问题
**问题：** `git add <symlink_dir>` → `fatal: pathspec 'xxx/' is beyond a symbolic link`  
**解决：** 不要使用符号链接，直接复制实际文件：
```bash
# 错误做法
ln -s ~/.hermes/skills DarkNight_Skills  # 会导致 git add 失败

# 正确做法
cp -R ~/.hermes/skills/ ~/Documents/GitHub/AI-Agent-Skills/
```

### 2. 嵌入式 git 仓库
**问题：** `openclaw-imports/` 下有嵌套的 `.git` 目录，git 会警告并拒绝包含  
**解决：** 添加前先排除：
```bash
git rm --cached -r openclaw-imports/slowmist-agent-security openclaw-imports/taste-skill 2>/dev/null
```

### 3. GitHub Desktop 凭证不可用
**问题：** `git push` → `could not read Username for 'https://github.com': Device not configured`  
**原因：** GitHub Desktop 的凭证库无法被终端 git 访问  
**解决：** 使用 `gh auth login` 授权（一次性操作）：
```bash
gh auth login --hostname github.com
# 选择 HTTPS + Web 浏览器授权
```
之后即可在终端直接 `git push`。

## 完整同步流程

```bash
REPO=~/Documents/GitHub/AI-Agent-Skills

# 1. 拉取最新
cd $REPO && git pull origin main

# 2. 同步技能文件（用复制，不用符号链接）
cp -R ~/.hermes/skills/ $REPO/

# 3. 进入仓库
cd $REPO

# 4. 排除嵌入式 git 仓库
git rm --cached -r openclaw-imports/slowmist-agent-security openclaw-imports/taste-skill 2>/dev/null

# 5. 添加所有文件
git add -A

# 6. 提交（自动附带日期时间）
git commit -m "sync: skills update — $(date '+%Y-%m-%d %H:%M')"

# 7. 推送
git push origin main
```

## 验证

```bash
# 确认提交成功
git log --oneline -1

# 确认 GitHub 上已更新
open https://github.com/leonkangxi-dev/AI-Agent-Skills
```

## 依赖

- `gh` CLI（用于授权）
- GitHub Desktop 已安装（已有凭证但需 CLI 授权）

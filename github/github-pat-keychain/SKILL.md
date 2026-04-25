---
name: github-pat-keychain
description: 在 macOS + GitHub Desktop 环境下，通过 PAT + git credential 存入 macOS Keychain，完成 git push，适用于终端无浏览器交互的 headless 场景。
trigger: git push 报错 "could not read Username" 且 gh auth login 设备码流程超时
category: github
---

# GitHub PAT → macOS Keychain 安全推送（macOS + GitHub Desktop）

## 问题症状

```
fatal: could not read Username for 'https://github.com': Device not configured
```

- `gh auth login` 设备码流程在非交互终端（PTY）中超时
- GitHub Desktop 的凭证库无法被 CLI git 直接访问
- `gh auth status` 可能仍显示未登录（gh 与 git 用不同的凭证存储）

## 解决方案：PAT + git credential 存储到 macOS Keychain

### Step 1：生成 PAT

1. 打开 https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾选 scopes：
   - `repo`（必须）
   - `read:org`（`gh auth login --with-token` 必须，否则报错 missing required scope）
   - `workflow`（可选）
4. 保存 token（格式：`ghp_xxx`）

### Step 2：把 PAT 存入 macOS Keychain

```bash
git credential fill << 'EOF'
protocol=https
host=github.com
username=<your-github-username>
password=<your-PAT>
EOF

git credential approve << 'EOF'
protocol=https
host=github.com
username=<your-github-username>
password=<your-PAT>
EOF
```

这会将 PAT 写入 macOS **Keychain Access**（非文件存储），GitHub Desktop 和 CLI git 共用同一把钥匙串。

### Step 3：还原远程 URL（移除明文 token）

如果之前设置了带 PAT 的远程 URL：
```bash
git remote set-url origin https://github.com/<owner>/<repo>.git
```

### Step 4：验证

```bash
git push origin main
# 成功且无密码提示 = 凭证已正确存储
```

## 快速验证凭证是否在 Keychain 中

```bash
security find-internet-password -s github.com 2>&1
# 找到记录 = 成功存入钥匙串
```

## 注意事项

- 绝对不要在 `git remote set-url` 中长期保留明文 PAT
- `gh auth login --insecure-storage` 会把 token 存明文文件，不推荐
- 如果 `gh auth status` 仍显示未登录但 push 成功，说明 git 用自己的 keychain 凭证，跟 `gh` CLI 无关，不要重复认证
- 首次认证完成后，后续 push 无需任何手动操作

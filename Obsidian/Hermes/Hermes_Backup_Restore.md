# Hermes Agent 备份恢复完整指南

## 备份信息

| 项目 | 值 |
|------|-----|
| 备份日期 | 2026-04-28 |
| 备份版本 | v0.11.0 (2026.4.23) |
| Git Commit | df51ad79 |
| 备份路径 | ~/Desktop/hermesbakup/hermes-agent_bak_20260428 |
| 备份大小 | 1.2GB |
| 备份方法 | ditto |

## 备份内容

- [x] 完整源代码（含 Git 仓库）
- [x] venv 虚拟环境
- [x] 内置 skills
- [x] 插件目录 plugins/
- [x] TUI 前端代码
- [x] 测试套件
- [ ] 配置文件（需单独备份）
- [ ] 用户 skills（需单独备份）
- [ ] Cron 任务（需单独备份）

## 恢复脚本

| 脚本 | 用途 | 路径 |
|------|------|------|
| restore_hermes.sh | 覆盖当前版本回滚 | ~/Desktop/hermesbakup/ |
| restore_fresh.sh | 新机器完整恢复 | ~/Desktop/hermesbakup/ |

## 快速恢复命令

### 方式一：覆盖恢复（当前机器回滚）

```bash
cd ~/Desktop/hermesbakup
./restore_hermes.sh
```

### 方式二：新机器恢复

```bash
cd ~/Desktop/hermesbakup
./restore_fresh.sh
```

### 方式三：Git 回滚（仅代码）

```bash
cd ~/.hermes/hermes-agent

# 回滚到备份版本
git reset --hard df51ad79

# 或回滚到指定版本
git reset --hard v0.10.0
```

## 全新安装步骤（未安装过 Hermes）

### 1. 安装依赖

```bash
# macOS
xcode-select --install
brew install git python@3.11

# Linux
apt-get update && apt-get install git python3.11 python3.11-venv
```

### 2. 克隆 Hermes Agent

```bash
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
```

### 3. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 4. 配置

```bash
# 复制配置模板
cp cli-config.yaml.example ~/.hermes/config.yaml

# 编辑配置
nano ~/.hermes/config.yaml
```

### 5. 验证

```bash
hermes --version
hermes doctor
```

## 新机器从备份恢复

### 1. 传输备份文件

将整个 `~/Desktop/hermesbakup/` 文件夹复制到新机器的相同位置。

### 2. 执行恢复脚本

```bash
cd ~/Desktop/hermesbakup
chmod +x restore_fresh.sh
./restore_fresh.sh
```

### 3. 配置 API Key

```bash
nano ~/.hermes/config.yaml
# 或
hermes setup
```

## 单独备份重要配置

在重装系统前，建议单独备份：

```bash
# 配置文件
cp ~/.hermes/config.yaml ~/Desktop/hermesbakup/config_backup.yaml

# 环境变量
cp ~/.hermes/.env ~/Desktop/hermesbakup/env_backup

# 用户 skills
cp -r ~/.hermes/skills ~/Desktop/hermesbakup/user_skills_backup

# Cron 任务
crontab -l > ~/Desktop/hermesbakup/crontab_backup.txt
```

## 常见问题

### Q1: 提示 "command not found: hermes"

```bash
# 检查 PATH
echo $PATH

# 或手动添加到 shell 配置
echo 'export PATH="$HOME/.hermes/hermes-agent:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Q2: Python 版本不兼容

```bash
# 需要 Python 3.11+
python3 --version

# macOS 使用 pyenv
brew install pyenv
pyenv install 3.11.15
pyenv global 3.11.15
```

### Q3: 权限错误

```bash
chmod +x ~/.hermes/hermes-agent/venv/bin/hermes
pip install -e . --force-reinstall
```

### Q4: API Key 无效

```bash
# 检查配置
cat ~/.hermes/config.yaml

# 或环境变量
echo $OPENAI_API_KEY

# 重新配置
hermes setup
```

## 元数据

- **创建日期**: 2026-04-28
- **备份版本**: Hermes Agent v0.11.0 (2026.4.23)
- **备份 commit**: df51ad79
- **文档路径**: ~/Desktop/hermesbakup/FULL_RESTORE_GUIDE.md

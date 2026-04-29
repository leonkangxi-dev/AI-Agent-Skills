# Hermes Agent 备份恢复

## 文档列表

- [[Hermes_Backup_Restore]] - 完整备份恢复指南（全新安装/回滚/新机器恢复）
- [[Hermes_Agent_Info]] - 当前安装信息

## 备份文件位置

- 备份目录：~/Desktop/hermesbakup/
- 备份内容：完整 Hermes Agent v0.11.0 (2026.4.23)

## 快速恢复

```bash
# 覆盖恢复（当前机器）
cd ~/Desktop/hermesbakup && ./restore_hermes.sh

# 新机器恢复
cd ~/Desktop/hermesbakup && ./restore_fresh.sh
```

## 更新日志

- 2026-04-28：创建备份，版本 v0.11.0

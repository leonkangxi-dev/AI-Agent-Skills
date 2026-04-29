# 深夜日志固化协议 - 技术文档

**创建时间:** 2026-04-23
**状态:** ✅ 已部署
**执行者:** 暗夜匿影 🌑

---

## 一、协议概述

『深夜日志固化协议』确保每日工作成果得到规范归档，形成完整的知识积累链条。

| 项目 | 内容 |
|------|------|
| **触发时间** | 每日 23:30 |
| **执行方式** | crontab 定时任务 |
| **归档路径** | `~/Documents/Obsidian/90_System/Daily_Logs/YYYY/MM/` |
| **文件名** | `YYYY-MM-DD_Work_Log.md` |

---

## 二、架构设计

### 2.1 组件

| 组件 | 路径 | 说明 |
|------|------|------|
| **固化脚本** | `~/.openclaw/workspace/services/daily_log_consolidate.py` | 核心逻辑 |
| **定时触发器** | `~/.openclaw/workspace/services/consolidate_cron.sh` | crontab 包装 |
| **守护进程** | crontab `30 23 * * *` | 每日 23:30 触发 |

### 2.2 执行流程

```
23:30 (crontab) 
  → consolidate_cron.sh
  → daily_log_consolidate.py
  → 收集当日事件
  → 归档到 Obsidian Daily_Logs
  → 生成明日待办
```

---

## 三、核心功能

### 3.1 数据收集

| 数据源 | 内容 |
|--------|------|
| **memory/*.md** | 当日会话日志 |
| **Git 日志** | Project_Lucid_Japanese, Project_Iris_FM |
| **系统统计** | 服务状态、下载数量、内存占用 |
| **OpenClaw 历史** | 会话事件提取 |

### 3.2 容错机制

**延迟归档规则:**
- 如果 23:30 时系统 down 掉
- 守护进程启动后 10 分钟内自动补录
- 标注 `[延迟归档]` 标签

### 3.3 日志格式

```markdown
# YYYY-MM-DD 深夜工作日志

**归档时间:** 23:30
**状态:** ✅ 已归档 / ⚠️ 延迟归档

## 📊 当日汇总

### 📚 Project_Lucid_Japanese
(git log)

### 📱 Project_Iris_FM
(git log)

## 🔮 明日待办
- [ ] ...
```

---

## 四、crontab 配置

```cron
30 23 * * * /bin/bash ~/.openclaw/workspace/services/consolidate_cron.sh
```

---

## 五、补录机制代码

```python
def consolidate():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = archive_dir / f"{today}_Work_Log.md"
    
    # 检查是否延迟归档
    if datetime.now().hour >= 0 and log_file.exists():
        with open(log_file, 'r') as f:
            content = f.read()
        if '延迟归档' not in content:
            # 首次归档
            pass
        else:
            # 延迟归档，不覆盖原有数据
            pass
```

---

## 六、相关文件

| 文件 | 路径 |
|------|------|
| 固化脚本 | `~/.openclaw/workspace/services/daily_log_consolidate.py` |
| 定时触发 | `~/.openclaw/workspace/services/consolidate_cron.sh` |
| 日志输出 | `~/.logs/daily_consolidate.log` |
| 归档目录 | `~/Documents/Obsidian/90_System/Daily_Logs/` |

---

*文档归档时间: 2026-04-23 00:36*
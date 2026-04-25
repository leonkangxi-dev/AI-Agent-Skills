---
name: desktop-file-archiver
description: 暗夜桌面文件自动归档 —每当系统在桌面生成新的分析报告或 Log 文件时，自动捕获、按日期重命名并移动到 Obsidian 项目库。
trigger: 暗夜生成分析报告或 Log 文件后，或手动调用
category: productivity
---

# Desktop File Archiver — 暗夜桌面文件自动归档

## 触发条件

每当暗夜在系统桌面 (`~/Desktop/`) 生成新的分析报告或 Log 文件时，自动捕获、按日期重命名，并移动到 Obsidian 项目库。

## 监控范围

**文件类型匹配模式：**
- 分析报告: `~/Desktop/*分析*.{md,pdf,txt,docx}`
- Log 文件: `~/Desktop/*.log`, `~/Desktop/*_log_*`, `~/Desktop/*LOG*`
- 暗夜输出: `~/Desktop/暗夜_*`, `~/Desktop/*_report_*`
- 时间戳文件: `~/Desktop/*[0-9]{8}*`（如 `20260425`）

**目标 Obsidian 库路径：**
```
~/Documents/Obsidian/90_System/Inbox/
```

## 归档规则

1. **扫描桌面**：获取上次检查之后新建或修改的文件
2. **重命名格式**：`{YYYYMMDD}_{原始文件名}`
   - 示例：`20260425_系统分析报告.md`
3. **移动目标**：`~/Documents/Obsidian/90_System/Inbox/{YYYYMMDD}_{原始文件名}`
4. **记录锚点**：更新 `~/.hermes/last_archive_check` 时间戳

## 执行脚本

```python
import os, shutil, glob, time
from datetime import datetime

desktop = os.path.expanduser("~/Desktop")
inbox = os.path.expanduser("~/Documents/Obsidian/90_System/Inbox")
timestamp_file = os.path.expanduser("~/.hermes/last_archive_check")

os.makedirs(inbox, exist_ok=True)

if os.path.exists(timestamp_file):
    with open(timestamp_file) as f:
        last_check = float(f.read().strip())
else:
    last_check = 0

patterns = ["*分析*", "*.log", "*_log_*", "暗夜_*", "*_report_*"]
new_files = []

for pat in patterns:
    for f in glob.glob(os.path.join(desktop, pat)):
        if os.path.getmtime(f) > last_check and os.path.isfile(f):
            new_files.append(f)

if new_files:
    print(f"发现 {len(new_files)} 个新文件:")
    for src in new_files:
        fname = os.path.basename(src)
        date_prefix = datetime.now().strftime("%Y%m%d")
        new_name = f"{date_prefix}_{fname}"
        dst = os.path.join(inbox, new_name)
        shutil.move(src, dst)
        print(f"  ✓ {fname} → {new_name}")
    with open(timestamp_file, "w") as f:
        f.write(str(time.time()))
else:
    print("未发现新文件需归档。")
```

## 验证步骤

归档完成后：
1. `ls ~/Documents/Obsidian/90_System/Inbox/ | grep {今天日期}` 确认文件存在
2. 在 Obsidian 中搜索 `{今天日期}` 确认已入库

## 注意事项

- 仅移动，不复制；原文件从桌面移除
- 重复运行同一批文件不会重复移动（基于 mtime 判断）
- 如桌面文件已按日期命名，自动保留原日期前缀

# Daemon Setup - 守护进程配置

**创建日期:** 2026-04-21
**项目:** Project_Night_Ops

---

## com.openclaw.nightly.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.nightly</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/opt/node@22/bin/node</string>
        <string>/usr/local/lib/node_modules/openclaw/dist/index.js</string>
        <string>gateway</string>
        <string>--port</string>
        <string>18789</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/tmp/openclaw/nightly_stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw/nightly_stderr.log</string>
    
    <key>WorkingDirectory</key>
    <string>/Users/jiang/.openclaw</string>
</dict>
</plist>
```

---

## 安装路径

- **plist文件:** `~/Library/LaunchAgents/com.openclaw.nightly.plist`
- **工作目录:** `~/Library/LaunchAgents/`

---

## 加载命令

```bash
# 加载（启动）
launchctl load ~/Library/LaunchAgents/com.openclaw.nightly.plist

# 卸载（停止）
launchctl unload ~/Library/LaunchAgents/com.openclaw.nightly.plist

# 查看状态
launchctl list | grep openclaw
```

---

## 功能说明

| 参数 | 说明 |
|------|------|
| RunAtLoad | 加载后立即启动 |
| KeepAlive | 进程退出后自动重启 |
| ProcessType | Interactive（交互式进程） |

---

## 验证

```bash
# 检查是否加载
launchctl list | grep nightly

# 查看日志
tail -f /tmp/openclaw/nightly_stdout.log
```

---

*由暗夜匿影自动记录*
*2026-04-21*
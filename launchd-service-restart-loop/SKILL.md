---
name: launchd-service-restart-loop
description: 诊断并终止 macOS launchd 管理的进程启动死循环，适用于 Hermes Gateway、OpenClaw Gateway 等服务 CPU 异常飙升至 100%+ 且不断重启的情况。
---

# Launchd Service Restart Loop

## 适用场景
- 进程 CPU 飙升至 100%+ 且不断重启
- kill -9 后进程又出现
- launchctl stop 无效

## 诊断
```bash
# 找到 launchd job
launchctl list | grep <关键词>

# 确认高 CPU 进程
ps aux | grep <关键词> | grep -v grep
```

## 解决步骤

### 1. 找到 job label
`launchctl list` 输出第三列即为 job label（不是 PID）

### 2. bootout 彻底移除
```bash
launchctl bootout gui/$(id -u)/<job-label>
```
**注意**: `kill -9` 和 `launchctl stop` 都无效，必须用 bootout

### 3. 验证
```bash
ps aux | grep <关键词>      # 应无输出
launchctl list | grep <关键词>  # 应无输出
```

## 经验记录
- Hermes Gateway CPU 异常: job label = `ai.hermes.gateway`
- OpenClaw Gateway CPU 异常: job label = `ai.openclaw.gateway`, `com.openclaw.nightly`

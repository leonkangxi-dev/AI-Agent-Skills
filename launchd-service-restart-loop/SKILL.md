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

## 关键教训：端口冲突会导致启动死循环

**现象**：进程 CPU 100%+，不断重启，日志显示 `EADDRINUSE: address already in use`

**根因**：系统上存在 **两个 launchd job**（不同 label，不同 plist）绑定同一端口，互相抢占
- 示例：`ai.openclaw.gateway`（Node 24）与 `com.openclaw.nightly`（Node 22）同时绑定 18789
- 其中一个启动失败，launchd 的 `KeepAlive: true` 立刻在 1 秒后重拉，形成死循环

**诊断**：
```bash
# 检查端口占用
lsof -i :<端口号>

# 检查所有 openclaw 相关 job（label 才是唯一标识）
launchctl list | grep openclaw
```

**解决**：保留一个，删除其余所有
```bash
# 1. 确认要保留的 label
launchctl list | grep openclaw

# 2. bootout 所有要删除的 job
launchctl bootout gui/$(id -u)/<job-label>

# 3. 删除对应 plist 文件（防止重启后复活）
rm ~/Library/LaunchAgents/<problematic-plist>.plist

# 4. 验证只剩一个，CPU 应降至 <10%
ps aux | grep <关键词>
```

**禁止**：不要只 `kill -9` 或只 `launchctl stop`——看门狗会在 1 秒内拉起新进程

---
name: system-healthcheck
description: 全面系统自检 - 检查服务状态、端口、资源、日志、Telegram Bot、Skills可用性等
---

# System Health Check Skill

## 功能

执行全面的系统自检，涵盖：

### 1. 端口服务检查
- 检查关键端口运行状态
- 端口：3000, 5002, 7890, 18789, 6379, 57311

### 2. 资源使用
- CPU 使用率
- 内存使用情况
- 磁盘空间

### 3. 网络连通性
- Telegram Bot API
- 外部网络连接

### 4. 服务进程
- OpenClaw Gateway
- Night_Watcher 守护进程
- Clash 代理

### 5. Skills 可用性
- 列出所有已部署 Skills
- 检查关键 Skills 状态

### 6. 日志检查
- 最近的系统日志异常

## 使用方法

直接执行自检：
```
执行系统自检
```

或指定检查项：
```
检查端口服务状态
检查资源使用
检查 Telegram Bot
```

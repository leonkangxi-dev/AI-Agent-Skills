# Health Check Logic - 自检逻辑说明

**创建日期:** 2026-04-21
**文件位置:** `~/Documents/Obsidian/90_System/health_check.py`

---

## 核心配置

```python
CHECK_INTERVAL = 300    # 5分钟检测一次
CPU_THRESHOLD = 80      # CPU阈值80%
MEMORY_THRESHOLD = 80   # 内存阈值80%
```

---

## 检测端口列表

| 端口 | 服务 |
|------|------|
| 3000 | 命令控制塔 |
| 5000 | 企业管理看板 |
| 5001 | 情报中心 |
| 5002 | FM App |
| 9996 | 火种API |
| 9997 | 自愈核心 |
| 9998 | 大脑心跳 |
| 18789 | OpenClaw Gateway |

---

## 检测逻辑

### 1. 端口响应检测
```python
def check_port(port):
    result = subprocess.run(
        ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 
         f'http://localhost:{port}', '--max-time', '3']
    )
    return result.stdout.strip() == '200'
```

### 2. 进程存活检测
```python
def check_process(name):
    for proc in psutil.process_iter(['name', 'cmdline']):
        if name.lower() in proc.name().lower():
            return True
    return False
```

### 3. 系统负载检测
```python
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return {'cpu': cpu, 'memory_percent': memory.percent}
```

---

## 响应动作

| 检测结果 | 执行操作 |
|----------|----------|
| CPU > 80% | 清理 `__pycache__` 和过期日志 |
| 内存 > 80% | 清理缓存 |
| 端口无响应 | 调用 `restart_service(port)` |
| OpenClaw进程消失 | 调用 `restart_openclaw()` |

---

## 冷启动恢复流程

1. **LaunchAgent 触发** → macOS 启动时自动加载 `com.openclaw.nightly.plist`
2. **Gateway 启动** → OpenClaw Gateway 监听 18789 端口
3. **自检脚本启动** → 加载 `health_check.py` 后台运行
4. **服务检测** → 逐个检测 3000/5000/5001/5002 端口
5. **自动拉起** → 无响应端口自动启动对应服务

---

## 启动自检脚本

```bash
# 后台启动
nohup python3 ~/Documents/Obsidian/90_System/health_check.py > ~/logs/health_check.log 2>&1 &

# 查看日志
tail -f ~/logs/health_check.log
```

---

*由暗夜匿影自动记录*
*2026-04-21*
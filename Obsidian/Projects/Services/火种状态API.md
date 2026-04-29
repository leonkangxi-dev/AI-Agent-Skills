# 火种状态API

**路径:** `~/.openclaw/workspace/services/fire_seed_api.py`  
**端口:** 9996  
**状态:** 🟢 运行中  
**归档时间:** 2026-04-23

---

## 一、概述

火种状态API 为系统核心监控接口，提供火种镜像状态的实时查询。

## 二、接口

| 端点 | 方法 | 返回 |
|------|------|------|
| `/status` | GET | JSON 状态数据 |

### 返回示例

```json
{
    "service": "fire_seed_api",
    "status": "active",
    "timestamp": "2026-04-23T00:43:00",
    "port": 9996
}
```

## 三、代码

```python
#!/usr/bin/env python3
"""火种状态API - 端口9996"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "service": "fire_seed_api",
                "status": "active",
                "timestamp": datetime.now().isoformat(),
                "port": 9996
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print("🔥 火种状态API 启动于端口 9996")
    HTTPServer(('127.0.0.1', 9996), Handler).serve_forever()
```

## 四、快速访问

```
http://127.0.0.1:9996/status
```
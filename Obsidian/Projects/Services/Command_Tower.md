# Command Tower

**路径:** `~/.openclaw/workspace/services/command_tower_web.py`  
**端口:** 3000  
**状态:** 🟢 运行中  
**归档时间:** 2026-04-23

---

## 一、概述

Command Tower 提供指挥中心 Web 界面，基于 `command_tower_v2.html`。

## 二、快速访问

```
http://127.0.0.1:3000/command_tower_v2.html
```

## 三、相关文件

| 文件 | 路径 |
|------|------|
| 启动脚本 | `services/command_tower_web.py` |
| 前端界面 | `evolution/command_tower_v2.html` |

## 四、代码

```python
#!/usr/bin/env python3
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

class H(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/Users/jiang/.openclaw/workspace', **kwargs)

print('Starting Command Tower on port 3000')
HTTPServer(('0.0.0.0', 3000), H).serve_forever()
```
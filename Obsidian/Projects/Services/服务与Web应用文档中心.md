# 服务与 Web 应用文档中心

**更新时间:** 2026-04-23
**归档状态:** ✅ 全面归档

---

## 一、核心服务总览

| 服务名 | 端口 | 路径 | 归档 | Obsidian 路径 |
|--------|------|------|------|------|
| 火种状态API | 9996 | `services/fire_seed_api.py` | ✅ | 见下方 |
| 自愈核心 | 9997 | `services/self_heal_core.py` | ✅ | 见下方 |
| 大脑心跳 | 9998 | `services/brain_heartbeat.py` | ✅ | 见下方 |
| 企业管理看板 | 5000 | `services/enterprise_dashboard.py` | ✅ | 见下方 |
| 情报中心 | 5001 | `services/intelligence_center.py` | ✅ | 见下方 |
| Linkage Observer | 3000 | `services/linkage_web.py` | ✅ | 见下方 |
| Command Tower | 3000 | `services/command_tower_web.py` | ✅ | 见下方 |
| 记忆自动更新 | - | `services/memory_auto_update.py` | ✅ | 见下方 |
| 记忆固化 | - | `services/memory_consolidate.py` | ✅ | 见下方 |
| 记忆索引 | - | `services/memory_indexer.py` | ✅ | 见下方 |
| 记忆检索 | - | `services/memory_search.py` | ✅ | 见下方 |
| 日志固化 | - | `services/daily_log_consolidate.py` | ✅ | 见下方 |
| 服务重启脚本 | - | `services/restart_all.sh` | ✅ | 见下方 |
| Command Tower UI | / | `evolution/command_tower_v2.html` | ✅ | 见下方 |
| X 文章代理 | / | `x_proxy_article.html` | ✅ | 见下方 |

---

## 二、各服务详情

### 2.1 火种状态 API

**路径:** `~/.openclaw/workspace/services/fire_seed_api.py`  
**端口:** 9996  
**功能:** 火种镜像状态查询  
**归档:** ✅  
**Obsidian:** `Projects/Services/火种状态API.md`

### 2.2 自愈核心

**路径:** `~/.openclaw/workspace/services/self_heal_core.py`  
**端口:** 9997  
**功能:** 系统自愈与异常检测  
**归档:** ✅  
**Obsidian:** `Projects/Services/自愈核心.md`

### 2.3 大脑心跳

**路径:** `~/.openclaw/workspace/services/brain_heartbeat.py`  
**端口:** 9998  
**功能:** 大脑链路健康检测  
**归档:** ✅  
**Obsidian:** `Projects/Services/大脑心跳.md`

### 2.4 企业管理看板

**路径:** `~/.openclaw/workspace/services/enterprise_dashboard.py`  
**端口:** 5000  
**功能:** 企业管理看板 Web UI  
**归档:** ✅  
**Obsidian:** `Projects/Services/企业管理看板.md`

### 2.5 情报中心

**路径:** `~/.openclaw/workspace/services/intelligence_center.py`  
**端口:** 5001  
**功能:** 情报数据采集与展示  
**归档:** ✅  
**Obsidian:** `Projects/Services/情报中心.md`

### 2.6 Linkage Observer + Command Tower

**路径:** `~/.openclaw/workspace/services/command_tower_web.py`  
**端口:** 3000  
**功能:** Command Tower Web 界面  
**归档:** ✅  
**Obsidian:** `Projects/Services/Command_Tower.md`

---

### 2.5 FM App

**路径:** `~/Documents/Obsidian/Projects/FM_App/代码/app.py`
**端口:** 5002
**状态:** 🟢 运行中
**归档:** ✅
**Obsidian:** `Projects/FM_App/`

**电台列表 (2026-04-23 更新):**
| 名称 | URL | 状态 |
|------|------|------|
| CCTV-1 | cd-live-stream.news.cctvplus.com | 🟢 |
| CCTV-2 | cd-live-stream.news.cctvplus.com | 🟢 |
| 央视新闻 | live.baidu.com | 🟢 |
| 中国教育1台 | live.baidu.com | 🟢 |
| CCTV-4 | live.baidu.com | 🟢 |
| 湖南卫视 | live.baidu.com | 🟢 |
| 浙江卫视 | live.baidu.com | 🟢 |
| 江苏卫视 | live.baidu.com | 🟢 |
| 东方卫视 | live.baidu.com | 🟢 |

**已失效 (删除):** 凤凰中文、RTHK TV 31、广东卫视、北京卫视、上海新闻、深圳卫视

---

## 三、快速访问

| 服务 | URL |
|------|-----|
| Command Tower | http://127.0.0.1:3000/command_tower_v2.html |
| 企业管理看板 | http://127.0.0.1:5000/ |
| 情报中心 | http://127.0.0.1:5001/ |
| 火种状态API | http://127.0.0.1:9996/ |
| 自愈核心 | http://127.0.0.1:9997/ |
| 大脑心跳 | http://127.0.0.1:9998/ |

---

*归档时间: 2026-04-23 00:43*
# FM App 开发日志

## 2026-04-16 工程化部署阶段

### 需求分析
- 将静态 HTML 改造成服务化应用
- 支持内网访问
- 修复播放逻辑问题
- 增加管理员后台

### 后端架构
- **框架**: Flask (轻量级)
- **端口**: 5002
- **存储**: SQLite 数据库
- **API**: RESTful

### 已完成任务
- [x] 创建 Dev_Log.md
- [x] Flask 服务搭建
- [x] 播放逻辑修复 (CORS + HLS.js)
- [x] 管理员后台
- [x] 播放列表浮层
- [x] 服务已启动 (端口 5002)

### API 设计
| 端点 | 方法 | 功能 |
|------|------|------|
| /api/channels | GET | 获取频道列表 |
| /api/channels | POST | 添加频道 |
| /api/channels/:id | PUT | 更新频道 |
| /api/channels/:id | DELETE | 删除频道 |
| /api/admin/login | POST | 管理员登录 |
| /api/admin/admins | GET | 获取管理员列表 |
| /api/admin/admins | POST | 添加管理员 |
| /api/admin/admins/:id | DELETE | 删除管理员 |

### Bug 修复记录
1. CORS 跨域问题 → 已配置 flask-cors
2. 流媒体格式兼容性 → 使用 HLS.js 处理
3. 播放索引逻辑 → 已修复循环切换
4. Socket IP获取 → 已修复使用connect方式

### 内网访问
- **播放器**: http://192.168.3.197:5002
- **管理后台**: http://192.168.3.197:5002/admin
- **账号**: admin / admin

---
*更新: 2026-04-16 09:15*

## 2026-04-23 电台链接全面检测与更新

### 一、执行背景

FM App 原内置 8 个默认电台（存储在代码 default_channels），大量链接已失效（500/404错误）。

### 二、检测方法

**工具:** Python ThreadPoolExecutor + curl
**超时:** 5秒/URL
**状态码判断:** HTTP 200/301/302 = 🟢 可用

### 三、原有电台检测结果

| 电台 | URL | 结果 |
|------|-----|------|
| CCTV-1 | cd-live-stream.news.cctvplus.com | 🟢 可用 |
| CCTV-2 | cd-live-stream.news.cctvplus.com | 🟢 可用 |
| 凤凰中文 | pluton.liveradio.cn | 🔴 500 |
| RTHK TV 31 | rthk.hk | 🔴 超时 |
| 广东卫视 | cdn4.skygo.mn | 🔴 500 |
| 北京卫视 | cdn4.skygo.mn | 🔴 404 |
| 上海新闻 | streamlive.shbst.cn | 🔴 超时 |
| 深圳卫视 | cdn4.skygo.mn | 🔴 500 |

**可用率: 2/8 (25%)**

### 四、新电台搜索

**搜索方向:**
1. 央视 CCTV+ 系列 (cd-live-stream.news.cctvplus.com)
2. 百度直播 (live.baidu.com) — 来源稳定
3. 地方卫视 CDN

**搜索结果:**

| 电台 | URL | 结果 |
|------|-----|------|
| 央视新闻 | live.baidu.com stream_src_id=1 | 🟢 可用 |
| 中国教育1台 | live.baidu.com stream_src_id=8 | 🟢 可用 |
| CCTV-4 | live.baidu.com stream_src_id=10 | 🟢 可用 |
| 湖南卫视 | live.baidu.com stream_src_id=5 | 🟢 可用 |
| 浙江卫视 | live.baidu.com stream_src_id=7 | 🟢 可用 |
| 江苏卫视 | live.baidu.com stream_src_id=6 | 🟢 可用 |
| 东方卫视 | live.baidu.com stream_src_id=4 | 🟢 可用 |
| 凤凰中文 | pili-live-hd.ifeng.com | 🔴 |
| RTHK 31 | rthk.hk | 🔴 |
| TVB 新闻 | news.hk.msdesign.net | 🔴 |
| 央视CCTV-5/6/7 | cd-live-stream.news.cctvplus.com | 🔴 |

**成功率: 7/13 (54%)**

### 五、更新结果

**删除失效电台 (6个):**
- 凤凰中文、RTHK TV 31、广东卫视、北京卫视、上海新闻、深圳卫视

**新增可用电台 (7个):**
- 央视新闻、中国教育1台、CCTV-4
- 湖南卫视、浙江卫视、江苏卫视、东方卫视

**现有电台 (9个):**
- CCTV-1、CCTV-2 (央视原有)
- 央视新闻、中国教育1台、CCTV-4 (百度直播)
- 湖南卫视、浙江卫视、江苏卫视、东方卫视 (地方台)

### 六、技术要点

**数据存储:** SQLite (`fm_app.db`) 而非 JSON 文件
**更新方式:** 直接操作 DB — `DELETE FROM channels` + `INSERT`

**百度直播 URL 格式:**
```
https://live.baidu.com/live/livestream/channeldetail?stream_src_type=1&stream_src_id={id}
```

**央视 CCTV+ 系列 URL 格式:**
```
https://cd-live-stream.news.cctvplus.com/live/smil:CHANNEL{id}.smil/playlist.m3u8
```

### 七、下次检测建议

- 建议每2周执行一次电台链接检测
- 优先使用百度直播 (live.baidu.com) 作为稳定源
- 备用源: 央视 CCTV+ (cd-live-stream.news.cctvplus.com)

---

*归档时间: 2026-04-23 09:33*

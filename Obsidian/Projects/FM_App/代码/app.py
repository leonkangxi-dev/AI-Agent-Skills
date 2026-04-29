#!/usr/bin/env python3
"""
FM Radio App - Flask Backend
网络电台播放器后端服务
"""
import os
import json
import sqlite3
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/api/*": {"origins": "*"}})

PORT = 5002
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'channels.json')
ADMINS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'admins.json')
DB_FILE = os.path.join(os.path.dirname(__file__), 'data', 'fm_app.db')

# 确保 data 目录存在
os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 频道表
    c.execute('''CREATE TABLE IF NOT EXISTS channels 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  url TEXT NOT NULL,
                  group_name TEXT DEFAULT 'General')''')
    
    # 管理员表
    c.execute('''CREATE TABLE IF NOT EXISTS admins 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE NOT NULL, 
                  password TEXT NOT NULL)''')
    
    # 默认管理员
    c.execute("SELECT COUNT(*) FROM admins")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO admins (username, password) VALUES ('admin', 'admin')")
    
    # 初始化默认频道
    c.execute("SELECT COUNT(*) FROM channels")
    if c.fetchone()[0] == 0:
        default_channels = [
            ('CCTV-1', 'https://cd-live-stream.news.cctvplus.com/live/smil:CHANNEL1.smil/playlist.m3u8', 'CCTV'),
            ('CCTV-2', 'https://cd-live-stream.news.cctvplus.com/live/smil:CHANNEL2.smil/playlist.m3u8', 'CCTV'),
            ('凤凰中文', 'https://pluton.liveradio.cn/1001', '凤凰'),
            ('RTHK TV 31', 'https://rthk.hk/ls/live/rthktv31.m3u8', '香港'),
            ('广东卫视', 'https://cdn4.skygo.mn/live/disk1/Guangdong/HLSv3-FTA/Guangdong.m3u8', '广东'),
            ('北京卫视', 'https://cdn4.skygo.mn/live/disk1/Beijing/HLSv3-FTA/Beijing.m3u8', '北京'),
            ('上海新闻', 'https://streamlive.shbst.cn/live/cctv4.m3u8', '上海'),
            ('深圳卫视', 'https://cdn4.skygo.mn/live/disk1/Shenzhen/HLSv3-FTA/Shenzhen.m3u8', '深圳'),
        ]
        c.executemany("INSERT INTO channels (name, url, group_name) VALUES (?, ?, ?)", default_channels)
    
    conn.commit()
    conn.close()

# API: 获取频道列表
@app.route('/api/channels', methods=['GET'])
def get_channels():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM channels ORDER BY id")
    rows = c.fetchall()
    channels = [dict(row) for row in rows]
    conn.close()
    return jsonify({'channels': channels, 'total': len(channels)})

# 兼容前端旧版 /stations 端点
@app.route('/stations', methods=['GET'])
def get_stations():
    return get_channels()

# API: 添加频道
@app.route('/api/channels', methods=['POST'])
def add_channel():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO channels (name, url, group_name) VALUES (?, ?, ?)",
               (data['name'], data['url'], data.get('group_name', 'General')))
    conn.commit()
    channel_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': channel_id})

# API: 更新频道
@app.route('/api/channels/<int:channel_id>', methods=['PUT'])
def update_channel(channel_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE channels SET name=?, url=?, group_name=? WHERE id=?",
               (data['name'], data['url'], data.get('group_name', 'General'), channel_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# API: 删除频道
@app.route('/api/channels/<int:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM channels WHERE id=?", (channel_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# API: 管理员登录
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE username=? AND password=?", 
               (data['username'], data['password']))
    admin = c.fetchone()
    conn.close()
    
    if admin:
        return jsonify({'success': True, 'token': f'admin_{admin["id"]}'})
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

# API: 获取管理员列表
@app.route('/api/admin/admins', methods=['GET'])
def get_admins():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, username FROM admins")
    admins = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({'admins': admins})

# API: 添加管理员
@app.route('/api/admin/admins', methods=['POST'])
def add_admin():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
                  (data['username'], data['password']))
        conn.commit()
        return jsonify({'success': True})
    except:
        return jsonify({'success': False, 'error': 'Username exists'}), 400
    finally:
        conn.close()

# API: 删除管理员
@app.route('/api/admin/admins/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM admins WHERE id=? AND username != 'admin'", (admin_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# 静态文件服务
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/admin/')
def admin_index():
    return send_from_directory('static', 'admin/index.html')

@app.route('/admin/<path:path>')
def serve_admin(path):
    return send_from_directory('static/admin', path)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    init_db()
    
    # 获取内网IP
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = '127.0.0.1'
    
    print(f"\n🎙️ FM Radio App 已启动")
    print(f"📍 内网访问: http://{local_ip}:{PORT}")
    print(f"🔧 管理后台: http://{local_ip}:{PORT}/admin")
    print(f"👤 默认账号: admin / admin\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)

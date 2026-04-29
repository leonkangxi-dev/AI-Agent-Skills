#!/usr/bin/env python3
"""系统级生存守护 - 自检脚本"""
import os
import time
import subprocess
import psutil
import requests
from datetime import datetime

# 配置
CHECK_INTERVAL = 300  # 5分钟
CPU_THRESHOLD = 80  # CPU阈值
MEMORY_THRESHOLD = 80  # 内存阈值
PORTS = [3000, 5000, 5001, 5002, 9996, 9997, 9998, 18789]
LOG_FILE = os.path.expanduser("~/logs/health_check.log")

def log(msg):
    """日志记录"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def check_port(port):
    """检测端口响应"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 
             f'http://localhost:{port}', '--max-time', '3'],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() == '200'
    except:
        return False

def check_process(name):
    """检测进程是否存在"""
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else ''
            if name.lower() in proc.name().lower() or name in cmdline:
                return True
        except:
            pass
    return False

def restart_service(port):
    """重启服务"""
    log(f"🔄 尝试重启端口 {port}...")
    
    # 根据端口匹配服务
    if port == 5002:
        # FM App
        subprocess.run(
            'cd ~/Documents/Obsidian/Projects/FM_App/代码 && nohup python3 app.py > ~/logs/fm_app.log 2>&1 &',
            shell=True, executable='/bin/zsh'
        )
    elif port == 3000:
        subprocess.run(
            'cd ~/Documents/Obsidian/Projects/FM_App/代码 && nohup python3 -m http.server 3000 > /dev/null 2>&1 &',
            shell=True, executable='/bin/zsh'
        )
    # 添加其他端口重启逻辑...

def restart_openclaw():
    """重启OpenClaw"""
    log("🔄 重启 OpenClaw Gateway...")
    subprocess.run(['openclaw', 'gateway', 'restart'], capture_output=True)

def cleanup_cache():
    """清理缓存"""
    log("🧹 清理缓存...")
    
    # 清理 __pycache__
    subprocess.run('find ~/.openclaw/workspace -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null', 
                   shell=True)
    
    # 清理日志
    subprocess.run('find ~/logs -name "*.log" -mtime +7 -delete 2>/dev/null',
                   shell=True)
    
    log("✅ 清理完成")

def get_system_stats():
    """获取系统状态"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        'cpu': cpu,
        'memory_percent': memory.percent,
        'memory_used_gb': memory.used / (1024**3),
        'swap_percent': swap.percent
    }

def check_and_restart():
    """主检查逻辑"""
    stats = get_system_stats()
    log(f"📊 系统状态 - CPU: {stats['cpu']}% | 内存: {stats['memory_percent']}% | SWAP: {stats['swap_percent']}%")
    
    # 检查CPU/内存负载
    if stats['cpu'] > CPU_THRESHOLD:
        log(f"⚠️ CPU过高 ({stats['cpu']}%)，执行清理...")
        cleanup_cache()
    
    if stats['memory_percent'] > MEMORY_THRESHOLD:
        log(f"⚠️ 内存过高 ({stats['memory_percent']}%)，执行清理...")
        cleanup_cache()
    
    # 检查OpenClaw进程
    if not check_process('openclaw'):
        log("⚠️ OpenClaw进程未运行，尝试重启...")
        restart_openclaw()
    
    # 检查关键端口
    for port in PORTS:
        if not check_port(port):
            log(f"⚠️ 端口 {port} 无响应，尝试重启...")
            restart_service(port)

def main():
    log("="*50)
    log("🌑 系统级生存守护 启动")
    log("="*50)
    
    while True:
        try:
            check_and_restart()
        except Exception as e:
            log(f"❌ 检查出错: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
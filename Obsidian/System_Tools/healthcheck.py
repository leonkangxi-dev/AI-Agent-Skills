#!/usr/bin/env python3
"""
System Health Check - 系统自检脚本
"""
import os
import json
import subprocess
from datetime import datetime

def check_ports():
    """检查端口服务"""
    ports = {
        3000: "控制塔",
        5002: "FM电台",
        7890: "Clash代理",
        18789: "OpenClaw",
        6379: "Redis",
        57311: "OpenCode"
    }
    
    result = {}
    for port, name in ports.items():
        try:
            output = subprocess.run(
                ["lsof", "-i", f":{port}"],
                capture_output=True, text=True, timeout=5
            )
            result[port] = "✅ 运行中" if output.returncode == 0 else "❌ 未运行"
        except:
            result[port] = "⚠️ 检查失败"
    
    return result

def check_resources():
    """检查资源使用"""
    try:
        # CPU
        cpu = subprocess.run(
            ["sh", "-c", "top -l 1 | grep 'CPU usage' | awk '{print $3}'"],
            capture_output=True, text=True, timeout=5
        )
        
        # 内存
        mem = subprocess.run(
            ["sysctl", "hw.memsize"],
            capture_output=True, text=True, timeout=5
        )
        
        # 磁盘
        disk = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True, text=True, timeout=5
        )
        
        return {
            "CPU": cpu.stdout.strip() or "正常",
            "Memory": f"{int(mem.stdout.strip().split(':')[1]) / 1024 / 1024 / 1024:.1f} GB",
            "Disk": disk.stdout.strip().split('\n')[1] if disk.stdout else "正常"
        }
    except Exception as e:
        return {"error": str(e)}

def check_telegram():
    """检查Telegram Bot"""
    try:
        import requests
        token = "8579932371:AAHBejw0ETAC0MiwTmyD6xzp3I2eo1A4oso"
        resp = requests.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=10
        )
        if resp.status_code == 200:
            return f"✅ Bot正常: @{resp.json()['result']['username']}"
        else:
            return f"❌ Bot异常: {resp.status_code}"
    except Exception as e:
        return f"❌ 连接失败: {str(e)[:30]}"

def check_processes():
    """检查关键进程"""
    processes = [
        "Night_Watcher",
        "opencode",
        "python3.*app.py",
        "clash"
    ]
    
    result = {}
    for proc in processes:
        output = subprocess.run(
            ["pgrep", "-fl", proc],
            capture_output=True, text=True, timeout=5
        )
        result[proc] = "✅ 运行中" if output.returncode == 0 else "❌ 未运行"
    
    return result

def check_skills():
    """检查 Skills"""
    skills_path = os.path.expanduser("~/.openclaw/workspace/skills")
    skills = []
    
    try:
        for item in os.listdir(skills_path):
            path = os.path.join(skills_path, item)
            if os.path.isdir(path) and item not in ['skills', 'MiniMax-AI']:
                skills.append(item)
    except:
        pass
    
    return {"count": len(skills), "skills": skills[:10]}

def run_healthcheck():
    """执行完整自检"""
    report = f"""
╔══════════════════════════════════════╗
║       SYSTEM HEALTH CHECK          ║
║       系统自检报告                  ║
╚══════════════════════════════════════╝

⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 端口服务状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    ports = check_ports()
    for port, status in ports.items():
        report += f"\n  端口 {port}: {status}"
    
    report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 系统资源
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    resources = check_resources()
    for k, v in resources.items():
        report += f"\n  {k}: {v}"
    
    report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Telegram Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {check_telegram()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 关键进程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    processes = check_processes()
    for proc, status in processes.items():
        report += f"\n  {proc}: {status}"
    
    report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Skills 状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    skills = check_skills()
    report += f"\n  已部署: {skills['count']} 个 Skills"
    report += f"\n  示例: {', '.join(skills['skills'][:5])}..."

    report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 自检完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return report

if __name__ == "__main__":
    print(run_healthcheck())

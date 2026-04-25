#!/usr/bin/env python3
"""
Recon 网络侦察系统
提供端口扫描、服务检测、网络探测等功能
"""

import subprocess
import socket
import time
import json
from datetime import datetime
from pathlib import Path

class Recon:
    """网络侦察系统"""
    
    def __init__(self):
        self.cache_dir = Path.home() / ".openclaw/workspace/cache/recon"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def check_services(self):
        """检测本地服务状态"""
        services = [
            ("3000", "命令控制塔"),
            ("5000", "企业管理看板"),
            ("5001", "情报中心"),
            ("18789", "OpenClaw主界面"),
            ("9996", "火种状态API"),
            ("9997", "自愈核心"),
            ("9998", "大脑心跳"),
        ]
        
        results = []
        for port, name in services:
            status = self.check_port("127.0.0.1", int(port))
            results.append({
                "port": port,
                "name": name,
                "status": "UP" if status else "DOWN"
            })
        
        return results
    
    def check_port(self, host, port, timeout=2):
        """检查端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_ports(self, ip, start_port=1, end_port=1024):
        """扫描端口"""
        open_ports = []
        print(f"扫描 {ip} 端口范围 {start_port}-{end_port}...")
        
        for port in range(start_port, end_port + 1):
            if self.check_port(ip, port, timeout=0.5):
                open_ports.append(port)
                print(f"  发现开放端口: {port}")
        
        return open_ports
    
    def ping(self, target):
        """检测网络连通性"""
        try:
            result = subprocess.run(
                ['ping', '-c', '3', '-W', '2', target],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                # 提取延迟
                for line in result.stdout.split('\n'):
                    if 'time=' in line:
                        return True, line.strip()
                return True, "连通"
            return False, "无法到达"
        except Exception as e:
            return False, str(e)
    
    def scan_network(self, subnet="192.168.1"):
        """扫描局域网设备"""
        devices = []
        print(f"扫描局域网 {subnet}.1-254...")
        
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            if self.check_port(ip, 80, timeout=0.3) or self.check_port(ip, 22, timeout=0.3):
                devices.append(ip)
                print(f"  发现设备: {ip}")
        
        return devices
    
    def health_check(self):
        """批量健康检查"""
        print("=" * 50)
        print("🔍 服务健康检查")
        print("=" * 50)
        
        results = self.check_services()
        
        print(f"\n{'端口':<8} {'服务名':<20} {'状态':<10}")
        print("-" * 50)
        for r in results:
            status_icon = "✅" if r['status'] == "UP" else "❌"
            print(f"{r['port']:<8} {r['name']:<20} {status_icon} {r['status']}")
        
        up_count = sum(1 for r in results if r['status'] == "UP")
        print(f"\n总计: {up_count}/{len(results)} 服务在线")
        
        return results

if __name__ == "__main__":
    import sys
    
    recon = Recon()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "health_check":
            recon.health_check()
        elif cmd == "check_services":
            results = recon.check_services()
            print(json.dumps(results, indent=2))
        elif cmd == "ping" and len(sys.argv) > 2:
            ok, msg = recon.ping(sys.argv[2])
            print(f"{'✅' if ok else '❌'} {sys.argv[2]}: {msg}")
        elif cmd == "scan_network" and len(sys.argv) > 2:
            devices = recon.scan_network(sys.argv[2])
            print(f"发现 {len(devices)} 台设备: {devices}")
        else:
            print("可用命令: health_check, check_services, ping <target>, scan_network <subnet>")
    else:
        recon.health_check()

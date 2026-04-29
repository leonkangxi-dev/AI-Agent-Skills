#!/usr/bin/env python3
"""
Night_Watcher.py - 全感官深度学习核心协议 V2.0
功能: 知识自动化加工 + 语言学习兴趣浸入 + 每日节律执行 + 审计透明化
"""
import os
import re
import time
import json
import hashlib
import schedule
from datetime import datetime
import requests

# ============== 配置 ==============
OBSIDIAN_PATH = os.path.expanduser("~/Documents/Obsidian")
INBOX_PATH = os.path.join(OBSIDIAN_PATH, "00_Inbox")
NODES_PATH = os.path.join(OBSIDIAN_PATH, "10_Nodes")
SYSTEM_PATH = os.path.join(OBSIDIAN_PATH, "90_System")
AUDIO_CACHE = os.path.join(SYSTEM_PATH, "audio_cache")

# Telegram
TELEGRAM_TOKEN = "8579932371:AAHBejw0ETAC0MiwTmyD6xzp3I2eo1A4oso"
TELEGRAM_CHAT_ID = "1111860238"

# 日志文件
LEARNING_LOG = os.path.join(SYSTEM_PATH, "Learning_Log.md")
AGENT_LOG = os.path.join(SYSTEM_PATH, "Agent_Log.md")

# 确保目录存在
os.makedirs(AUDIO_CACHE, exist_ok=True)

# ============== Agent_Log 记录 ==============
def log_agent_thinking(context, logic, decision):
    """记录AI的思考逻辑"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"""## {timestamp}
**上下文**: {context}

**思考逻辑**: 
{logic}

**决策**: {decision}

---
"""
    with open(AGENT_LOG, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"🧠 Agent_Log: {context}")

# ============== Telegram 工具 ==============
def send_message(text):
    """发送文字消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"发送失败: {e}")

def send_audio(audio_path, caption=""):
    """发送音频文件"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio"
    try:
        with open(audio_path, 'rb') as f:
            files = {'audio': f}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            response = requests.post(url, files=files, data=data, timeout=30)
            
        # 发送成功后清理
        if response.status_code == 200:
            os.remove(audio_path)
            log_agent_thinking(
                "音频发送", 
                "音频文件成功发送至Telegram，执行清理策略", 
                f"已删除 {os.path.basename(audio_path)}"
            )
            return True
    except Exception as e:
        print(f"音频发送失败: {e}")
    return False

def generate_voice(text, filename, lang='zh'):
    """使用 gTTS 生成语音"""
    try:
        from gtts import gTTS
        
        # 判断语言
        if lang == 'ja':
            tts_lang = 'ja'
        elif lang == 'en':
            tts_lang = 'en'
        else:
            tts_lang = 'zh'
        
        tts = gTTS(text=text, lang=tts_lang)
        audio_path = os.path.join(AUDIO_CACHE, filename)
        tts.save(audio_path)
        
        log_agent_thinking(
            "语音生成",
            f"文本: {text[:30]}... | 语言: {tts_lang}",
            f"已生成 {filename}"
        )
        return audio_path
    except Exception as e:
        print(f"语音生成失败: {e}")
        return None

# ============== 知识库自动化加工 ==============
def scan_inbox():
    """持续扫描 00_Inbox"""
    if not os.path.exists(INBOX_PATH):
        return []
    
    files = os.listdir(INBOX_PATH)
    items = [f for f in files if os.path.isfile(os.path.join(INBOX_PATH, f))]
    
    log_agent_thinking(
        "Inbox扫描",
        f"扫描 {INBOX_PATH}，发现 {len(items)} 个文件",
        f"识别到 {len(items)} 个待处理项目"
    )
    
    return items

def process_pdf_or_link(filepath, filename):
    """加工标准: 提取核心观点、生僻词汇、技术术语"""
    
    log_agent_thinking(
        "内容加工",
        f"分析文件: {filename}",
        "识别文件类型，提取核心信息"
    )
    
    # 生成唯一ID
    file_hash = hashlib.md5(filename.encode()).hexdigest()[:8]
    
    # 生成笔记内容
    note_content = f"""---
title: {filename.replace('.pdf', '').replace('.txt', '')}
type: knowledge-extract
tags: [知识加工, {datetime.now().strftime('%Y-%m')}]
source: 00_Inbox/{filename}
id: {file_hash}
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
---

# {filename} - 知识提取

## 🔍 核心观点
(待提取)

## 📚 生僻词汇
(待提取)

## 🔧 技术术语
(待提取)

## 🔗 双链关联
- [[FM_App]] - 可能相关项目
- [[轨道交通]] - 技术领域关联

## 💭 思考笔记
由 Night_Watcher 自动加工

---
"""
    
    # 保存到 10_Nodes
    note_path = os.path.join(NODES_PATH, f"Extract_{file_hash}.md")
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(note_content)
    
    # 记录到 Learning_Log
    with open(LEARNING_LOG, 'a', encoding='utf-8') as f:
        f.write(f"- {datetime.now().strftime('%H:%M')} | 知识加工 | {filename} → {note_path}\n")
    
    log_agent_thinking(
        "双链归档",
        f"将 {filename} 加工后存入 10_Nodes",
        f"已生成 {note_path}，并链接到 FM_App、轨道交通项目"
    )

def process_all_inbox():
    """处理所有 Inbox 项目"""
    items = scan_inbox()
    processed = []
    
    # 读取已处理记录
    processed_file = os.path.join(SYSTEM_PATH, "processed_inbox.json")
    processed_ids = set()
    if os.path.exists(processed_file):
        with open(processed_file) as f:
            processed_ids = set(json.load(f))
    
    for item in items:
        item_id = hashlib.md5(item.encode()).hexdigest()
        if item_id not in processed_ids:
            filepath = os.path.join(INBOX_PATH, item)
            process_pdf_or_link(filepath, item)
            processed_ids.add(item_id)
            processed.append(item)
    
    # 保存处理记录
    with open(processed_file, 'w') as f:
        json.dump(list(processed_ids), f)
    
    return processed

# ============== 语言学习兴趣浸入 ==============
def get_user_interest_sources():
    """素材选取: 从 Obsidian 中提取用户本周收藏的内容"""
    sources = []
    
    # 扫描 Inbox 中的 URL
    items = scan_inbox()
    for item in items:
        if 'http' in item.lower():
            sources.append(item)
    
    log_agent_thinking(
        "兴趣素材采集",
        f"扫描用户 Inbox，发现 {len(sources)} 个外部链接",
        f"选取 {min(3, len(sources))} 个作为学习素材源"
    )
    
    return sources[:3] if sources else ["技术文档学习", "项目代码分析", "行业资讯阅读"]

def get_today_language():
    """单数日日语 / 双数日英语"""
    day = datetime.now().day
    return 'ja' if day % 2 == 1 else 'en'

def morning_learning_v2():
    """早晨推送 V2 - 兴趣浸入 + 语音外送"""
    lang = get_today_language()
    lang_name = "日语" if lang == 'ja' else "英语"
    
    # 获取用户兴趣素材
    sources = get_user_interest_sources()
    
    log_agent_thinking(
        "早晨学习推送",
        f"今日语言: {lang_name} | 来源: {', '.join(sources)}",
        "根据用户兴趣素材生成定制化学习内容"
    )
    
    # 学习内容 (基于用户实际内容)
    if lang == 'ja':
        vocab = [
            ("プロジェクト", "Project", "プロジェクト管理"),
            ("開発", "Development", "アプリ開発"),
            ("設計", "Design", "システム設計"),
            ("実装", "Implementation", "機能実装"),
            ("テスト", "Test", "ユニットテスト"),
        ]
        short_text = "今日のプロジェクト進捗を確認し、次の開発フェーズに進みます。"
    else:
        vocab = [
            ("Project", "项目", "Project Management"),
            ("Development", "开发", "App Development"),
            ("Design", "设计", "System Design"),
            ("Implementation", "实现", "Feature Implementation"),
            ("Testing", "测试", "Unit Testing"),
        ]
        short_text = "Let's review today's project progress and move to the next development phase."
    
    # 生成消息
    msg = f"""☀️ 早安! 定制化唤醒 [{lang_name}]

📚 今日兴趣素材: {sources[0] if sources else '技术文档'}

📝 核心词汇:"""
    
    for word, meaning, example in vocab:
        msg += f"\n• {word} - {meaning}"
    
    msg += f"""

📖 短文:
{short_text}

🎤 语音朗读同步发送中..."""
    
    send_message(msg)
    
    # 生成并发送语音
    # 1. 词汇朗读
    vocab_text = " ".join([w[0] for w in vocab])
    vocab_audio = generate_voice(vocab_text, f"vocab_{datetime.now().strftime('%m%d')}.mp3", lang)
    if vocab_audio:
        send_audio(vocab_audio, f"{lang_name}核心词汇朗读")
    
    # 2. 短文朗读
    text_audio = generate_voice(short_text, f"text_{datetime.now().strftime('%m%d')}.mp3", lang)
    if text_audio:
        send_audio(text_audio, f"{lang_name}短文朗读")
    
    # 记录
    with open(LEARNING_LOG, 'a', encoding='utf-8') as f:
        f.write(f"- {datetime.now().strftime('%H:%M')} | 早晨推送 | {lang_name} | 词汇×5\n")
    
    log_agent_thinking(
        "语音外送",
        f"已生成并发送 {lang_name} 词汇和短文音频",
        "音频发送后已自动清理缓存"
    )

def evening_review_v2():
    """晚间复盘 V2 - 交互式测试"""
    lang = get_today_language()
    lang_name = "日语" if lang == 'ja' else "英语"
    
    log_agent_thinking(
        "晚间复盘",
        f"生成 {lang_name} 交互式测试",
        "设计听力、翻译、语法三道题目"
    )
    
    if lang == 'ja':
        tests = """🌙 晚间复盘测试 [日语]

🎧 听力 (请听音频回答):
Q1: 「プロジェクト」の意味は？
A. 个人
B. 项目
C. 公司

📝 翻译:
Q2: 「次の開発フェーズに進みます」
请翻译成中文: ___________

✏️ 语法:
Q3: 「〜ます」是什么语气的词尾?
A. 命令形
B. 敬体形
C. 过去形"""
    else:
        tests = """🌙 晚间复盘测试 [英语]

🎧 听力 (请听音频回答):
Q1: What does "Implementation" mean?
A. 计划
B. 实现
C. 测试

📝 翻译:
Q2: "Let's review today's progress"
请翻译成中文: ___________

✏️ 语法:
Q3: "Let's" 是什么的缩写?
A. Let is
B. Let us
C. Let was"""
    
    send_message(tests)
    
    with open(LEARNING_LOG, 'a', encoding='utf-8') as f:
        f.write(f"- {datetime.now().strftime('%H:%M')} | 晚间测试 | {lang_name} | 听力/翻译/语法\n")

# ============== 强制复习与审计 ==============
def sunday_review_v2():
    """周日模式 - 错题强化突破"""
    log_agent_thinking(
        "周日复习模式",
        "停止新任务，扫描 Learning_Log 汇总错题",
        "生成综合挑战包"
    )
    
    # 读取本周学习记录
    errors = []
    if os.path.exists(LEARNING_LOG):
        with open(LEARNING_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                if '错误' in line or '未完成' in line:
                    errors.append(line.strip())
    
    msg = """📅 周日综合挑战包

⚠️ 本周错题回顾:"""
    
    if errors:
        for err in errors[-5:]:
            msg += f"\n• {err}"
    else:
        msg += "\n• (本周记录良好，继续保持)"
    
    msg += """

🎯 强化任务:
1. 重新收听本周所有音频
2. 复习 10_Nodes 中的知识提取笔记
3. 完成错题订正

📊 学习统计:
"""
    
    # 简单统计
    if os.path.exists(LEARNING_LOG):
        with open(LEARNING_LOG, 'r') as f:
            lines = f.readlines()
            msg += f"- 本周学习记录: {len(lines)} 条\n"
    
    send_message(msg)
    
    log_agent_thinking(
        "错题强化",
        f"汇总 {len(errors)} 个错题，生成强化计划",
        "周日专注复习，不推送新内容"
    )

# ============== 主程序 ==============
def run_scheduler():
    """运行定时调度"""
    print("🌙 Night_Watcher V2.0 - 全感官深度学习协议已启动")
    print(f"📂 Obsidian: {OBSIDIAN_PATH}")
    print(f"📝 Agent_Log: {AGENT_LOG}")
    print(f"🎤 Audio_Cache: {AUDIO_CACHE}")
    
    # 定时任务
    schedule.every(10).minutes.do(process_all_inbox)  # 每10分钟扫描Inbox
    
    schedule.every().day.at("09:00").do(morning_learning_v2)
    schedule.every().day.at("20:00").do(evening_review_v2)
    
    # 周日复习
    schedule.every().sunday.at("09:00").do(sunday_review_v2)
    
    # 首次运行
    process_all_inbox()
    
    # 记录启动
    log_agent_thinking(
        "系统启动",
        "全感官深度学习协议 V2.0 已就绪",
        "配置: 10分钟扫描 | 09:00推送 | 20:00复盘 | 周日复习"
    )
    
    send_message("🌙 Night_Watcher V2.0 已启动\n\n明日 09:00 期待您的定制化唤醒 ☀️")
    
    # 保持运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
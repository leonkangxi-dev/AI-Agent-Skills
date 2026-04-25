# Video Highlights Skill

自动扫描视频文件夹，识别音量大于-20dB的高能片段，提取并合成集锦。

## 功能

- 扫描指定文件夹下的所有视频文件（MP4、AVI、MOV、MKV等）
- 使用FFmpeg分析音频音量，识别音量 > -20dB 的片段
- 自动提取高能片段
- 合成最终集锦视频

## 依赖

- FFmpeg（必需）
- Python 3（用于解析片段）
- bc（用于计算）

## 使用方法

```bash
# 基本用法
~/.openclaw/workspace/skills/video-highlights/run.sh -f /path/to/videos

# 指定输出文件
~/.openclaw/workspace/skills/video-highlights/run.sh -f /path/to/videos -o my_highlights.mp4

# 自定义参数
~/.openclaw/workspace/skills/video-highlights/run.sh \
    -f /path/to/videos \
    -o output.mp4 \
    -t -25 \
    -d 2.0 \
    -p 1.0
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-f, --folder` | 视频文件夹路径 | 必需 |
| `-o, --output` | 输出文件名 | highlights.mp4 |
| `-t, --threshold` | 音量阈值dB | -20 |
| `-d, --min-duration` | 最小片段时长秒 | 1.0 |
| `-p, --padding` | 片段前后预留秒数 | 0.5 |

## 示例

```bash
# 处理桌面视频文件夹
~/.openclaw/workspace/skills/video-highlights/run.sh -f ~/Desktop/我的视频

# 使用-25dB阈值，提取更安静但有声音的片段
~/.openclaw/workspace/skills/video-highlights/run.sh -f ~/Videos -t -25

# 生成更长的片段（最少3秒）
~/.openclaw/workspace/skills/video-highlights/run.sh -f ~/Videos -d 3.0
```

## 输出

生成的集锦视频将保存在指定位置，包含所有识别出的高能片段。

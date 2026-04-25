# Video Editor Skill

按文件名顺序合并视频，统一调整为16:9比例，输出到桌面。

## 功能

- 扫描文件夹中的所有视频文件
- 按文件名排序
- 统一调整为1920x1080 (16:9) 比例
- 合并输出到桌面

## 使用方法

```bash
# 基本用法
python3 video_editor.py /path/to/videos

# 指定输出文件名
python3 video_editor.py /path/to/videos -o my_video.mp4
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `folder` | 视频文件夹路径 | 必需 |
| `-o, --output` | 输出文件名 | merged_video.mp4 |

## 输出

视频将保存到桌面：~/Desktop/merged_video.mp4

## 支持的格式

- MP4
- MOV
- AVI
- MKV
- FLV
- WMV
- M4V

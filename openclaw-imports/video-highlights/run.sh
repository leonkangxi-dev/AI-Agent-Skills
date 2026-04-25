#!/bin/bash
# Video Highlights Skill - 使用FFmpeg实现
# 自动识别视频中音量大于-20dB的片段并合成集锦

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认参数
THRESHOLD_DB=-20
MIN_DURATION=1.0
PADDING=0.5
OUTPUT_FILE="highlights.mp4"

# 显示帮助
show_help() {
    echo "视频高能片段提取器"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -f, --folder PATH       视频文件夹路径 (必需)"
    echo "  -o, --output FILE       输出文件名 (默认: highlights.mp4)"
    echo "  -t, --threshold DB      音量阈值dB (默认: -20)"
    echo "  -d, --min-duration SEC  最小片段时长秒 (默认: 1.0)"
    echo "  -p, --padding SEC       片段前后预留秒数 (默认: 0.5)"
    echo "  -h, --help              显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 -f ~/Videos -o my_highlights.mp4"
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--folder)
            FOLDER="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -t|--threshold)
            THRESHOLD_DB="$2"
            shift 2
            ;;
        -d|--min-duration)
            MIN_DURATION="$2"
            shift 2
            ;;
        -p|--padding)
            PADDING="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$FOLDER" ]; then
    echo -e "${RED}错误: 请指定视频文件夹路径 (-f)${NC}"
    show_help
    exit 1
fi

if [ ! -d "$FOLDER" ]; then
    echo -e "${RED}错误: 文件夹不存在: $FOLDER${NC}"
    exit 1
fi

# 检查FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}错误: FFmpeg未安装${NC}"
    exit 1
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo -e "${GREEN}视频高能片段提取器${NC}"
echo "===================="
echo "文件夹: $FOLDER"
echo "输出: $OUTPUT_FILE"
echo "音量阈值: ${THRESHOLD_DB}dB"
echo ""

# 查找所有视频文件
VIDEO_FILES=()
while IFS= read -r -d '' file; do
    VIDEO_FILES+=("$file")
done < <(find "$FOLDER" -type f \( -name "*.mp4" -o -name "*.avi" -o -name "*.mov" -o -name "*.mkv" -o -name "*.flv" -o -name "*.wmv" -o -name "*.m4v" \) -print0 2>/dev/null)

if [ ${#VIDEO_FILES[@]} -eq 0 ]; then
    echo -e "${RED}错误: 文件夹中没有视频文件${NC}"
    exit 1
fi

echo "找到 ${#VIDEO_FILES[@]} 个视频文件"
echo ""

# 处理每个视频
SEGMENT_LIST="$TEMP_DIR/segments.txt"
touch "$SEGMENT_LIST"

for video in "${VIDEO_FILES[@]}"; do
    echo "分析: $(basename "$video")"
    
    # 获取视频时长
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video" 2>/dev/null || echo "0")
    duration=${duration%.*}
    
    if [ "$duration" -eq 0 ]; then
        echo "  跳过: 无法读取时长"
        continue
    fi
    
    echo "  时长: ${duration}s"
    
    # 使用FFmpeg的silencedetect滤镜检测非静音片段
    # 反转逻辑: 检测音量大于阈值的片段
    ffmpeg -i "$video" -af "silencedetect=noise=${THRESHOLD_DB}dB:d=0.5" -f null - 2>"$TEMP_DIR/silence.log" || true
    
    # 解析silencedetect输出，找出高音量片段
    # silence_start和silence_end之间的片段就是高音量片段
    python3 <> "$TEMP_DIR/extract.py" << 'EOF'
import re
import sys

silence_file = sys.argv[1]
video_file = sys.argv[2]
output_list = sys.argv[3]
video_duration = float(sys.argv[4])
padding = float(sys.argv[5])
min_duration = float(sys.argv[6])

# 读取silencedetect输出
with open(silence_file, 'r') as f:
    content = f.read()

# 提取silence_start和silence_end
starts = re.findall(r'silence_start: ([\d.]+)', content)
ends = re.findall(r'silence_end: ([\d.]+)', content)

# 计算高音量片段（silence之间的片段）
highlights = []
last_end = 0.0

for i, start in enumerate(starts):
    start = float(start)
    # 从上一个静音结束到当前静音开始，就是高音量片段
    if start > last_end:
        segment_start = max(0, last_end - padding)
        segment_end = min(video_duration, start + padding)
        
        # 确保最小时长
        if segment_end - segment_start < min_duration:
            segment_end = min(video_duration, segment_start + min_duration)
        
        if segment_end - segment_start >= min_duration:
            highlights.append((segment_start, segment_end))
    
    # 更新last_end
    if i < len(ends):
        last_end = float(ends[i])

# 处理最后一个片段（从最后一个静音结束到视频结束）
if last_end < video_duration:
    segment_start = max(0, last_end - padding)
    segment_end = video_duration
    
    if segment_end - segment_start >= min_duration:
        highlights.append((segment_start, segment_end))

# 如果没有检测到静音，说明整个视频都是高音量
if not starts:
    highlights.append((0, video_duration))

# 输出片段信息
for i, (start, end) in enumerate(highlights):
    print(f"  片段 {i+1}: {start:.2f}s - {end:.2f}s (时长: {end-start:.2f}s)")
    # 写入片段列表
    with open(output_list, 'a') as f:
        f.write(f"{video_file}|{start}|{end}\n")

print(f"  提取 {len(highlights)} 个片段")
EOF
    
    python3 "$TEMP_DIR/extract.py" "$TEMP_DIR/silence.log" "$video" "$SEGMENT_LIST" "$duration" "$PADDING" "$MIN_DURATION" || true
    echo ""
done

# 检查是否有片段
if [ ! -s "$SEGMENT_LIST" ]; then
    echo -e "${RED}错误: 没有找到高能片段${NC}"
    exit 1
fi

# 提取所有片段
echo "提取片段..."
CLIP_COUNT=0
while IFS='|' read -r video start end; do
    CLIP_COUNT=$((CLIP_COUNT + 1))
    output_clip="$TEMP_DIR/clip_$(printf "%04d" $CLIP_COUNT).mp4"
    
    ffmpeg -y -i "$video" -ss "$start" -t "$(echo "$end - $start" | bc)" \
        -c:v libx264 -preset fast -crf 23 \
        -c:a aac -b:a 128k \
        -pix_fmt yuv420p \
        "$output_clip" 2>/dev/null || true
done < "$SEGMENT_LIST"

# 检查提取的片段
CLIP_FILES=("$TEMP_DIR"/clip_*.mp4)
if [ ! -f "${CLIP_FILES[0]}" ]; then
    echo -e "${RED}错误: 片段提取失败${NC}"
    exit 1
fi

# 创建concat列表
echo "合成集锦视频..."
CONCAT_LIST="$TEMP_DIR/concat.txt"
for clip in "$TEMP_DIR"/clip_*.mp4; do
    if [ -f "$clip" ]; then
        echo "file '$(echo "$clip" | sed "s/'/'\\\\''/g")'" >> "$CONCAT_LIST"
    fi
done

# 合成最终视频
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" \
    -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 192k \
    -pix_fmt yuv420p \
    -movflags +faststart \
    "$OUTPUT_FILE" 2>/dev/null

# 检查输出
if [ -f "$OUTPUT_FILE" ]; then
    FILESIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo -e "${GREEN}✅ 集锦视频已生成: $OUTPUT_FILE (${FILESIZE})${NC}"
else
    echo -e "${RED}❌ 生成失败${NC}"
    exit 1
fi

echo ""
echo "完成！"

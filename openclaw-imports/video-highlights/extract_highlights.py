#!/usr/bin/env python3
"""
Video Highlights Extractor
自动识别视频中的高能片段（音量>-20dB）并合成集锦
"""

import os
import sys
import argparse
from pathlib import Path
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip


def get_video_files(folder):
    """获取文件夹下所有视频文件"""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v'}
    folder = Path(folder)
    videos = []
    for ext in video_extensions:
        videos.extend(folder.glob(f'*{ext}'))
        videos.extend(folder.glob(f'*{ext.upper()}'))
    return sorted(videos)


def analyze_audio_volume(video_path, threshold_db=-20, sample_rate=10):
    """
    分析视频音频音量，返回音量大于阈值的片段
    
    Args:
        video_path: 视频文件路径
        threshold_db: 音量阈值（dB），默认-20
        sample_rate: 每秒采样次数
    
    Returns:
        list: [(start_time, end_time), ...] 高能片段列表
    """
    print(f"分析视频: {video_path.name}")
    
    try:
        clip = VideoFileClip(str(video_path))
        audio = clip.audio
        
        if audio is None:
            print(f"  ⚠️ 视频没有音频轨道")
            return []
        
        # 获取音频数据
        duration = clip.duration
        samples = int(duration * sample_rate)
        
        # 分段分析音量
        high_volume_segments = []
        segment_duration = 1.0 / sample_rate
        
        for i in range(samples):
            start = i * segment_duration
            end = min((i + 1) * segment_duration, duration)
            
            # 提取该时间段的音频样本
            try:
                audio_chunk = audio.subclip(start, end)
                # 获取音频数组
                audio_array = audio_chunk.to_soundarray(fps=22000)
                
                # 计算音量（RMS）
                if len(audio_array) > 0:
                    # 转换为单声道
                    if len(audio_array.shape) > 1:
                        audio_array = audio_array.mean(axis=1)
                    
                    # 计算RMS音量
                    rms = np.sqrt(np.mean(audio_array ** 2))
                    
                    # 转换为dB
                    if rms > 0:
                        volume_db = 20 * np.log10(rms)
                    else:
                        volume_db = -100
                    
                    # 检查是否超过阈值
                    if volume_db > threshold_db:
                        high_volume_segments.append((start, end, volume_db))
                        
            except Exception as e:
                continue
        
        clip.close()
        
        # 合并相邻的片段
        return merge_segments(high_volume_segments, min_gap=0.5)
        
    except Exception as e:
        print(f"  ❌ 分析失败: {e}")
        return []


def merge_segments(segments, min_gap=0.5):
    """合并相邻的高音量片段"""
    if not segments:
        return []
    
    # 按时间排序
    segments = sorted(segments, key=lambda x: x[0])
    
    merged = []
    current_start = segments[0][0]
    current_end = segments[0][1]
    max_volume = segments[0][2]
    
    for start, end, volume in segments[1:]:
        if start - current_end <= min_gap:
            # 合并
            current_end = end
            max_volume = max(max_volume, volume)
        else:
            # 保存当前片段
            merged.append((current_start, current_end, max_volume))
            current_start = start
            current_end = end
            max_volume = volume
    
    # 保存最后一个片段
    merged.append((current_start, current_end, max_volume))
    
    return merged


def extract_highlights(video_path, segments, padding=0.5, min_duration=1.0):
    """
    从视频中提取高能片段
    
    Args:
        video_path: 视频文件路径
        segments: 高能片段列表 [(start, end, volume), ...]
        padding: 前后预留时间（秒）
        min_duration: 最小片段时长（秒）
    
    Returns:
        list: 视频片段列表
    """
    if not segments:
        return []
    
    print(f"  提取 {len(segments)} 个高能片段...")
    
    try:
        clip = VideoFileClip(str(video_path))
        clips = []
        
        for i, (start, end, volume) in enumerate(segments):
            # 添加padding
            clip_start = max(0, start - padding)
            clip_end = min(clip.duration, end + padding)
            
            # 确保最小时长
            if clip_end - clip_start < min_duration:
                clip_end = min(clip.duration, clip_start + min_duration)
            
            try:
                subclip = clip.subclip(clip_start, clip_end)
                clips.append(subclip)
                print(f"    片段 {i+1}: {clip_start:.2f}s - {clip_end:.2f}s (音量: {volume:.1f}dB)")
            except Exception as e:
                print(f"    ⚠️ 提取片段 {i+1} 失败: {e}")
                continue
        
        clip.close()
        return clips
        
    except Exception as e:
        print(f"  ❌ 提取失败: {e}")
        return []


def create_highlights_video(clips, output_path, transition_duration=0.3):
    """
    合成集锦视频
    
    Args:
        clips: 视频片段列表
        output_path: 输出路径
        transition_duration: 转场时长（秒）
    """
    if not clips:
        print("❌ 没有可合成的片段")
        return False
    
    print(f"\n合成集锦视频: {len(clips)} 个片段")
    
    try:
        # 统一分辨率（使用第一个片段的分辨率）
        target_size = clips[0].size
        
        processed_clips = []
        for i, clip in enumerate(clips):
            # 调整分辨率
            if clip.size != target_size:
                clip = clip.resize(newsize=target_size)
            
            # 添加转场效果（淡入淡出）
            if i > 0:
                clip = clip.fadein(transition_duration)
            if i < len(clips) - 1:
                clip = clip.fadeout(transition_duration)
            
            processed_clips.append(clip)
        
        # 合成最终视频
        final_video = concatenate_videoclips(processed_clips, method="compose")
        
        # 写入文件
        print(f"  正在渲染...")
        final_video.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            fps=30,
            threads=4,
            logger=None  # 减少输出信息
        )
        
        # 清理
        final_video.close()
        for clip in processed_clips:
            clip.close()
        
        print(f"✅ 集锦视频已保存: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 合成失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='视频高能片段提取器')
    parser.add_argument('--folder', '-f', required=True, help='视频文件夹路径')
    parser.add_argument('--output', '-o', default='highlights.mp4', help='输出视频路径')
    parser.add_argument('--threshold', '-t', type=float, default=-20, help='音量阈值dB（默认-20）')
    parser.add_argument('--min-duration', '-d', type=float, default=1.0, help='最小片段时长秒（默认1.0）')
    parser.add_argument('--padding', '-p', type=float, default=0.5, help='片段前后预留秒数（默认0.5）')
    
    args = parser.parse_args()
    
    # 检查文件夹
    folder = Path(args.folder)
    if not folder.exists():
        print(f"❌ 文件夹不存在: {folder}")
        return 1
    
    # 获取视频文件
    videos = get_video_files(folder)
    if not videos:
        print(f"❌ 文件夹中没有视频文件: {folder}")
        return 1
    
    print(f"找到 {len(videos)} 个视频文件\n")
    
    # 处理每个视频
    all_clips = []
    for video_path in videos:
        # 分析音量
        segments = analyze_audio_volume(video_path, threshold_db=args.threshold)
        
        if segments:
            # 提取片段
            clips = extract_highlights(
                video_path, 
                segments, 
                padding=args.padding,
                min_duration=args.min_duration
            )
            all_clips.extend(clips)
        else:
            print(f"  没有找到高能片段\n")
    
    # 合成集锦
    if all_clips:
        output_path = Path(args.output)
        success = create_highlights_video(all_clips, output_path)
        
        # 清理
        for clip in all_clips:
            try:
                clip.close()
            except:
                pass
        
        return 0 if success else 1
    else:
        print("❌ 没有提取到任何高能片段")
        return 1


if __name__ == '__main__':
    sys.exit(main())

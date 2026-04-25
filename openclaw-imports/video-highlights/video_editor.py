#!/usr/bin/env python3
"""
Video Editor Skill
批量筛选、缩放并合并视频
"""

import os
import sys
import argparse

# 检查并安装moviepy
try:
    from moviepy import VideoFileClip, concatenate_videoclips, vfx
except ImportError:
    print("正在安装moviepy...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "--break-system-packages", "-q"])
    from moviepy import VideoFileClip, concatenate_videoclips, vfx

# 配置ImageMagick路径（macOS常见路径）
os.environ['IMAGEMAGICK_BINARY'] = '/usr/local/bin/convert'


class VideoEditorSkill:
    def __init__(self, output_dir="~/Desktop/OpenClaw_Output"):
        self.output_dir = os.path.expanduser(output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"创建输出目录: {self.output_dir}")

    def process_videos(self, input_folder, target_resolution=(1920, 1080), output_name="final_video.mp4"):
        """
        批量筛选、缩放并合并视频
        """
        video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v')
        clips = []
        
        # 1. 获取并排序素材
        files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(video_extensions)])
        
        if not files:
            return "文件夹内没有找到有效的视频素材。"

        print(f"正在处理 {len(files)} 个素材...")

        try:
            for file in files:
                file_path = os.path.join(input_folder, file)
                print(f"  处理: {file}")
                
                try:
                    clip = VideoFileClip(file_path)
                except Exception as e:
                    print(f"    跳过: 无法读取文件 ({e})")
                    continue
                
                # 2. 筛选逻辑：跳过小于 1 秒的残次品
                if clip.duration < 1.0:
                    print(f"    跳过: 时长太短 ({clip.duration:.2f}s)")
                    clip.close()
                    continue

                # 3. 统一分辨率
                clip_resized = clip.resize(height=target_resolution[1])
                clips.append(clip_resized)
                print(f"    已添加: {clip.duration:.2f}s")

            if not clips:
                return "没有有效的视频片段可以合并。"

            # 4. 合并素材
            print(f"\n合并 {len(clips)} 个片段...")
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # 5. 输出文件
            output_path = os.path.join(self.output_dir, output_name)
            print(f"渲染中... 输出: {output_path}")
            
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac", 
                fps=24, 
                threads=4,
                logger=None  # 减少输出信息
            )
            
            return f"✅ 剪辑完成！文件已保存至: {output_path}"

        except Exception as e:
            return f"❌ 剪辑过程中出错: {str(e)}"
        finally:
            # 释放内存，防止文件占用
            for c in clips:
                try:
                    c.close()
                except:
                    pass


def main():
    parser = argparse.ArgumentParser(description='视频批量剪辑工具')
    parser.add_argument('-f', '--folder', required=True, help='输入视频文件夹路径')
    parser.add_argument('-o', '--output', default='final_video.mp4', help='输出文件名')
    parser.add_argument('-r', '--resolution', default='1920x1080', help='目标分辨率 (默认: 1920x1080)')
    parser.add_argument('-d', '--output-dir', default='~/Desktop/OpenClaw_Output', help='输出目录')
    
    args = parser.parse_args()
    
    # 解析分辨率
    try:
        width, height = map(int, args.resolution.split('x'))
        target_resolution = (width, height)
    except:
        print("分辨率格式错误，使用默认 1920x1080")
        target_resolution = (1920, 1080)
    
    # 检查输入文件夹
    if not os.path.exists(args.folder):
        print(f"❌ 文件夹不存在: {args.folder}")
        return 1
    
    # 执行处理
    editor = VideoEditorSkill(output_dir=args.output_dir)
    result = editor.process_videos(args.folder, target_resolution, args.output)
    print(result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

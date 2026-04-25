#!/usr/bin/env python3
"""
Video Editor Skill - 简化版
按文件名顺序合并视频，统一16:9比例，输出到桌面
"""

import os
import sys
import argparse

# 导入moviepy
try:
    from moviepy import VideoFileClip, concatenate_videoclips
except ImportError:
    print("正在安装moviepy...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "--break-system-packages", "-q"])
    from moviepy import VideoFileClip, concatenate_videoclips


class VideoEditor:
    def __init__(self):
        # 输出到桌面
        self.output_dir = os.path.expanduser("~/Desktop")

    def merge_videos(self, input_folder, output_name="merged_video.mp4"):
        """
        按文件名顺序合并视频，统一16:9比例
        """
        video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v')
        clips = []
        
        # 获取并排序视频文件
        files = sorted([f for f in os.listdir(input_folder) 
                       if f.lower().endswith(video_extensions)])
        
        if not files:
            return "❌ 文件夹内没有找到视频素材"

        print(f"找到 {len(files)} 个视频文件:")
        for f in files:
            print(f"  - {f}")

        try:
            for file in files:
                file_path = os.path.join(input_folder, file)
                print(f"\n处理: {file}")
                
                try:
                    clip = VideoFileClip(file_path)
                except Exception as e:
                    print(f"  跳过: 无法读取 ({e})")
                    continue
                
                # 调整为16:9比例 (1920x1080)
                clip_resized = self.resize_to_16x9(clip, target_height=1080)
                clips.append(clip_resized)
                print(f"  ✅ 已调整至16:9")

            if not clips:
                return "❌ 没有可合并的视频"

            # 合并视频
            print(f"\n合并 {len(clips)} 个视频片段...")
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # 输出到桌面
            output_path = os.path.join(self.output_dir, output_name)
            print(f"渲染中...")
            
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=30,
                threads=4,
                logger=None
            )
            
            return f"✅ 完成！视频已保存至: {output_path}"

        except Exception as e:
            return f"❌ 错误: {str(e)}"
        finally:
            # 清理资源
            for c in clips:
                try:
                    c.close()
                except:
                    pass

    def resize_to_16x9(self, clip, target_height=1080):
        """
        将视频调整为16:9比例
        - 先缩放到目标高度
        - 如果宽度不是1920，进行裁剪或填充
        """
        # 目标尺寸 1920x1080 (16:9)
        target_width = 1920
        target_height = 1080
        
        # 当前尺寸
        current_w, current_h = clip.size
        
        # 计算缩放比例（基于高度）
        scale = target_height / current_h
        new_width = int(current_w * scale)
        
        # 缩放
        if scale != 1.0:
            clip = clip.resize(height=target_height)
        
        # 调整宽度到1920
        if new_width != target_width:
            if new_width > target_width:
                # 太宽了，裁剪两边
                x_center = new_width // 2
                x1 = x_center - target_width // 2
                clip = clip.crop(x1=x1, y1=0, width=target_width, height=target_height)
            else:
                # 太窄了，填充黑边
                from moviepy.video.fx import resize
                clip = clip.fx(resize, width=target_width, height=target_height)
        
        return clip


def main():
    parser = argparse.ArgumentParser(description='视频合并工具 - 16:9输出')
    parser.add_argument('folder', help='视频文件夹路径')
    parser.add_argument('-o', '--output', default='merged_video.mp4', help='输出文件名')
    
    args = parser.parse_args()
    
    # 检查文件夹
    if not os.path.exists(args.folder):
        print(f"❌ 文件夹不存在: {args.folder}")
        return 1
    
    if not os.path.isdir(args.folder):
        print(f"❌ 不是有效的文件夹: {args.folder}")
        return 1
    
    # 执行合并
    editor = VideoEditor()
    result = editor.merge_videos(args.folder, args.output)
    print(f"\n{result}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

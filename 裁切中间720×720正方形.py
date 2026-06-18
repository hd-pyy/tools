#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本2：裁切视频正中间的720×720正方形区域
支持：单个视频文件 或 文件夹（批量处理）
视频原始尺寸: 1280×720 -> 裁切中间的720×720
"""

import cv2
import os
import sys
from pathlib import Path


def extract_center_720_single(video_path, output_dir, interval=1):
    """
    处理单个视频文件，裁切中间的720×720
    """
    print(f"\n🎯 处理视频: {os.path.basename(video_path)}")

    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 打开视频
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"   ❌ 无法打开视频: {video_path}")
        return False

    # 获取视频信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 计算裁切区域（裁切中间的720×720）
    crop_size = 720
    crop_x = (width - crop_size) // 2  # 对于1280×720: (1280-720)/2 = 280
    crop_y = (height - crop_size) // 2  # 对于1280×720: (720-720)/2 = 0

    print(f"   原始: {width}x{height} -> 裁切: {crop_size}x{crop_size}")
    print(f"   裁切位置: x={crop_x}, y={crop_y}")
    print(f"   总帧数: {total_frames}")

    # 开始抽取
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            # 裁切中心正方形
            center_square = frame[crop_y:crop_y + crop_size,
                            crop_x:crop_x + crop_size]

            filename = f"center_{saved_count:06d}.jpg"
            filepath = output_path / filename
            success = cv2.imwrite(str(filepath), center_square, [cv2.IMWRITE_JPEG_QUALITY, 95])

            if success:
                saved_count += 1

        frame_count += 1

        if frame_count % 100 == 0:
            print(f"   进度: {frame_count}/{total_frames} 帧")

    cap.release()
    print(f"   ✅ 完成! 保存 {saved_count} 张 720×720 图片")
    return True


def extract_center_720_batch(input_path, output_base_dir="center_720_output", interval=1):
    """
    批量处理：如果输入是文件夹，处理里面所有视频
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"❌ 错误: 路径不存在: {input_path}")
        return

    # 视频扩展名
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}

    if input_path.is_file():
        # 单个文件
        if input_path.suffix.lower() in video_extensions:
            video_name = input_path.stem
            output_dir = Path(output_base_dir) / video_name
            extract_center_720_single(input_path, output_dir, interval)
        else:
            print(f"❌ 不支持的文件格式: {input_path.suffix}")

    elif input_path.is_dir():
        # 文件夹：处理所有视频
        video_files = [f for f in input_path.iterdir()
                       if f.is_file() and f.suffix.lower() in video_extensions]

        if not video_files:
            print(f"❌ 文件夹中没有找到视频文件: {input_path}")
            return

        print(f"\n📁 找到 {len(video_files)} 个视频文件")
        print("=" * 70)

        success_count = 0
        for video_file in video_files:
            video_name = video_file.stem
            output_dir = Path(output_base_dir) / video_name
            if extract_center_720_single(video_file, output_dir, interval):
                success_count += 1

        print("\n" + "=" * 70)
        print(f"🎉 批量处理完成! 成功处理 {success_count}/{len(video_files)} 个视频")
    else:
        print(f"❌ 无效的路径: {input_path}")


def main():
    # ==========================================
    # 在这里修改参数
    # ==========================================

    # 输入路径：可以是视频文件 或 文件夹
    input_path = r"C:\Users\17651\Desktop\论文图\02-01-03-01-01-01-01.mp4"

    # 输出基础目录
    output_base_dir = r"C:\Users\17651\Desktop\论文图\center_720_output"

    # 抽取间隔（1=每帧都抽）
    interval = 1

    # ==========================================
    # 执行
    # ==========================================

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_base_dir = sys.argv[2]
    if len(sys.argv) > 3:
        interval = int(sys.argv[3])

    extract_center_720_batch(input_path, output_base_dir, interval)


if __name__ == "__main__":
    main()
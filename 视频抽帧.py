import cv2
import os
import numpy as np

video_path = r"C:\Users\17651\Desktop\论文图\02-01-03-01-01-01-01.mp4"
output_dir = r"C:\Users\17651\Desktop\论文图\02-01-03-01-01-01-01-mp4\frames_output"

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 打开视频
cap = cv2.VideoCapture(video_path)
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 使用imencode保存（更可靠）
    filename = os.path.join(output_dir, f"frame_{count:06d}.jpg")
    success, encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])

    if success:
        with open(filename, 'wb') as f:
            f.write(encoded.tobytes())
        count += 1

        if count % 10 == 0:
            print(f"已保存 {count} 帧")
    else:
        print(f"❌ 编码失败: 第{count}帧")

cap.release()
print(f"\n✅ 完成! 共保存 {count} 帧")
print(f"📁 {output_dir}")

# 验证
if count > 0:
    files = os.listdir(output_dir)
    print(f"实际文件数: {len(files)}")
else:
    print("❌ 保存失败，请检查:")
    print("1. 磁盘空间是否充足")
    print("2. 是否有写入权限")
    print("3. 使用管理员权限运行")
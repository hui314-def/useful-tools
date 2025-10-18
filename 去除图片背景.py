import os
from rembg import remove
from PIL import Image

input_dir = 'output_frames'  # 输入图片文件夹
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
        with Image.open(input_path) as img:
            img_no_bg = remove(img)
            img_no_bg.save(output_path, 'PNG')
print("批量去除背景完成，图片已保存为PNG格式。")

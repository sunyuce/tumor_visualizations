import cv2
import os
import matplotlib.pyplot as plt

import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

# 生成热力图
def generate_heatmap(image, min_val, max_val):
    # 归一化处理
    normalized_image = (image - min_val) / (max_val - min_val)  # 归一化到0-1范围
    normalized_image = np.clip(normalized_image, 0, 1)  # 将归一化后的值限制在0到1之间
    # 应用伪彩色映射生成热力图
    heatmap = cv2.applyColorMap((normalized_image * 255).astype(np.uint8), cv2.COLORMAP_RAINBOW)
    heatmap[image == 0] = [0, 0, 0]

    return heatmap



# 生成热力图


def process_folders(src_folder, output_folder):
    for subdir, dirs, files in os.walk(src_folder):

        heat = np.zeros(shape=(256, 256))
        output_paths = []
        heats=[]

        files.sort(key=lambda f: int(f.split('_')[2].split('.')[0]))

        for file_name in files[::-1]:
            if file_name.startswith("image_") and file_name.endswith(".png"):
                num = file_name.split('_')[2].split('.')[0]
                sub_folder = os.path.relpath(subdir, src_folder)
                mask_path = os.path.join(subdir, f"image_mask_{num}.png")
                output_path = os.path.join(output_folder, sub_folder, f"heat_{num}.png")
                if os.path.exists(mask_path):
                    heat += np.array(Image.open(mask_path).convert("L"))
                    heats.append(heat.copy())
                    output_paths.append(output_path)

        if heats:
            # 获取所有像素的最小值和最大值
            min_val = min(np.min(h) for h in heats)
            max_val = max(np.max(h) for h in heats)

            for i, heat in enumerate(heats):
                heat_image = generate_heatmap(heat, min_val, max_val)
                # 保存结果图像
                output_path = output_paths[i]
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                output_path = os.path.splitext(output_path)[0] + ".png"
                heat_image_pil = Image.fromarray(heat_image)
                heat_image_pil.save(output_path)
                print(f"Saved heatmap to {output_path}")
        else:
            print("No valid image and mask pairs found.")
# 定义文件夹路径
# folder1 = "C:\deskTop\Brain_MRI_segmentation"
# folder2 = "C:/deskTop/unet_predict"
# output_folder = "C:/deskTop/heat_image"
src_folder = 'E:\\brain_three\\b_2'
output_folder = "E:\\brain_three\\b_1"
# 处理文件夹中的图像
process_folders(src_folder, output_folder)


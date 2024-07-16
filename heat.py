#生成一张最终热力图,输入文件夹中包含三个解剖平面的子文件夹,start from 0
import os
import numpy as np
from PIL import Image
# 生成热力图
# def generate_heatmap(image, min_val, max_val):
#     normalized_image = (image - min_val) / (max_val - min_val)  # 归一化到0-1范围
#     normalized_image = np.clip(normalized_image, 0, 1)  # 将归一化后的值限制在0到1之间
#     #COLORMAP采用cv2中的库颜色
#     heatmap = cv2.applyColorMap((normalized_image * 255).astype(np.uint8), cv2.COLORMAP_RAINBOW)
#     heatmap[image == 0] = [0, 0, 0]  # 保留背景
#     return heatmap

def create_custom_colormap():
    cdict = {
        'red':   [(0.0, 0.0, 0.0),   # 红色在起始处是0
                  (0.5, 1.0, 1.0),   # 红色在中间变为最大值
                  (1.0, 1.0, 1.0)],  # 红色在末尾仍然是最大值
        'green': [(0.0, 1.0, 1.0),   # 绿色在起始处是最大值
                  (0.5, 1.0, 1.0),   # 绿色在中间仍然是最大值
                  (1.0, 0.0, 0.0)],  # 绿色在末尾变为0
        'blue':  [(0.0, 0.0, 0.0),   # 蓝色在起始处是0
                  (1.0, 0.0, 0.0)]   # 蓝色在整个范围内都是0
    }
    return cdict

def apply_custom_colormap(image):
    colormap = create_custom_colormap()
    custom_cmap = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            value = image[i, j] / 255.0  # 归一化像素值
            custom_cmap[i, j, 0] = int(np.interp(value, [0, 0.5, 1], [0, 255, 255]))  # 红色通道
            custom_cmap[i, j, 1] = int(np.interp(value, [0, 0.5, 1], [255, 255, 0]))  # 绿色通道
            custom_cmap[i, j, 2] = int(np.interp(value, [0, 1], [0, 0]))  # 蓝色通道（始终为0）
    return custom_cmap

def generate_heatmap(image, min_val, max_val):
    normalized_image = (image - min_val) / (max_val - min_val)  # 归一化到0-1范围
    normalized_image = np.clip(normalized_image, 0, 1)  # 将归一化后的值限制在0到1之间
    # 将归一化后的图像扩展到0-255范围并转换为uint8类型
    normalized_image_uint8 = (normalized_image * 255).astype(np.uint8)
    # 应用自定义颜色映射
    heatmap = apply_custom_colormap(normalized_image_uint8)
    heatmap[image == 0] = [0, 0, 0]  # 保留背景
    return heatmap

def process_files(files, subdir, src_folder, output_folder,z):
    heat = np.zeros(shape=(256, 256))
    heats = []

    files.sort(key=lambda f: int(f.split('_')[-1].split('.')[0]))  # 按切片编号排序
    if z == 1:
        for file_name in files[::-1]:
            if file_name.startswith("axial_slice_") and file_name.endswith(".png"):
                num = file_name.split('_')[-1].split('.')[0]
                mask_path = os.path.join(subdir, f"axial_slice_{num}.png")
                if os.path.exists(mask_path):
                    heat += np.array(Image.open(mask_path).convert("L"))
                    heats.append(heat.copy())

        if heats:
            min_val = min(np.min(h) for h in heats)
            max_val = max(np.max(h) for h in heats)

            # 只保存最大 i 对应的热力图
            heat_image = generate_heatmap(heats[-1], min_val, max_val)
            output_subdir = os.path.relpath(subdir, src_folder)[:12]
            output_path = os.path.join(output_folder, output_subdir, "axial_heat.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            heat_image_pil = Image.fromarray(heat_image)
            heat_image_pil.save(output_path)
            print(f"Saved heatmap to {output_path}")
    elif z == 2:
        for file_name in files[::-1]:
            if file_name.startswith("coronal_slice_") and file_name.endswith(".png"):
                num = file_name.split('_')[-1].split('.')[0]
                mask_path = os.path.join(subdir, f"coronal_slice_{num}.png")
                if os.path.exists(mask_path):
                    heat += np.array(Image.open(mask_path).convert("L"))
                    heats.append(heat.copy())

        if heats:
            min_val = min(np.min(h) for h in heats)
            max_val = max(np.max(h) for h in heats)

            # 只保存最大 i 对应的热力图
            heat_image = generate_heatmap(heats[-1], min_val, max_val)
            output_subdir = os.path.relpath(subdir, src_folder)[:12]
            output_path = os.path.join(output_folder, output_subdir, "coronal_heat.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            heat_image_pil = Image.fromarray(heat_image)
            heat_image_pil.save(output_path)
            print(f"Saved heatmap to {output_path}")
    elif z == 3:
        for file_name in files[::-1]:
            if file_name.startswith("sagittal_slice_") and file_name.endswith(".png"):
                num = file_name.split('_')[-1].split('.')[0]
                mask_path = os.path.join(subdir, f"sagittal_slice_{num}.png")
                if os.path.exists(mask_path):
                    heat += np.array(Image.open(mask_path).convert("L"))
                    heats.append(heat.copy())

        if heats:
            min_val = min(np.min(h) for h in heats)
            max_val = max(np.max(h) for h in heats)

            # 只保存最大 i 对应的热力图
            heat_image = generate_heatmap(heats[-1], min_val, max_val)
            output_subdir = os.path.relpath(subdir, src_folder)[:12]
            output_path = os.path.join(output_folder, output_subdir, "sagittal_heat.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            heat_image_pil = Image.fromarray(heat_image)
            heat_image_pil.save(output_path)
            print(f"Saved heatmap to {output_path}")

def process_folders(src_folder, output_folder):
    for subdir, dirs, files in os.walk(src_folder):
        if 'axial' in subdir:
            process_files(files, subdir, src_folder, output_folder,1)
        if 'coronal' in subdir:
            process_files(files, subdir, src_folder, output_folder,2)
        if 'sagittal' in subdir:
            process_files(files, subdir, src_folder, output_folder,3)

# 定义文件夹路径
src_folder = ''
output_folder = ""

# 处理文件夹中的图像
process_folders(src_folder, output_folder)

import os
from PIL import Image

# def overlay_images(image_folder, heat_folder, output_folder):
#     for subdir, _, files in os.walk(image_folder):
#         if subdir == image_folder:
#             continue
#
#         # 获取相对路径，构建 heat 文件夹中的对应路径
#         relative_path = os.path.relpath(subdir, image_folder)
#         corresponding_heat_folder = os.path.join(heat_folder, relative_path)
#
#         if not os.path.exists(corresponding_heat_folder):
#             continue
#
#         output_sub_folder = os.path.join(output_folder, relative_path)
#         os.makedirs(output_sub_folder, exist_ok=True)
#
#         for file in files:
#             if file.startswith('image_') and file.endswith('.png'):
#                 image_file_path = os.path.join(subdir, file)
#                 image_num = file.split('_')[1].split('.')[0]
#                 heat_file_path = os.path.join(corresponding_heat_folder, f'heat_{image_num}.png')
#
#                 if os.path.exists(heat_file_path):
#                     # 打开 image 和 heat 图片
#                     image = Image.open(image_file_path).convert("RGBA")
#                     heat = Image.open(heat_file_path).convert("RGBA")
#
#                     # 确保两张图片的大小相同
#                     if image.size != heat.size:
#                         raise ValueError("Image and heat files must have the same dimensions")
#
#                     # 获取图片数据
#                     image_pixels = image.load()
#                     heat_pixels = heat.load()
#
#                     # 遍历每一个像素
#                     for y in range(image.height):
#                         for x in range(image.width):
#                             hr, hg, hb, ha = heat_pixels[x, y]
#                             # 检查是否不是黑色像素
#                             if (hr, hg, hb) != (0, 0, 0):
#                                 image_pixels[x, y] = (hr, hg, hb, ha)
#
#                     # 保存结果图片
#                     output_file_path = os.path.join(output_sub_folder, f'cheat_{image_num}.png')
#                     image.save(output_file_path)
#                     print(f"Saved: {output_file_path}")
#
# # 示例使用
# image_folder = 'E:\\barin_white'  # 替换为存储 image 文件的主文件夹路径
# heat_folder = 'E:\\brain_heat\\heat_syc'    # 替换为存储 heat 文件的主文件夹路径
# output_folder = 'E:\\brain_heat\\heat_combine' # 替换为你想要保存结果的主文件夹路径
#
# overlay_images(image_folder, heat_folder, output_folder)


# def overlay_images(image_folder, heat_folder, output_folder):
#     for subdir, _, files in os.walk(image_folder):
#         if subdir == image_folder:
#             continue
#
#         # 获取相对路径，构建 heat 文件夹中的对应路径
#         relative_path = os.path.relpath(subdir, image_folder)
#         corresponding_heat_folder = os.path.join(heat_folder, relative_path)
#
#         if not os.path.exists(corresponding_heat_folder):
#             continue
#
#         output_sub_folder = os.path.join(output_folder, relative_path)
#         os.makedirs(output_sub_folder, exist_ok=True)
#
#         for file in files:
#             if file.startswith('axial') and file.endswith('.png'):
#                 image_file_path = os.path.join(subdir, file)
#                 heat_file_path = os.path.join(corresponding_heat_folder, 'axial_heat.png')
#
#                 if os.path.exists(heat_file_path):
#                     # 打开 image 和 heat 图片
#                     image = Image.open(image_file_path).convert("RGBA")
#                     heat = Image.open(heat_file_path).convert("RGBA")
#
#                     # 确保两张图片的大小相同
#                     if image.size != heat.size:
#                         raise ValueError("Image and heat files must have the same dimensions")
#
#                     # 获取图片数据
#                     image_pixels = image.load()
#                     heat_pixels = heat.load()
#
#                     # 遍历每一个像素
#                     for y in range(image.height):
#                         for x in range(image.width):
#                             hr, hg, hb, ha = heat_pixels[x, y]
#                             # 检查是否不是黑色像素
#                             if (hr, hg, hb) != (0, 0, 0):
#                                 image_pixels[x, y] = (hr, hg, hb, ha)
#
#                     # 保存结果图片
#                     output_file_path = os.path.join(output_sub_folder, 'axial_com.png')
#                     image.save(output_file_path)
#                     print(f"Saved: {output_file_path}")
#             elif file.startswith('coronal') and file.endswith('.png'):
#                 image_file_path = os.path.join(subdir, file)
#                 heat_file_path = os.path.join(corresponding_heat_folder, 'coronal_heat.png')
#
#                 if os.path.exists(heat_file_path):
#                     # 打开 image 和 heat 图片
#                     image = Image.open(image_file_path).convert("RGBA")
#                     heat = Image.open(heat_file_path).convert("RGBA")
#
#                     # 确保两张图片的大小相同
#                     if image.size != heat.size:
#                         raise ValueError("Image and heat files must have the same dimensions")
#
#                     # 获取图片数据
#                     image_pixels = image.load()
#                     heat_pixels = heat.load()
#
#                     # 遍历每一个像素
#                     for y in range(image.height):
#                         for x in range(image.width):
#                             hr, hg, hb, ha = heat_pixels[x, y]
#                             # 检查是否不是黑色像素
#                             if (hr, hg, hb) != (0, 0, 0):
#                                 image_pixels[x, y] = (hr, hg, hb, ha)
#
#                     # 保存结果图片
#                     output_file_path = os.path.join(output_sub_folder, 'coronal_com.png')
#                     image.save(output_file_path)
#                     print(f"Saved: {output_file_path}")
#             elif file.startswith('sagittal') and file.endswith('.png'):
#                 image_file_path = os.path.join(subdir, file)
#                 heat_file_path = os.path.join(corresponding_heat_folder, 'sagittal_heat.png')
#
#                 if os.path.exists(heat_file_path):
#                     # 打开 image 和 heat 图片
#                     image = Image.open(image_file_path).convert("RGBA")
#                     heat = Image.open(heat_file_path).convert("RGBA")
#
#                     # 确保两张图片的大小相同
#                     if image.size != heat.size:
#                         raise ValueError("Image and heat files must have the same dimensions")
#
#                     # 获取图片数据
#                     image_pixels = image.load()
#                     heat_pixels = heat.load()
#
#                     # 遍历每一个像素
#                     for y in range(image.height):
#                         for x in range(image.width):
#                             hr, hg, hb, ha = heat_pixels[x, y]
#                             # 检查是否不是黑色像素
#                             if (hr, hg, hb) != (0, 0, 0):
#                                 image_pixels[x, y] = (hr, hg, hb, ha)
#
#                     # 保存结果图片
#                     output_file_path = os.path.join(output_sub_folder, 'sagittal_com.png')
#                     image.save(output_file_path)
#                     print(f"Saved: {output_file_path}")
#
# # 示例使用
# image_folder = ''  # 替换为存储 image 文件的主文件夹路径
# heat_folder = ''    # 替换为存储 heat 文件的主文件夹路径
# output_folder = '' # 替换为你想要保存结果的主文件夹路径
#
# overlay_images(image_folder, heat_folder, output_folder)

import os
from PIL import Image
import numpy as np

#批量堆叠三个解剖平面的肿瘤热力图到解剖平面图上
import os
from PIL import Image
import numpy as np


def process_images(src_dir1, src_dir2, dst_dir):
    # 遍历第一个主文件夹
    for root, dirs, files in os.walk(src_dir1):
        for dir_name in dirs:
            # 获取对应的子文件夹路径
            subdir1 = os.path.join(root, dir_name)
            subdir2 = subdir1.replace(src_dir1, src_dir2)
            out_subdir = subdir1.replace(src_dir1, dst_dir)

            # 定义三个文件夹名
            folders = ['axial', 'coronal', 'sagittal']
            for folder in folders:
                folder_path1 = os.path.join(subdir1, folder)
                folder_path2 = os.path.join(subdir2, folder)
                out_folder_path = os.path.join(out_subdir, folder)

                if os.path.exists(folder_path1) and os.path.exists(folder_path2):
                    # 只有在存在图片时才创建输出文件夹
                    if any(os.path.exists(os.path.join(folder_path2, img)) for img in os.listdir(folder_path1)):
                        os.makedirs(out_folder_path, exist_ok=True)

                    for img_name in os.listdir(folder_path1):
                        img_path1 = os.path.join(folder_path1, img_name)
                        img_path2 = os.path.join(folder_path2, img_name)

                        if os.path.exists(img_path2):
                            # 读取图片
                            img1 = Image.open(img_path1).convert('RGBA')
                            img2 = Image.open(img_path2).convert('RGBA')

                            # 转换为numpy数组
                            arr1 = np.array(img1)
                            arr2 = np.array(img2)

                            # 找到非黑色像素并替换为绿色
                            non_black = (arr2[..., 0] != 0) | (arr2[..., 1] != 0) | (arr2[..., 2] != 0)
                            arr1[non_black] = [0, 255, 0, 255]

                            # 转换回图片
                            result_img = Image.fromarray(arr1)

                            # 保存图片
                            result_img.save(os.path.join(out_folder_path, img_name))
                        else:
                            # 如果第二个文件夹中没有对应的图片，直接复制
                            os.makedirs(out_folder_path, exist_ok=True)
                            img1 = Image.open(img_path1)
                            img1.save(os.path.join(out_folder_path, img_name))


if __name__ == "__main__":
    src_dir1 = ""
    src_dir2 = ""
    dst_dir = ""

    process_images(src_dir1, src_dir2, dst_dir)

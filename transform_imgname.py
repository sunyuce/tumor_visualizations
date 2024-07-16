import os
import shutil


def rename_and_move_images(main_folder_path, new_main_folder_path):
    # 创建新的主文件夹
    if not os.path.exists(new_main_folder_path):
        os.makedirs(new_main_folder_path)

    # 遍历主文件夹中的所有子文件夹
    for subdir, _, files in os.walk(main_folder_path):
        if subdir == main_folder_path:
            continue
        # 创建新的子文件夹
        relative_path = os.path.relpath(subdir, main_folder_path)
        subprefix = relative_path[:12]
        new_subdir_path = os.path.join(new_main_folder_path, subprefix)
        if not os.path.exists(new_subdir_path):
            os.makedirs(new_subdir_path)

        # 过滤出文件夹中的所有图片文件
        images = [f for f in files if f.startswith('image_') and not f.startswith('image_mask')]
        # images = [f for f in files if f.startswith('image_mask_')]
        # 按照文件名中的数字排序
        images.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))
        # images.sort(key=lambda f: int(f.split('_')[2].split('.')[0]))

        # 重新命名并移动图片文件
        for index, filename in enumerate(images, start=0):
            old_file_path = os.path.join(subdir, filename)
            # new_file_name = f"image_mask_{index}.png"
            new_file_name = f"image_{index}.png"
            new_file_path = os.path.join(new_subdir_path, new_file_name)
            shutil.copy2(old_file_path, new_file_path)
            print(f"Copied and Renamed: {old_file_path} -> {new_file_path}")


# 使用方法
main_folder_path = 'E:\\tumor_data'  # 替换为主文件夹的实际路径
new_main_folder_path = 'E:\\brain_three\\brain'  # 替换为新主文件夹的实际路径
rename_and_move_images(main_folder_path, new_main_folder_path)

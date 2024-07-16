# SYC python learning
# 时间：2024/7/12 14:28
#保存vtp文件
# import os
# import shutil
#
#
# def rename_and_move_files(source_dir, target_dir):
#     # 确保目标文件夹存在，如果不存在则创建
#     if not os.path.exists(target_dir):
#         os.makedirs(target_dir)
#
#     # 遍历源文件夹下的所有文件
#     for filename in os.listdir(source_dir):
#         # 检查文件是否以_tumor.vtp结尾
#         if filename.endswith("_tumor.vtp"):
#             # 生成新文件名
#             new_filename = filename[:12] + "_tumor.vtp"
#             # 构造源文件路径和目标文件路径
#             source_path = os.path.join(source_dir, filename)
#             target_path = os.path.join(target_dir, new_filename)
#             # 移动并重命名文件
#             shutil.move(source_path, target_path)
#             print(f"Moved and renamed: {source_path} to {target_path}")
#
#
# # 调用函数，指定源文件夹和目标文件夹路径
# source_directory = "E:\\tumor_data_out"
# target_directory = "E:\\combine_tumor"
# rename_and_move_files(source_directory, target_directory)

#取符合条件的高亮大脑图
# import os
# import shutil
# def read_filenames_from_txt(txt_file):
#     with open(txt_file, 'r') as file:
#         filenames = file.read().splitlines()
#     return filenames
#
#
# def find_and_copy_subfolders(main_folder, subfolder_names, target_folder):
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)
#
#     for subfolder in subfolder_names:
#         src_folder = os.path.join(main_folder, subfolder)
#         dst_folder = os.path.join(target_folder, subfolder)
#         if os.path.exists(src_folder):
#             shutil.copytree(src_folder, dst_folder)
#             print(f"Copied {src_folder} to {dst_folder}")
#         else:
#             print(f"{src_folder} does not exist.")
#
#
# def rename_images_in_folders(target_folder):
#     for root, _, files in os.walk(target_folder):
#         png_files = [f for f in files if f.endswith('.png')]
#         png_files.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))
#
#         for idx, file in enumerate(png_files):
#             old_file = os.path.join(root, file)
#             new_file = os.path.join(root, f"image_{idx}.png")
#             os.rename(old_file, new_file)
#             print(f"Renamed {old_file} to {new_file}")
#
#
# def main(txt_file, main_folder, target_folder):
#     subfolder_names = read_filenames_from_txt(txt_file)
#     find_and_copy_subfolders(main_folder, subfolder_names, target_folder)
#     rename_images_in_folders(target_folder)
#
#
# # 设置参数
# txt_file = 'more_than_50.txt'  # txt文件路径
# main_folder = 'E:\\brain_three\\brain'  # 主文件夹路径
# target_folder = 'E:\\brain_three\\brain_50'  # 目标文件夹路径
#
# # 执行主函数
# main(txt_file, main_folder, target_folder)
import os
import shutil
def read_filenames_from_txt(txt_file):
    with open(txt_file, 'r') as file:
        filenames = file.read().splitlines()
    return filenames


def find_and_copy_subfolders(main_folder, subfolder_names, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for subfolder in subfolder_names:
        src_folder = os.path.join(main_folder, subfolder)
        dst_folder = os.path.join(target_folder, subfolder)
        if os.path.exists(src_folder):
            shutil.copytree(src_folder, dst_folder)
            print(f"Copied {src_folder} to {dst_folder}")
        else:
            print(f"{src_folder} does not exist.")

def main(txt_file, main_folder, target_folder):
    subfolder_names = read_filenames_from_txt(txt_file)
    find_and_copy_subfolders(main_folder, subfolder_names, target_folder)


# 设置参数
txt_file = 'more_than_50.txt'  # txt文件路径
main_folder = 'E:\\brain_three\\tumor_syc'  # 主文件夹路径
target_folder = 'E:\\brain_three\\tumor_50_out'  # 目标文件夹路径

# 执行主函数
main(txt_file, main_folder, target_folder)
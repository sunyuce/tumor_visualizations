#查看各个患者图片数量
import os


def process_folders(base_folder):
    nums = []
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    for sub_folder in os.listdir(base_folder):
        sub_folder_path = os.path.join(base_folder, sub_folder)
        if os.path.isdir(sub_folder_path):
            images = [f for f in os.listdir(sub_folder_path) if f.endswith('.png')]
            image_count = len(images) // 2
            if image_count>=50:
                print(os.path.relpath(sub_folder_path,base_folder)[:12])
            nums.append(image_count)
            # print(sub_folder_path)

    print("Nums array:", nums)
    print('max num:',max(nums))
    print('min num:',min(nums))

if __name__ == '__main__':
    base_folder = ''  # 替换为实际路径
    process_folders(base_folder)

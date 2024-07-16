#测试热力图堆叠
from PIL import Image

def overlay_images(source_img_path, target_img_path, output_img_path):
    # 打开源图片和目标图片
    source_img = Image.open(source_img_path).convert("RGBA")
    target_img = Image.open(target_img_path).convert("RGBA")

    # 确保两张图片的大小相同
    if source_img.size != target_img.size:
        raise ValueError("Source and target images must have the same dimensions")

    # 获取图片数据
    source_pixels = source_img.load()
    target_pixels = target_img.load()

    # 遍历每一个像素
    for y in range(source_img.height):
        for x in range(source_img.width):
            r, g, b, a = source_pixels[x, y]
            # 检查是否不是黑色像素
            if (r, g, b) != (0, 0, 0):
                target_pixels[x, y] = (r, g, b, a)

    # 保存结果图片
    target_img.save(output_img_path)

# 示例使用
source_img_path = 'heat/sagittal_heat.png'  # 替换为你的源图片路径
target_img_path = 'heat/sagittal_slice.png'  # 替换为你的目标图片路径
output_img_path = 'heat/result3.png'  # 替换为你想要保存的输出图片路径

overlay_images(source_img_path, target_img_path, output_img_path)

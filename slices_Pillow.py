#将二值图像切分为三个解剖平面方向上的三组图像，编号从0开始
import vtk
import os
# 读取一组 PNG 图像并组合成三维图像数据
def read_png_series(directory, file_prefix, extent, spacing):
    reader = vtk.vtkPNGReader()
    reader.SetFilePrefix(os.path.join(directory, file_prefix))
    reader.SetFilePattern("%s%d.png")
    reader.SetDataExtent(extent)
    reader.SetDataSpacing(spacing)
    reader.Update()
    return reader.GetOutput()


# 保存切面图像的函数
def save_slice(image, slice_orientation, output_path, slice_index=0):
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(image)
    reslice.SetOutputDimensionality(2)

    origin = image.GetOrigin()
    spacing = image.GetSpacing()
    extent = image.GetExtent()

    if slice_orientation == 'axial':  # xoy 平面
        reslice.SetResliceAxesDirectionCosines(1, 0, 0, 0, 1, 0, 0, 0, 1)
        reslice.SetResliceAxesOrigin(origin[0], origin[1], origin[2] + slice_index * spacing[2])
    elif slice_orientation == 'sagittal':  # yoz 平面
        reslice.SetResliceAxesDirectionCosines(0, -1, 0, 0, 0, 1, 1, 0, 0)
        reslice.SetResliceAxesOrigin(origin[0] + slice_index * spacing[0], origin[1], origin[2])
    elif slice_orientation == 'coronal':  # zoy 平面
        reslice.SetResliceAxesDirectionCosines(1, 0, 0, 0, 0, 1, 0, 1, 0)
        reslice.SetResliceAxesOrigin(origin[0], origin[1] + slice_index * spacing[1], origin[2])

    reslice.SetInterpolationModeToLinear()
    reslice.SetOutputSpacing(spacing[0], spacing[1], spacing[2])
    reslice.SetOutputExtent(0, 255, 0, 255, 0, 0)
    reslice.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(output_path)
    writer.SetInputConnection(reslice.GetOutputPort())
    writer.Write()


# 处理每个子文件夹
def process_subfolder(input_folder, output_folder, subfolder):
    subfolder_path = os.path.join(input_folder, subfolder)
    images = [f for f in os.listdir(subfolder_path) if f.endswith('.png')]
    if not images:
        return

    # 假设文件名前缀相同，例如 'image_'
    file_prefix = 'image_'
    num_images = len(images)
    extent = [0, 255, 0, 255, 0, num_images - 1]
    z = 0.00082 * (num_images ** 2) - 0.13561 * num_images + 7.38431
    spacing = [1.0, 1.0, z]

    image_data = read_png_series(subfolder_path, file_prefix, extent, spacing)

    axial_output_path = os.path.join(output_folder, subfolder, 'axial')
    sagittal_output_path = os.path.join(output_folder, subfolder, 'sagittal')
    coronal_output_path = os.path.join(output_folder, subfolder, 'coronal')

    for path in [axial_output_path, sagittal_output_path, coronal_output_path]:
        if not os.path.exists(path):
            os.makedirs(path)

    # 保存不同切片索引的图像
    for i in range(num_images):
        save_slice(image_data, 'axial', os.path.join(axial_output_path, f'axial_slice_{i}.png'), slice_index=i)
        # save_slice(image_data, 'sagittal', os.path.join(sagittal_output_path, f'sagittal_slice_{i}.png'), slice_index=(i*256)//num_images)
        # save_slice(image_data, 'coronal', os.path.join(coronal_output_path, f'coronal_slice_{i}.png'), slice_index=(i*256)//num_images)
    for i in range(256):
        save_slice(image_data, 'sagittal', os.path.join(sagittal_output_path, f'sagittal_slice_{i}.png'), slice_index=i)
        save_slice(image_data, 'coronal', os.path.join(coronal_output_path, f'coronal_slice_{i}.png'), slice_index=i)


# 主函数
def main(input_folder, output_folder):
    subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
    for subfolder in subfolders:
        process_subfolder(input_folder, output_folder, subfolder)


# 设置输入和输出文件夹
input_folder = ''
output_folder = ''

# 执行主函数
main(input_folder, output_folder)

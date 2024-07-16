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

    subfolder_output_path = os.path.join(output_folder, subfolder)
    if not os.path.exists(subfolder_output_path):
        os.makedirs(subfolder_output_path)

    # 保存不同切片索引的图像
    save_slice(image_data, 'axial', os.path.join(subfolder_output_path, 'axial_slice.png'),
               slice_index=(extent[4] + extent[5]) // 2)
    save_slice(image_data, 'sagittal', os.path.join(subfolder_output_path, 'sagittal_slice.png'),
               slice_index=(extent[0] + extent[1]) // 2)
    save_slice(image_data, 'coronal', os.path.join(subfolder_output_path, 'coronal_slice.png'),
               slice_index=(extent[2] + extent[3]) // 2)
    print('saved slices')


# 主函数
def main(input_folder, output_folder):
    subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
    for subfolder in subfolders:
        process_subfolder(input_folder, output_folder, subfolder)


# 设置输入和输出文件夹
input_folder = 'E:\\brain_three\\brain'
output_folder = 'E:\\brain_three\\brain_syc'

# 执行主函数
main(input_folder, output_folder)

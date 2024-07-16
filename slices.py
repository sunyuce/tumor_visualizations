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

    print(f"Origin: {origin}")
    print(f"Spacing: {spacing}")
    print(f"Extent: {extent}")

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
    # 变成256*256px
    reslice.SetOutputSpacing(spacing[0], spacing[1], spacing[2])
    reslice.SetOutputExtent(0, 255, 0, 255, 0, 0)
    reslice.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(output_path)
    writer.SetInputConnection(reslice.GetOutputPort())
    writer.Write()


# 设置 PNG 图像序列的路径和文件前缀
directory = 'TCGA_DU_6399_19830416'
file_prefix = 'image_'
extent = [0, 255, 0, 255, 0, 52]  # 设置图像的范围，假设有 52 张切片
spacing = [1.0, 1.0, 2.5]  # 设置图像数据在 x, y 和 z 方向上的间距

# 读取 PNG 图像序列
image_data = read_png_series(directory, file_prefix, extent, spacing)

# 保存切面图像
output_folder = 'slices'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 保存不同切片索引的图像
save_slice(image_data, 'axial', os.path.join(output_folder, 'axial_slice.png'),
           slice_index=(extent[4] + extent[5]) // 2)
save_slice(image_data, 'sagittal', os.path.join(output_folder, 'sagittal_slice.png'),
           slice_index=(extent[0] + extent[1]) // 2)
save_slice(image_data, 'coronal', os.path.join(output_folder, 'coronal_slice.png'),
           slice_index=(extent[2] + extent[3]) // 2)

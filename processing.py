# 时间：2024/7/4 15:48
import os
import vtk

def convert_images_to_vtp(image_folder, image_prefix, image_count, output_file):
    # 设置PNG阅读器
    png_reader = vtk.vtkPNGReader()
    png_reader.SetNumberOfScalarComponents(1) #单通道灰度图
    png_reader.SetFileDimensionality(2) #二维图像

    # 定义图像大小
    png_reader.SetDataExtent(0, 256, 0, 256, 0, image_count-1)
    png_reader.SetFilePrefix(image_prefix)
    png_reader.SetFilePattern("%s%d.png")
    png_reader.Update()
    png_reader.SetDataByteOrderToLittleEndian()
    z = 0.00082 * (image_count ** 2) - 0.13561 * image_count + 7.38431
    # a = 0.00082 , b = -0.13561 , c = 7.38431
    spacing = [1.0, 1.0, z]  # x, y 方向上的间距为 1 像素，z 方向上的间距为自定义像素
    png_reader.GetOutput().SetSpacing(spacing)

    # 高斯平滑
    gauss = vtk.vtkImageGaussianSmooth()
    gauss.SetInputConnection(png_reader.GetOutputPort())
    gauss.SetStandardDeviations(1.0, 1.0, 1.0)
    gauss.SetRadiusFactors(1.0, 1.0, 1.0)
    gauss.Update()

    # 计算轮廓
    contour = vtk.vtkMarchingCubes()
    gauss.GetOutput().SetSpacing(spacing)
    contour.SetInputConnection(gauss.GetOutputPort())
    contour.ComputeNormalsOn()
    contour.SetValue(0, 100)

    # 保存为VTP文件
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputConnection(contour.GetOutputPort())
    writer.Write()

def merge_vtp_files(vtp_file1, vtp_file2, output_file):
    # 读取第一个VTP文件
    reader1 = vtk.vtkXMLPolyDataReader()
    reader1.SetFileName(vtp_file1)
    reader1.Update()

    # 读取第二个VTP文件
    reader2 = vtk.vtkXMLPolyDataReader()
    reader2.SetFileName(vtp_file2)
    reader2.Update()

    # 设置第一个模型的颜色为灰色
    gray_color = vtk.vtkUnsignedCharArray()
    gray_color.SetNumberOfComponents(4)
    gray_color.SetName("Colors")
    num_points1 = reader1.GetOutput().GetNumberOfPoints()
    for i in range(num_points1):
        gray_color.InsertNextTuple4(200, 200, 200,138)  # 灰色

    reader1.GetOutput().GetPointData().SetScalars(gray_color)

    # 设置第二个模型的颜色为红色
    red_color = vtk.vtkUnsignedCharArray()
    red_color.SetNumberOfComponents(4)
    red_color.SetName("Colors")
    num_points2 = reader2.GetOutput().GetNumberOfPoints()
    for i in range(num_points2):
        red_color.InsertNextTuple4(0, 255, 0,255)  # 绿色

    reader2.GetOutput().GetPointData().SetScalars(red_color)

    # 合并两个模型
    append_filter = vtk.vtkAppendPolyData()
    append_filter.AddInputData(reader1.GetOutput())
    append_filter.AddInputData(reader2.GetOutput())
    append_filter.Update()

    # 写入合并后的模型到新的VTP文件
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(append_filter.GetOutput())
    writer.Write()

def process_folders(base_folder, output_folder,output_folder_combine):
    nums = []
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for sub_folder in os.listdir(base_folder):
        sub_folder_path = os.path.join(base_folder, sub_folder)
        if os.path.isdir(sub_folder_path):
            images = [f for f in os.listdir(sub_folder_path) if f.endswith('.png')]
            image_count = len(images) // 2
            nums.append(image_count)
            brain_prefix = os.path.join(sub_folder_path, "image_")
            tumor_prefix = os.path.join(sub_folder_path, "image_mask_")

            brain_vtp = os.path.join(output_folder, sub_folder + "_brain.vtp")
            tumor_vtp = os.path.join(output_folder, sub_folder + "_tumor.vtp")
            combined_vtp = os.path.join(output_folder_combine, sub_folder[:12] + ".vtp")

            convert_images_to_vtp(sub_folder_path, brain_prefix, image_count, brain_vtp)
            convert_images_to_vtp(sub_folder_path, tumor_prefix, image_count, tumor_vtp)
            merge_vtp_files(brain_vtp, tumor_vtp, combined_vtp)

    print("Nums array:", nums)

if __name__ == '__main__':
    base_folder = 'E:\\tumor_data'  # 替换为实际路径
    output_folder = 'E:\\tumor_data_out'  # 替换为实际路径
    output_folder_combine = 'E:\\tumor_data_out\\combine'  # 替换为实际路径
    process_folders(base_folder, output_folder,output_folder_combine)

# SYC python learning
# 时间：2024/7/4 9:33
import vtk
import os

# 定义渲染窗口、交互模式
aRender = vtk.vtkRenderer()
Renwin = vtk.vtkRenderWindow()
Renwin.AddRenderer(aRender)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(Renwin)

# 定义个图片读取接口
PNG_Reader = vtk.vtkPNGReader()
PNG_Reader.SetNumberOfScalarComponents(1)
PNG_Reader.SetFileDimensionality(2)  # 说明图像是二维的

# 定义图像大小，本行表示图像大小为（256*256）
PNG_Reader.SetDataExtent(0, 256, 0, 256, 0, 52)
# 设置图像的存放位置
name_prefix = ['TCGA_DU_6399_19830416/image_mask_']
PNG_Reader.SetFilePrefix(name_prefix[0])

# 设置图像前缀名字
PNG_Reader.SetFilePattern("%s%d.png")
PNG_Reader.Update()
PNG_Reader.SetDataByteOrderToLittleEndian()
spacing = [1.0, 1.0, 2.5]  # x, y 方向上的间距为 1 像素，z 方向上的间距为 2.5 像素
PNG_Reader.GetOutput().SetSpacing(spacing)

# 高斯平滑
gauss = vtk.vtkImageGaussianSmooth()
gauss.SetInputConnection(PNG_Reader.GetOutputPort())
gauss.SetStandardDeviations(1.0, 1.0, 1.0)
gauss.SetRadiusFactors(1.0, 1.0, 1.0)
gauss.Update()

# 计算轮廓的方法
contour = vtk.vtkMarchingCubes()
gauss.GetOutput().SetSpacing(spacing)
contour.SetInputConnection(gauss.GetOutputPort())
contour.ComputeNormalsOn()
contour.SetValue(0, 100)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.SetBackground([0.0, 0.0, 0.0])
renderer.AddActor(actor)

window = vtk.vtkRenderWindow()
window.SetSize(512, 512)
window.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

# 保存为VTP文件的函数
def save_vtp(file_name):
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(file_name)
    writer.SetInputConnection(contour.GetOutputPort())
    writer.Write()

# 指定文件夹路径
output_folder = 'vtp_models'
# 创建文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 开始显示
if __name__ == '__main__':
    save_vtp(os.path.join(output_folder, 'o2.vtp'))  # 保存文件
    window.Render()
    interactor.Initialize()
    interactor.Start()

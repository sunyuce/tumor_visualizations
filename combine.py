# 时间：2024/7/4 14:51
import os

import vtk

# 读取第一个VTP文件
reader1 = vtk.vtkXMLPolyDataReader()
reader1.SetFileName("vtp_models/o1.vtp")
reader1.Update()

# 读取第二个VTP文件
reader2 = vtk.vtkXMLPolyDataReader()
reader2.SetFileName("vtp_models/o2.vtp")
reader2.Update()

# 设置第一个模型的颜色为灰色
gray_color = vtk.vtkUnsignedCharArray()
gray_color.SetNumberOfComponents(4)
gray_color.SetName("Colors")
num_points1 = reader1.GetOutput().GetNumberOfPoints()
for i in range(num_points1):
    gray_color.InsertNextTuple4(128, 128, 128,138)  # 灰色半透明

reader1.GetOutput().GetPointData().SetScalars(gray_color)

# 设置第二个模型的颜色为红色
red_color = vtk.vtkUnsignedCharArray()
red_color.SetNumberOfComponents(4)
red_color.SetName("Colors")
num_points2 = reader2.GetOutput().GetNumberOfPoints()
for i in range(num_points2):
    red_color.InsertNextTuple4(255, 0, 0,255)  # 红色 完全不透明

reader2.GetOutput().GetPointData().SetScalars(red_color)

# 合并两个模型
append_filter = vtk.vtkAppendPolyData()
append_filter.AddInputData(reader1.GetOutput())
append_filter.AddInputData(reader2.GetOutput())
append_filter.Update()

# 写入合并后的模型到新的VTP文件
output_folder = "vtp_models"
output_filename = os.path.join(output_folder, "c2.vtp")
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(output_filename)
writer.SetInputData(append_filter.GetOutput())
writer.Write()

# 检查合并后的模型颜色
output = append_filter.GetOutput()
colors = output.GetPointData().GetScalars()
for i in range(output.GetNumberOfPoints()):
    color = colors.GetTuple4(i)
    # print(f"Point {i} color: {color}")

# 在窗口中显示合并后的模型
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(append_filter.GetOutput())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)  # 设置背景颜色

render_window.Render()
render_window_interactor.Start()

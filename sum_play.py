#来绘制z index拉伸图
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 定义二次多项式函数
def polynomial(x, a, b, c):
    return a * x**2 + b * x + c
#a = 0.00082 , b = -0.13561 , c = 7.38431
# 定义已知的点
x_data = np.array([88, 53, 20])
y_data = np.array([1.8, 2.5, 5])

# 使用 curve_fit 进行拟合
params, _ = curve_fit(polynomial, x_data, y_data)

# 拟合参数
a, b, c = params

# 打印拟合参数
print(f"Fitted parameters: a = {a}, b = {b}, c = {c}")

# 测试数组
array = [23, 20, 20, 20, 20, 20, 24, 22, 25, 24, 20, 24, 26, 20, 28, 22, 38, 40, 36, 36, 36, 26, 36, 71, 38, 53, 57, 51, 53, 60, 58, 56, 52, 58, 49, 60, 36, 38, 34, 32, 36, 36, 35, 36, 36, 42, 40, 37, 37, 37, 36, 36, 37, 36, 38, 38, 35, 56, 23, 31, 36, 24, 51, 26, 36, 48, 60, 48, 26, 27, 51, 48, 60, 50, 36, 73, 32, 32, 20, 32, 28, 30, 21, 25, 20, 24, 20, 21, 21, 21, 32, 22, 20, 30, 28, 80, 32, 20, 20, 32, 22, 20, 22, 21, 22, 23, 32, 28, 88, 88]

# 计算参数值
param_values = [polynomial(x, a, b, c) for x in array]

# 输出结果
print(param_values)

# 可视化结果
plt.plot(array, param_values, 'o', label='Data Points')
plt.xlabel('Number of MRI')
plt.ylabel('Z index Value')
plt.title('Number of MRI vs Z index Value')
plt.legend()
plt.show()

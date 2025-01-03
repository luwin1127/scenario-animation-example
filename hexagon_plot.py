import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
from PIL import Image

# 定义参数
rc = 6
dy = 2 * rc
dx = rc * np.sqrt(3)
A = np.pi / 3 * np.arange(1, 8)
num = 0

# 用于存储每个六边形的中心坐标
centers = []


# 画图
fig, ax = plt.subplots()

ax.set_facecolor('w')  # 设置背景颜色为白色
ax.set_xlim(-45, 45)  # 设置x轴范围
ax.set_ylim(-50, 50)  # 设置y轴范围
ax.set_aspect('equal')  # 设置坐标轴比例相等
ax.axis('off')  # 关闭坐标轴

# plt.figure(facecolor='w', figsize=(6, 7))  # 创建一个新的图形窗口，并设置背景颜色为白色和大小
# plt.axis([-45, 45, -50, 50])  # 设置坐标轴范围
# plt.axis('equal')  # 设置坐标轴比例相等，使得x和y轴的单位长度一致
# plt.axis('off')  # 关闭坐标轴
# plt.box(on=True)  # 显示边框

# 读取图片
sat_red_img = Image.open('sat_red.png')
sat_red_img_arr = np.array(sat_red_img)
sat_blue_img = Image.open('sat_blue.png')
sat_blue_img_arr = np.array(sat_blue_img)

# 卫星中心坐标比例
sat_rate = 4

# 用于存储已经绘制过的六边形中心坐标
drawn_centers = set()


# ===================================== #
#                 开始绘图               #
# ===================================== #
for yk in np.concatenate((np.arange(0, 101, dy), np.arange(0, -101, -dy))):
    # 定义y=f(x)的直线方程
    def yfun(x): return np.sqrt(3) * x / 3 + yk  
    for xk in np.concatenate((np.arange(0, 101, dx), np.arange(0, -101, -dx))):
        xp = xk
        yp = yfun(xp)
        # 存入六边形中心坐标
        center = (xp, yp)
        centers.append(center)
        # ===================================== #
        # 在六边形中心插入图片（插进六边形的fig里）#
        # ===================================== #
        # sat_red = ax.imshow(sat_red_img, 
        #                     extent=((xp-sat_rate),
        #                             (xp+sat_rate),
        #                             (yp-sat_rate),
        #                             (yp+sat_rate)), 
        #                     zorder=3)    # zorder确保图片在最上层
        if center not in drawn_centers and -50 < xp < 50 and -50 < yp < 50:
            T = (xp + 1j * yp) + rc * np.exp(1j * A) * 2 / np.sqrt(3)  # 将点(xp, yp)转换为复数形式，并进行变换
            num += 1
            print(f'第{num}个六边形加粗')
            ax.plot(T.real, T.imag, color=[0.7176, 0.7176, 0.7176], linewidth=1.5)  # 绘制变换后的六边形
            ax.plot(xp, yp, color=[1, 1, 1], linewidth=1.5)  # 绘制原始的点(xp, yp)
            ax.text(xp, yp, str(len(drawn_centers)), ha='center', va='center', fontsize=6) # 添加编号

            # 记录已绘制的六边形中心坐标
            drawn_centers.add(center)
            print(f'六边形中心坐标：{center}')

# ===================================== #
#                 绘图结束               #
# ===================================== #

# ===================================== #
#                 插入卫星               #
# ===================================== #
# 将已绘制的中心坐标转换为列表
drawn_centers_list = list(drawn_centers)

scaling_index = 200
attrition_case1 = pd.read_excel('attrition_record.xlsx', sheet_name=0)
x_d_case1 = np.round(attrition_case1.x_d / scaling_index)
x_k_case1 = np.round(attrition_case1.x_k / scaling_index)
y_d_case1 = np.round(attrition_case1.y_d / scaling_index)
y_k_case1 = np.round(attrition_case1.y_k / scaling_index)

# 红蓝方卫星集群数量
red_num, blue_num = 9, 9
x_d_num = x_d_case1[0]
x_k_num = x_k_case1[0]
y_d_num = y_d_case1[0]
y_k_num = y_k_case1[0]

# 列出来要画红蓝方卫星的坐标点
drawn_centers_num = np.random.choice(range(0, len(drawn_centers)), (red_num+blue_num), replace=False)
drawn_centers_red = drawn_centers_num[0:red_num]                    # 红方卫星坐标点
drawn_centers_blue = drawn_centers_num[red_num:red_num+blue_num]    # 蓝方卫星坐标点

# 在红方坐标点上画红方卫星图片
for center_index in drawn_centers_red:
    xp, yp = drawn_centers_list[center_index]
    ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

# 在蓝方坐标点上画蓝方卫星图片
for center_index in drawn_centers_blue:
    xp, yp = drawn_centers_list[center_index]
    ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

# ===================================== #
#                 插入结束               #
# ===================================== #

# 保存图片
fig.savefig('confrontation_scenario.png', dpi=300)

# 显示图形
plt.show()  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.animation import FuncAnimation

# 辅助函数，将matplotlib的figure对象转换为PIL的Image对象
def fig2img(fig):
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    w,h = fig.canvas.get_width_height()
    img = Image.frombytes("RGBA", (w,h), buf)
    img = img.convert('RGB')
    return img

# 辅助函数，保存gif图片
def save_gif(images, filename, duration):
    frames = []
    for img in images:
        frames.append(img)
    images[0].save(filename, format='GIF', append_images=frames[1:], save_all=True, duration=duration, loop=0)

# 定义参数
rc = 6
dy = 2 * rc
dx = rc * np.sqrt(3)
A = np.pi / 3 * np.arange(1, 8)

# 画图
fig, ax = plt.subplots()
ax.set_facecolor('w')  # 设置背景颜色为白色
ax.set_xlim(-45, 45)  # 设置x轴范围
ax.set_ylim(-50, 50)  # 设置y轴范围
ax.set_aspect('equal')  # 设置坐标轴比例相等
ax.axis('off')  # 关闭坐标轴

# 读取图片
sat_red_img = Image.open('sat_red.png')
sat_red_img_arr = np.array(sat_red_img)
sat_blue_img = Image.open('sat_blue.png')
sat_blue_img_arr = np.array(sat_blue_img)

# 卫星中心坐标比例
sat_rate = 4

# 用于存储已经绘制过的六边形中心坐标
drawn_centers = set()

# 读取Excel文件
scaling_index = 200
attrition_case1 = pd.read_excel('attrition_record.xlsx', sheet_name=0)
x_d_case1 = np.round(attrition_case1.x_d / scaling_index)
x_k_case1 = np.round(attrition_case1.x_k / scaling_index)
y_d_case1 = np.round(attrition_case1.y_d / scaling_index)
y_k_case1 = np.round(attrition_case1.y_k / scaling_index)

# 动画完成需要的图片数
animation_num = len(x_d_case1)

# 初始化gif图片列表
images = []

for i in range(animation_num):
    # 清除之前的图像
    ax.clear()
    ax.set_facecolor('w')  # 设置背景颜色为白色
    ax.set_xlim(-45, 45)  # 设置x轴范围
    ax.set_ylim(-50, 50)  # 设置y轴范围
    ax.set_aspect('equal')  # 设置坐标轴比例相等
    ax.axis('off')  # 关闭坐标轴

    # 列出来要画红蓝方卫星的坐标点
    drawn_centers_num = np.random.choice(range(0, len(drawn_centers)), (x_d_case1[i]+x_k_case1[i]+y_d_case1[i]+y_k_case1[i]), replace=False)
    drawn_centers_x_d = drawn_centers_num[0 : x_d_case1[i]]  # 红方直瞄群坐标点
    drawn_centers_x_k = drawn_centers_num[x_d_case1[i] : x_d_case1[i]+x_k_case1[i]]  # 红方动能群坐标点
    drawn_centers_y_d = drawn_centers_num[x_d_case1[i]+x_k_case1[i] : x_d_case1[i]+x_k_case1[i]+y_d_case1[i]]  # 蓝方直瞄群坐标点
    drawn_centers_y_k = drawn_centers_num[x_d_case1[i]+x_k_case1[i]+y_d_case1[i] : x_d_case1[i]+x_k_case1[i]+y_d_case1[i]+y_k_case1[i]]  # 蓝方动能群坐标点

    # 在红方直瞄群坐标点上画卫星
    for center_index in drawn_centers_x_d:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 在红方动能群坐标点上画卫星
    for center_index in drawn_centers_x_k:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 在蓝方直瞄群坐标点上画卫星
    for center_index in drawn_centers_y_d:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 在蓝方动能群坐标点上画卫星
    for center_index in drawn_centers_y_k:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 保存每一帧
    images.append(fig2img(fig))

# 保存为gif
save_gif(images, 'animation.gif', duration=0.2)

# 显示图形
plt.show()


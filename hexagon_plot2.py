import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
from PIL import Image

# ===================================== #
#                子函数部分              #
# ===================================== #
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

# ===================================== #
#                 初始参数               #
# ===================================== #
# 设置蜂窝形状的中心点坐标
x_center, y_center = 0, 0
# 设置蜂窝的边长和旋转角度
side_length = 1.0
angle = np.pi / 3 
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

# 读取图片
sat_red_img = Image.open('sat_red.png')
sat_red_img_arr = np.array(sat_red_img)
sat_blue_img = Image.open('sat_blue.png')
sat_blue_img_arr = np.array(sat_blue_img)
sat_up_img = Image.open('sat_up.png')
sat_up_img_arr = np.array(sat_up_img)
sat_down_img = Image.open('sat_down.png')
sat_down_img_arr = np.array(sat_down_img)

# 卫星中心坐标比例
sat_rate = 4

# 用于存储已经绘制过的六边形中心坐标
drawn_centers = set()


# 计算顶点坐标
vertices = []
for i in range(7):
    angle_offset = i * angle
    x = x_center + side_length * np.cos(angle_offset)
    y = y_center + side_length * np.sin(angle_offset)
    vertices.append((x, y))

# 绘制正六边形
plt.plot(*zip(*vertices), fillstyle='none')

# 添加网格线
plt.grid(True)

# 设置坐标轴范围
plt.xlim(0, 2)
plt.ylim(0, 2)

# 隐藏坐标轴
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# 设置标题和标签
plt.title('蜂窝形状')
plt.xlabel('X 轴')
plt.ylabel('Y 轴')

# 显示图形
plt.show()
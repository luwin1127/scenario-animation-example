import SatelliteSwarm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
# 设置蜂窝的边长和旋转角度
side_length = 10
angle = np.pi / 3 * np.arange(1, 8)
num = 0
# 设置蜂窝形状的中心点坐标
x0_odd, y0_odd = 0, 0
x0_even, y0_even = 1.5 * side_length, (np.sqrt(3)/2) * side_length
row = 14
col = 4

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
sat_rate = side_length/2

# 动画完成需要的图片数
animation_num = 23

# 初始化gif图片列表
images = []

# 卫星初始位置编号
red_sat_num = [8, 10, 17, 22, 29, 28, 43, 42, 40]
blue_sat_num = [5, 12, 14, 19, 21, 33, 35, 32, 34, 38]

# 建立卫星对象
red_sat0 = SatelliteSwarm.SatelliteSwarm(col, row, red_sat_num[0])

# 使用列表推导式自动建立 SatelliteSwarm 对象
red_sats = [SatelliteSwarm.SatelliteSwarm(col, row, num) for num in red_sat_num]
blue_sats = [SatelliteSwarm.SatelliteSwarm(col, row, num) for num in blue_sat_num]

# 如果需要通过编号访问特定卫星，可以这样做：
for i, red_sat in enumerate(red_sats):
    print(f"Red satellite {i} at position {red_sat.sat_num}")

for i, blue_sat in enumerate(blue_sats):
    print(f"Blue satellite {i} at position {blue_sat.sat_num}")

# 导入卫星数据
# 坐标点
drawn_centers_x_total = [[8, 10, 17, 22, 29, 28, 43, 42, 40],
                        [12, 18, 17, 22, 29, 28, 43, 42],
                        [8, 10, 17, 22, 29, 28, 43],
                        [8, 10, 17, 22, 29, 28],
                        [8, 10, 17, 22, 29, 28, 43, 46],
                        [8, 10, 17, 22, 29, 28, 43],
                        [8, 10, 17, 22, 29, 28, 43],
                        [8, 10, 17, 22, 29, 28, 43],
                        [8, 10, 17, 22, 29, 28, 43]]
                   
drawn_centers_y_total = [[5, 12, 14, 19, 21, 33, 35, 32, 34, 38],
                        [5, 12, 14, 19, 21, 33, 35, 32],
                        [5, 12, 14, 19, 21, 33],
                        [5, 12, 14, 19, 21],
                        [5, 12, 14, 19, 21, 48, 52, 44],
                        [5, 12, 14, 19],
                        [5, 12],
                        [],
                        []]

# ===================================== #
#                 插入卫星               #
# ===================================== #
for scenario_num in range(0,animation_num):
    # 画图
    fig, ax = plt.subplots(dpi=300)
    ax.set_facecolor('w')  # 设置背景颜色为白色
    ax.set_xlim(-side_length, side_length*3*col)  # 设置x轴范围
    ax.set_ylim(-side_length * np.sqrt(3)/2 * row, side_length * np.sqrt(3)/2)  # 设置y轴范围
    ax.set_aspect('equal')  # 设置坐标轴比例相等
    ax.axis('off')  # 关闭坐标轴

    # 用于存储每个六边形的中心坐标
    centers = []

    # ===================================== #
    #                 开始绘图               #
    # ===================================== #
    for j in range(0,row):      # 行数
        for i in range(0,col):  # 列数
            if (j % 2) == 0:    # 为偶数行
                x_center = x0_odd + 3 * i * side_length
                y_center = y0_odd - np.sqrt(3) * (j/2) * side_length
            else:   # 为奇数行
                x_center = x0_even + 3 * i * side_length
                y_center = y0_even - np.sqrt(3) * np.ceil(j/2) * side_length
            center = (x_center, y_center)
            centers.append(center)

            # 一次性计算所有顶点的坐标
            x_vertices = x_center + side_length * np.cos(angle)
            y_vertices = y_center + side_length * np.sin(angle)

            # 绘制正六边形
            ax.plot(x_vertices, y_vertices, color=[0.7176, 0.7176, 0.7176], linewidth=1.5)

    # ===================================== #
    #                 绘图结束               #
    # ===================================== #    
    # 将已绘制的中心坐标转换为列表
    drawn_centers_list = centers
    if scenario_num == 0:
        for i, red_sat in enumerate(red_sats):
            center_index = red_sat.sat_num
            # 插入卫星图片
            xp, yp = drawn_centers_list[center_index]
            ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)
        for i, blue_sat in enumerate(blue_sats):
            center_index = blue_sat.sat_num
            # 插入卫星图片
            xp, yp = drawn_centers_list[center_index]
            ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)
    else:
        for i, red_sat in enumerate(red_sats):
            center_index = red_sat.update()
            # 插入卫星图片
            xp, yp = drawn_centers_list[center_index]
            ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)
        for i, blue_sat in enumerate(blue_sats):
            center_index = blue_sat.update()
            # 插入卫星图片
            xp, yp = drawn_centers_list[center_index]
            ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 保存每一帧
    images.append(fig2img(fig))
    ax.clear()
    plt.close()

# 保存为gif
save_gif(images, 'confrontation_scenario_changes_case2.gif', duration=350) # 单位是毫秒 (ms)
print("--== 画图结束 ==--")
# ===================================== #
#                 插入结束               #
# ===================================== #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
from PIL import Image

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
ax.clear()
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

# 动画完成需要的图片数
animation_num = len(x_d_case1)

# 初始化gif图片列表
images = []

# 红蓝方卫星集群数量
x_d_num0 = int(x_d_case1[0])
x_k_num0 = int(x_k_case1[0])
y_d_num0 = int(y_d_case1[0])
y_k_num0 = int(y_k_case1[0])

drawn_centers_num = np.random.choice(range(0, len(drawn_centers)), (x_d_num0+x_k_num0+y_d_num0+y_k_num0), replace=False)
drawn_centers_x_d = drawn_centers_num[0 : x_d_num0]                                                     # 红方直瞄群坐标点
drawn_centers_x_k = drawn_centers_num[x_d_num0 : x_d_num0+x_k_num0]                                     # 红方动能群坐标点
drawn_centers_y_d = drawn_centers_num[x_d_num0+x_k_num0 : x_d_num0+x_k_num0+y_d_num0]                   # 蓝方直瞄群坐标点
drawn_centers_y_k = drawn_centers_num[x_d_num0+x_k_num0+y_d_num0 : x_d_num0+x_k_num0+y_d_num0+y_k_num0] # 蓝方动能群坐标点

for scenario_num in range(0,animation_num):
    # 画图
    fig, ax = plt.subplots()
    ax.set_facecolor('w')  # 设置背景颜色为白色
    ax.set_xlim(-45, 45)  # 设置x轴范围
    ax.set_ylim(-50, 50)  # 设置y轴范围
    ax.set_aspect('equal')  # 设置坐标轴比例相等
    ax.axis('off')  # 关闭坐标轴

    # ===================================== #
    #                 开始绘图               #
    # ===================================== #
    for yk in np.concatenate((np.arange(0, 101, dy), np.arange(0, -101, -dy))):
        # 定义y=f(x)的直线方程
        def yfun(x): return np.sqrt(3) * x / 3 + yk  
        for xk in np.concatenate((np.arange(0, 101, dx), np.arange(0, -101, -dx))):
            xp = xk
            yp = yfun(xp)
            
            if center not in drawn_centers and -50 < xp < 50 and -50 < yp < 50:
                T = (xp + 1j * yp) + rc * np.exp(1j * A) * 2 / np.sqrt(3)  # 将点(xp, yp)转换为复数形式，并进行变换
                ax.plot(T.real, T.imag, color=[0.7176, 0.7176, 0.7176], linewidth=1.5)  # 绘制变换后的六边形


    # ===================================== #
    #                 绘图结束               #
    # ===================================== #
    # 将已绘制的中心坐标转换为列表
    drawn_centers_list = list(drawn_centers)

    # 红蓝方卫星集群数量
    x_d_num = int(x_d_case1[scenario_num])
    x_k_num = int(x_k_case1[scenario_num])
    y_d_num = int(y_d_case1[scenario_num])
    y_k_num = int(y_k_case1[scenario_num])

    drawn_centers_num = np.random.choice(range(0, len(drawn_centers)), (x_d_num+x_k_num+y_d_num+y_k_num), replace=False)
    drawn_centers_x_d = drawn_centers_num[0 : x_d_num]                                                  # 红方直瞄群坐标点
    drawn_centers_x_k = drawn_centers_num[x_d_num : x_d_num+x_k_num]                                    # 红方动能群坐标点
    drawn_centers_y_d = drawn_centers_num[x_d_num+x_k_num : x_d_num+x_k_num+y_d_num]                    # 蓝方直瞄群坐标点
    drawn_centers_y_k = drawn_centers_num[x_d_num+x_k_num+y_d_num : x_d_num+x_k_num+y_d_num+y_k_num]    # 蓝方动能群坐标点

    # 在红方直瞄群坐标点上画卫星
    for center_index in drawn_centers_x_d:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 在红方直瞄群坐标点上画卫星
    for center_index in drawn_centers_x_k:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 在红方直瞄群坐标点上画卫星
    for center_index in drawn_centers_y_d:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 在红方直瞄群坐标点上画卫星
    for center_index in drawn_centers_y_k:
        xp, yp = drawn_centers_list[center_index]
        ax.imshow(sat_blue_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

    # 保存图片
    savefig_str = './img/confronation_scenario_'+str(scenario_num)+'.jpg'
    fig.savefig(savefig_str, dpi=300)

    # 保存每一帧
    images.append(fig2img(fig))
    ax.clear()
    plt.close()

# 保存为gif
save_gif(images, './img/confrontation_scenario_changes.gif', duration=200) # 单位是毫秒 (ms)
# ===================================== #
#                 插入结束               #
# ===================================== #

# # 保存图片
# fig.savefig('confrontation_scenario.png', dpi=300)

# # 显示图形
# plt.show()  
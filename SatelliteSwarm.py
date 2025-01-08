import numpy as np
import numpy as np
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

class SatelliteSwarm:
    def __init__(self, col, row, drawn_centers_num):
        self.sat_num = drawn_centers_num
        self.col = col
        self.row = row
        self.update_parity()
        self.action = 'none'

    def update_parity(self):
        temp = np.floor(self.sat_num / 4) + 1 # 每个六边形编号对应的行数 = 向下取整（编号/列数）+1
        if temp % 2 == 0:   # 判断行数的奇偶性
            self.parity = 'odd'
        else:
            self.parity = 'even'
    
    def move_12_clock(self):
        # 更新行数的奇偶性
        self.update_parity()
        self.action = '12 clock'
        self.sat_num = self.sat_num - 2 * self.col

        return self.sat_num
    
    def move_2_clock(self):
        # 更新行数的奇偶性
        self.update_parity()
        self.action = '2 clock'
        if self.parity == 'odd':
            self.sat_num = self.sat_num - (self.col-1) 
        elif self.parity == 'even':
            self.sat_num = self.sat_num - self.col

        return self.sat_num
    
    def move_4_clock(self):
        # 更新行数的奇偶性
        self.update_parity()
        self.action = '4 clock'
        if self.parity == 'odd':
            self.sat_num = self.sat_num + (self.col+1) 
        elif self.parity == 'even':
            self.sat_num = self.sat_num + self.col

        return self.sat_num
    
    def move_6_clock(self):
        # 更新行数的奇偶性
        self.update_parity()
        self.action = '6 clock'
        self.sat_num = self.sat_num + 2 * self.col

        return self.sat_num
    
    def move_8_clock(self):
        # 更新行数的奇偶性
        self.update_parity()
        self.action = '8 clock'
        if self.parity == 'odd':
            self.sat_num = self.sat_num + self.col
        elif self.parity == 'even':
            self.sat_num = self.sat_num + (self.col-1)

        return self.sat_num
    
    def move_10_clock(self):
        # 更新行数的奇偶性
        self.update_parity()
        self.action = '10 clock'
        if self.parity == 'odd':
            self.sat_num = self.sat_num - self.col
        elif self.parity == 'even':
            self.sat_num = self.sat_num - (self.col+1)

        return self.sat_num
    
    def update(self):
        # 上方边缘的坐标点
        if self.sat_num == 0:   # 左上角
            move_direction = np.random.randint(3,5)
        elif self.sat_num in np.arange(1, self.col): # 除了左上角的上方边缘（奇数行）
            move_direction = np.random.randint(3,6)
        elif self.sat_num in np.arange(self.col, 2*self.col-1):   # 除了右上角的上方边缘（偶数行）
            move_direction = np.random.randint(2,7)
        elif self.sat_num == 2*self.col - 1: # 右上角
            move_direction = np.random.randint(4,7)
        # 右方边缘的坐标点
        elif self.sat_num in np.arange(2*self.col-1, (2*self.col * self.row/2) - 1, 2*self.col): # 除了右下角的右方边缘（7被包括进去了，但是没有关系，因为如果self.sat_num=7，就肯定会进入前面的elif()）
            move_direction = np.random.choice([1,4,5,6],1)
        elif self.sat_num == 2*self.col * self.row/2 - 1:       # 右下角
            move_direction = np.random.choice([1,6],1)
        # 左方边缘的坐标点
        elif self.sat_num in np.arange(0, 2*self.col * (self.row/2 - 1), 2*self.col): # 除了左下角的左方边缘（0被包括进去了，但是没有关系，因为如果self.sat_num=0，就肯定会进入前面的elif()）
            move_direction = np.random.randint(1,5)
        elif self.sat_num == 2*self.col * (self.row/2 - 1):   # 左下角
            move_direction = np.random.randint(1,4)
        # 下方边缘的坐标点
        elif self.sat_num in np.arange((2*self.col * self.row/2) - self.col, (2*self.col * self.row/2) - 1): # 除了右下角的下方边缘（偶数行）
            move_direction = np.random.choice([1,2,6],1)
        elif self.sat_num in np.arange(2*self.col * (self.row/2 - 1), 2*self.col * (self.row/2 - 1)+self.col):   # 除了左下角的下方边缘（奇数行）（48被包括进去了，但是没有关系，因为如果self.sat_num=48，就肯定会进入前面的elif()）
            move_direction = np.random.choice([1,2,3,5,6],1)
        # 不在边缘的坐标点
        else:
            move_direction = np.random.randint(1,7)

        if move_direction == 1:
            self.move_12_clock()
        elif move_direction == 2:
            self.move_2_clock()
        elif move_direction == 3:
            self.move_4_clock()
        elif move_direction == 4:
            self.move_6_clock()
        elif move_direction == 5:
            self.move_8_clock()
        elif move_direction == 6:
            self.move_10_clock()

        return self.sat_num

if __name__ == '__main__':
    
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
    sat_up_img = Image.open('sat_up.png')
    sat_up_img_arr = np.array(sat_up_img)

    # 卫星中心坐标比例
    sat_rate = side_length/2

    # 动画完成需要的图片数
    animation_num = 23

    # 初始化gif图片列表
    images = []

    # 卫星初始位置编号
    sat_num = np.random.randint(0, 2*col * row/2)
    print(sat_num)

    # 建立卫星对象
    red_sat1 = SatelliteSwarm(col, row, sat_num)

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
            center_index = sat_num
        else:
            center_index = red_sat1.update()

        # 插入卫星图片
        xp, yp = drawn_centers_list[center_index]
        if scenario_num != animation_num-1:
            ax.imshow(sat_red_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)
        else:
            ax.imshow(sat_up_img_arr, extent=(xp-sat_rate, xp+sat_rate, yp-sat_rate, yp+sat_rate), zorder=3)

        # 保存每一帧
        images.append(fig2img(fig))
        ax.clear()
        plt.close()

    # 保存为gif
    save_gif(images, 'confrontation_scenario_changes_single.gif', duration=350) # 单位是毫秒 (ms)
    print("--== 画图结束 ==--")
    # ===================================== #
    #                 插入结束               #
    # ===================================== #
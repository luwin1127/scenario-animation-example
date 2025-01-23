import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from PIL import Image

# 读取图片
mario_img = Image.open('mario.png')
mushroom_img = Image.open('mushroom.png')

# 设置画布
fig, ax = plt.subplots()
plt.axis('off')

ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-0.5, 10.5)

ax.vlines(np.arange(11), 0, 10)
ax.hlines(np.arange(11), 0, 10)

# 画蘑菇
mushroom = ax.imshow(mushroom_img, extent=(9, 10, 9, 10))

# 画马里奥
mario_x = 1
mario_y = 1
mario = ax.imshow(mario_img, extent=(mario_x - 1, mario_x, mario_y - 1, mario_y))



def move():
    global mario_x, mario_y
    if mario_x == 10 == mario_y: # 吃到蘑菇了噢
        mario_x = mario_y = 1
        return True
    elif mario_x == 10:
        mario_y += 1
    elif mario_y == 10:
        mario_x += 1
    else:
        if np.random.random() < 0.5:
            mario_x += 1
        else:
            mario_y += 1

    return False # 还没吃到蘑菇呢！


def init():
    pass

def update(frame):
    mario.set_extent((mario_x - 1, mario_x, mario_y - 1, mario_y))

	# 若吃到蘑菇则隐藏蘑菇，避免两张图片重叠，更好看一点
    if move():
        mushroom.set_alpha(0)
    else:
        mushroom.set_alpha(1)



ani = FuncAnimation(fig, update, frames=range(180), blit=False, interval=300,
                              repeat=False, init_func=init)
plt.show()
ani.save('mario_like_mushroom.gif')

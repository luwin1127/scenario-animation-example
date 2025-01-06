import numpy as np
class SatelliteSwarm:
    def __init__(self, col, row, drawn_centers_num, sat_rate):
        self.drawn_centers_num = drawn_centers_num
        self.sat_rate = sat_rate
        self.col = col
        self.row = row
        temp = np.floor(self.drawn_centers_num / 4) + 1 # 每个六边形编号对应的行数 = 向下取整（编号/列数）+1
        if temp % 2 == 0:   # 判断行数的奇偶性
            self.parity = 'odd'
        else:
            self.parity = 'even'
    
    def move_12_clock(self):
        self.drawn_centers_num = self.drawn_centers_num - 2 * self.col
        return self.drawn_centers_num
    
    def move_2_clock(self):
        if self.parity == 'odd':
            self.drawn_centers_num = self.drawn_centers_num - (self.col-1) 
        elif self.parity == 'even':
            self.drawn_centers_num = self.drawn_centers_num - self.col

        return self.drawn_centers_num
    
    def move_4_clock(self):
        if self.parity == 'odd':
            self.drawn_centers_num = self.drawn_centers_num + (self.col+1) 
        elif self.parity == 'even':
            self.drawn_centers_num = self.drawn_centers_num + self.col

        return self.drawn_centers_num
    
    def move_6_clock(self):
        self.drawn_centers_num = self.drawn_centers_num + 2 * self.col

        return self.drawn_centers_num
    
    def move_8_clock(self):
        if self.parity == 'odd':
            self.drawn_centers_num = self.drawn_centers_num + self.col
        elif self.parity == 'even':
            self.drawn_centers_num = self.drawn_centers_num + (self.col-1)

        return self.drawn_centers_num
    
    def move_10_clock(self):
        if self.parity == 'odd':
            self.drawn_centers_num = self.drawn_centers_num - self.col
        elif self.parity == 'even':
            self.drawn_centers_num = self.drawn_centers_num - (self.col+1)

        return self.drawn_centers_num
    



if __name__ == '__main__':
    red_sat1 = SatelliteSwarm(11, 14)
    print(red_sat1.move_12_clock())
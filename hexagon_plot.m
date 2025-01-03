clc;clear;close all; 


%% 定义参数
% 定义圆的半径
rc=6; 
% 计算圆的直径dy和边长dx，这里假设是正六边形
dy=2*rc;dx=rc*sqrt(3); 
% 创建一个1到7的数组
A = 1:7; 
% 将数组中的每个元素乘以π/3，用于后续的角度计算
A=pi/3*A; 
% 初始化计数器
num=0; 

%% 画图
figure('Color',[1,1,1],'Position',[900,200,600,700]) 
% 外层循环，y方向的遍历
for yk=[0:dy:100,0:-dy:-100] 
    % 计算y=f(x)的直线方程
%     yfun=inline(['sqrt(3)*x/3+',num2str(yk)]); 
    % 内层循环，x方向的遍历
    for xk=[0:dx:100,0:-dx:-100] 
        % 将xk赋值给xp，用于后续计算
        xp=xk; 
        yp=yfun(xp,yk); 
         % 如果点(xp, yp)在(-50, 50)的范围内
        if -50<xp && xp<50 && -50<yp && yp<50
            % 将点(xp, yp)转换为复数形式，并进行变换
            T = [xp+1i*yp]+rc*exp(1i*A)*2/sqrt(3); 
            num=num+1; 
            fprintf('第%d个六边形加粗\n',num); 
            plot(T,'Color',[0.7176,0.7176,0.7176],'LineWidth',1.5);
            hold on; 
            plot(xp,yp) % 绘制原始的点(xp, yp)
        end
    end
end
axis([-45 45 -50 50]);
axis equal; % 设置坐标轴比例相等，使得x和y轴的单位长度一致
axis off;
box on;

% 计算y=f(x)的直线方程
function yp = yfun(x,yk)
yp = sqrt(3)*x/3 + yk;
end

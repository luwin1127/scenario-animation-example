clc;clear;close all; 


%% �������
% ����Բ�İ뾶
rc=6; 
% ����Բ��ֱ��dy�ͱ߳�dx�������������������
dy=2*rc;dx=rc*sqrt(3); 
% ����һ��1��7������
A = 1:7; 
% �������е�ÿ��Ԫ�س��Ԧ�/3�����ں����ĽǶȼ���
A=pi/3*A; 
% ��ʼ��������
num=0; 

%% ��ͼ
figure('Color',[1,1,1],'Position',[900,200,600,700]) 
% ���ѭ����y����ı���
for yk=[0:dy:100,0:-dy:-100] 
    % ����y=f(x)��ֱ�߷���
%     yfun=inline(['sqrt(3)*x/3+',num2str(yk)]); 
    % �ڲ�ѭ����x����ı���
    for xk=[0:dx:100,0:-dx:-100] 
        % ��xk��ֵ��xp�����ں�������
        xp=xk; 
        yp=yfun(xp,yk); 
         % �����(xp, yp)��(-50, 50)�ķ�Χ��
        if -50<xp && xp<50 && -50<yp && yp<50
            % ����(xp, yp)ת��Ϊ������ʽ�������б任
            T = [xp+1i*yp]+rc*exp(1i*A)*2/sqrt(3); 
            num=num+1; 
            fprintf('��%d�������μӴ�\n',num); 
            plot(T,'Color',[0.7176,0.7176,0.7176],'LineWidth',1.5);
            hold on; 
            plot(xp,yp) % ����ԭʼ�ĵ�(xp, yp)
        end
    end
end
axis([-45 45 -50 50]);
axis equal; % ���������������ȣ�ʹ��x��y��ĵ�λ����һ��
axis off;
box on;

% ����y=f(x)��ֱ�߷���
function yp = yfun(x,yk)
yp = sqrt(3)*x/3 + yk;
end

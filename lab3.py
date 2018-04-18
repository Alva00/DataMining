import matplotlib
import numpy as np
import pandas as pd


def main1():
	x = np.linspace(-2, 2, 50)
	y1 = 0.5 * x + 1.5
	y2 = x ** 2
	with open('file.csv', 'w') as file:
		file.write("x, y, z \n")
		for (a, b, c) in zip(x, y1, y2):
			file.write("%f, %f, %f \n"%(a, b, c))
	file.close()

def main2(filename):
	csvfile = pd.read_csv(filename)
	x = list(csvfile['x'])
	y1 = list(csvfile['y1'])
	y2 = list(csvfile['y2'])
    plt.figure(num=3) # 定义一个图像窗口：编号为3；大小为(8, 5).
    plt.plot(x, y2)                        # 绘制(x,y)曲线
    plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--') 
    plt.xlim((-2.0, 2.0))   # 设置坐标轴的范围
    plt.ylim((-2.0, 3.0))   
    plt.xlabel('x')     # 设置坐标轴的名称
    plt.ylabel('y')
    ax = plt.gca()      
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')   # 你可以把bottom改成其它的观察一下变化
    ax.yaxis.set_ticks_position('left') 
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0)) 
    plt.show()


if __name__ == '__main__':
	main1()

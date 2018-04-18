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
def main(filename):
    csvfile = pd.read_csv(filename)
    x = list(csvfile.iloc[:,0])
    y1 = list(csvfile.iloc[:,1])
    y2 = list(csvfile.iloc[:,2])
    
    plt.figure(num=3) # 定义一个图像窗口：编号为3；大小为(8, 5).
    l1, = plt.plot(x, y1, label='linear line')   
    l2, = plt.plot(x, y2, color='red', linewidth=1.0, linestyle='--', label='square line')
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
    x0 = -1
    y0 = x0**2
    plt.plot([x0, x0,], [0, y0,], 'k--', linewidth=2.5)
    x1 = 1.5
    y1 = 2.25
    plt.legend(handles=[l1, l2], labels=['y1 = 0.5x+1.5', 'y2 = x^2'], loc='best')  
    plt.scatter([x0, ], [y0, ], s=50, color='b')   # 把需要标注的点标出
    plt.annotate(r'$0.5x+1=%s$' % y1, xy=(x1, y1), 
                 xycoords='data', xytext=(+30, -30),textcoords='offset points', fontsize=16,
                 arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
    plt.show() 


if __name__ == '__main__':
	main2()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string
import jieba
import re


def main1():
    x = np.linspace(-2, 2, 50)
    y1 = 0.5 * x + 1.5
    y2 = x ** 2
    with open('file.csv', 'w') as file:
        file.write("x, y, z \n")
        for (a, b, c) in zip(x, y1, y2):
            file.write("%f, %f, %f \n" % (a, b, c))
    file.close()


def main2(filename):
    csvfile = pd.read_csv(filename)
    ''' 分别得到x y1 y2共三个向量 '''
    x = list(csvfile.iloc[:, 0])
    y1 = list(csvfile.iloc[:, 1])
    y2 = list(csvfile.iloc[:, 2])

    ''' 定义一个窗口 '''
    plt.figure(1)
    ''' 在窗口中画图 '''
    l1, = plt.plot(x, y1, label='linear line')
    l2, = plt.plot(x, y2, color='red', linewidth=1.0, linestyle='--', label='square line')
    ''' 设置坐标轴范围 '''
    plt.xlim((-2.0, 2.0))
    plt.ylim((-2.0, 3.0))
    ''' 分别设置x和y轴刻度 '''
    new_ticks_x = np.linspace(-2.0, 2.0, 9)
    new_ticks_y = np.linspace(-2.0, 3.0, 6)
    plt.xticks(new_ticks_x)
    plt.yticks(new_ticks_y)
    ''' 获得当前坐标轴信息 '''
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ''' 设置图例位置 '''
    # plt.legend(loc='lower left')
    ''' 在途中划线和点 '''
    x0 = -1
    y0 = x0**2
    plt.plot([x0, x0, ], [0, y0, ], 'k--', linewidth=2.5)
    plt.scatter([x0,], [y0, ], s=50, color='b')
    x1 = 1.5
    y1 = 2.25
    plt.plot([x1, x1, ], [0, y1, ], 'k--', linewidth=2.5)
    plt.scatter([x1, ], [y1, ], s=50, color='b')
    ''' 图例信息及位置 '''
    plt.legend(handles=[l1, l2], labels=['y1 = 0.5x+1.5', 'y2 = x^2'], loc='best')
    ''' 标注 '''
    plt.annotate(r'$0.5x+1=%s$' % y1, xy=(x1, y1),
                 xycoords='data', xytext=(+30, -30), textcoords='offset points', fontsize=16,
                 arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
    plt.show()

def clean1(text):
    pattern = re.compile(r"(南方(.+))讯（.+）|"
    r"本报讯.+\)|"
    r"\w{0,2}：(.+)|"
    r"南方\w{0,3}记者 (.+)?报道|"
    r"本版\w{0,2}/(.{1,25})?", re.S)
    r = pattern.sub("", text).strip()
    return r

def main3():
    patten0 = r'(<DOC_FORETOPIC>=)(.+)'
    patten1 = r'(<SYS_TOPIC>=)(.+)'
    patten2 = r'(<DOC_SUBTOPIC>=)(.+)'

    fore_topic = ''
    sys_topic = ''
    sub_topic = ''
    with open ('text.txt','r') as f:
        for line in f:
            tmp0 = re.search(patten0,line)
            tmp1 = re.search(patten1,line)
            tmp2 = re.search(patten2,line)
            if tmp0!=None:
                fore_topic += tmp0.group(2)
            if tmp1!=None:
                sys_topic += tmp1.group(2)
            if tmp2!=None:
                sub_topic += tmp2.group(2)
    print('fore_topic : ',fore_topic)
    print('sys_topic : ',sys_topic)
    print('sub_topic : ',sub_topic)

''' 清洗 text1函数 '''
def clean2(text):
    pattern = re.compile(r"(南方(.+))讯 （.+）|"
    r"中国哈哈哈(.+) |"
    r"（.+）", re.S)
    r = pattern.sub("", text).strip()
    return r

''' 清洗text2 函数 '''
def clean3(text):
    pattern = re.compile(r"(南方(.+))讯 （.+）|"
    r"\w{0,6}：(.+)|"
    r"南方日报记者.+|"
    r"中国哈哈哈.+|"
    r"（.+）", re.S)
    r = pattern.sub("", text).strip()
    return r

''' text1 + text2 清洗 '''
def main4():
    ''' 数据清洗 '''
    cleaned_text = ''
    with open('text4.txt','r') as f:
        for line in f:
            cleaned_text += clean3(line).strip('\n').strip()
        print(cleaned_text)
    f.close()
    ''' 分词并统计 '''
    character_count = 0
    punctuation_count = 0
    numeric_count = 0
    char2 = 0
    char3 = 0
    char4 = 0
    more_char = 0
    punc = string.punctuation
    with open('text4ans.txt', 'w') as ans1:
        seg_list = jieba.cut(cleaned_text)
        for i in seg_list:
            if i.isdigit():
                numeric_count += 1
            elif i in punc:
                punctuation_count += 1
            else:
                character_count += len(re.findall(r'[\u4e00-\u9fff]', i))
                if len(i) == 2:
                    char2 += 1
                elif len(i) == 3:
                    char3 += 1
                elif len(i) == 4:
                    char4 += 1
                elif len(i) > 4:
                    more_char += 1
        print("汉字个数: %d"%character_count)
        print("标点个数: %d"%punctuation_count)
        print("数字个数: %d"%numeric_count)
        print("2字词个数: %d"%char2)
        print("3字词个数: %d"%char3)
        print("4字词个数: %d"%char4)
        print("多于4字词个数: %d"%more_char)
    ans1.close()
    
    ''' 画柱状图 '''
    x_tick = ["character", "punctuation", "number", "2-char", "3-char", '4-char', 'more-char']
    plt.figure(2)
    y_tick = [character_count, punctuation_count, numeric_count, char2, char3, char4, more_char]
    plt.bar(x_tick, y_tick)
    for x, y in zip(x_tick, y_tick):
        plt.text(x, y, '%d' %y, ha='center', va='bottom')
    plt.show()


if __name__ == "__main__":
    main4()
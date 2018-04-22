import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string
import jieba
import re


''' text1 + text2 清洗 '''
def main():
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
    main()
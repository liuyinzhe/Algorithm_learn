# 拷贝自 NW全局比对算法原理及python实现 (考虑gap长度)
# https://cloud.tencent.com/developer/article/1614162?ivk_sa=1024320u

import argparse
import numpy as np


# 比较两个碱基分数， gaps的分数考虑在 cal_score
def diff(first, second):
    if first == second:
        return match 
    else:
        return mismatch

def cal_score(seq1, seq2):

    nrow = len(seq1)
    ncol = len(seq2)

    scores = np.zeros((nrow, ncol))
    path = np.zeros((nrow, ncol))
    # 初始化第一行第一列
    for index1 in range(nrow):
        scores[index1,0] = gap * index1
        path[index1,0] = 0 #上面

    for index2 in range(ncol):
        scores[0,index2] = gap * index2
        path[0, index2] = 2 #左侧


    for num1 in range(1, nrow):
        for num2 in range(1, ncol):

            # 得到上面，斜上和左侧的结果
            last_score = [scores[num1 - 1, num2], scores[num1 - 1, num2 - 1], scores[num1, num2 - 1]]
            change_score = diff(seq1[num1], seq2[num2])
            current_score = []

            if path[num1 - 1 , num2] == 0:
                current_score.append(scores[num1-1, num2] + extend) # 上面
            else:
                current_score.append(scores[num1-1, num2] + gap)

            current_score.append(scores[num1-1, num2 - 1] + change_score) # 斜上

            if path[num1 , num2 -1] == 2:
                current_score.append(scores[num1, num2-1] + extend) # 左侧
            else:
                current_score.append(scores[num1, num2-1] + gap)    

            current_index = current_score.index(max(current_score)) # 当前索引，不是0就gap

            scores[num1, num2] = max(current_score)

            path[num1, num2] = current_index


    return scores, path


def cal_seq(scores, path):
    index1 = len(seq1) - 1
    index2 = len(seq2) -1

    top = ''
    middle = ''
    bottom = ''

    while True:
        if path[index1, index2] == 1:
            top += seq1[index1]
            bottom += seq2[index2]

            if seq1[index1] == seq2[index2]:
                middle += '|'
            else:
                middle += ' '

            index1 -= 1
            index2 -= 1

        elif path[index1, index2] == 0:
            top += seq1[index1]
            bottom += '-'
            middle += ' '

            index1 -= 1

        else:
            top += '-'
            bottom += seq2[index2]
            middle += ' '

            index2 -= 1 

        
        top_num = len(top) - top.count('-')
        bottom_num = len(bottom) - bottom.count('-')
        if top_num == max(len(seq1), len(seq2))-1 or bottom_num == max(len(seq1), len(seq2))-1:
            break

    return top, middle, bottom

def getArgs(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-seq1", help = "", required = True)
    parser.add_argument("-seq2", help = "", required = True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    #args = getArgs()
    #seq1 = "_" + args.seq1
    #seq2 = "_" + args.seq2
    seq1 = 'CGATATCGTAGGCGTCGATGGAGAGCTAGAT'
    seq2 = 'TATCGTAGGCGTCGATGGAGAGCTAGATCGA'

    match=5  # 或者别的分数
    mismatch=-5
    gap=-10  
    extend = -0.5  

    scores,path = cal_score(seq1, seq2)
    top, middle, bottom = cal_seq(scores, path)

    print(top[::-1])
    print(middle[::-1])
    print(bottom[::-1])

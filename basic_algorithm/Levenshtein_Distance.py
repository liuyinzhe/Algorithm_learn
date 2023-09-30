

def Levenshtein_Distance(str1, str2):
    """
    计算字符串 str1 和 str2 的编辑距离
    :param str1
    :param str2
    :return:
    """
    matrix = [[ i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    print(matrix)
    '''
    DP 表格
    [ i/j "" b d
      ""  [0,1,2]
      a   [1,2,3]
      b   [2,3,4]
      c   [3,4,5]
    ]

    str1 列  i
    str2 行  j
    '''
    # 跳过矩阵的 第一行第一列 matrix[0:0],方便 i-1 j-1 进行比较
    for i in range(1, len(str1)+1):
        # i 123
        for j in range(1, len(str2)+1):
            # j 12
            # 每个字符进行判断， offset d 变量，不等时 等于1
            if(str1[i-1] == str2[j-1]):
                d = 0
            else:
                d = 1
            # 更新 DP 表格(matrix)， 取最小的 打分进行替换，寻找当前最小解
            
            '''
            # 目标:matrix[i][j]
            # 删除罚分 +1 
            插入 目标上一行对应 位置 matrix[i-1][j] +1
            目标右下侧斜对角线上一个 位置 matrix[i-1][j-1]
            删除 目标左侧1列对应 位置  matrix[i][j-1]+1
            '''
            matrix[i][j] = min(matrix[i-1][j]+1, matrix[i][j-1]+1, matrix[i-1][j-1]+d)
        #返回DP打分表最后末尾的打分
    #print(matrix)
    '''
    [ i/j "" b d
      ""  [0,1,2]
      a   [1,1,2]
      b   [2,1,2]
      c   [3,2,2]
    ]
    '''
    return matrix[len(str1)][len(str2)]
 
 
print(Levenshtein_Distance("abc", "bd"))

'''
https://blog.csdn.net/sinat_26811377/article/details/102652547
'''

def global_align(x, y, s_match=1, s_mismatch=-1, s_gap=-2):
    '''
    retrun align_x, align_y, distance  
    '''
    scoring_matrix = [] 
    '''
    scoring_matrix=[
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    '''
    for i in range(len(y) + 1): # 0,1,2...y
        scoring_matrix.append([0] * (len(x) + 1)) # 初始化为 [0,0,0]
    
    '''
    scoring_matrix=[   # x seq
    #1    [0,0,0],
    #y    [-2,-2,-2],
    #2    [-4,-4,-4]
    ]
    '''
    for i in range(len(y) + 1):
        scoring_matrix[i][0] = s_gap * i
    '''
    A=[
        
        [0,-2,-4],
        [-2,-2,-2],
        [-4,-4,-4]
    ]
    '''
    for i in range(len(x) + 1):
        scoring_matrix[0][i] = s_gap * i
    #print(scoring_matrix)
    # 矩阵 更新数值
    for i in range(1, len(y) + 1):
        for j in range(1, len(x) + 1):
            # 计算几个数字的最大值
            '''
            A[i][j - 1] + s_gap,  A[1][0] 位置 更新一次 A[1][0] = -2 + (-2)
            A[i - 1][j] + s_gap,  A[0][1]  位置 更新一次 A[0][1] = -2 + (-2)
            next_step = 
            A[i - 1][j - 1]       A[0][0] 位置 +
            tmp1 = (s_match if (y[i - 1] == x[j - 1] and y[i - 1] != '-') else 0)  # 当A
            '''

            scoring_match,scoring_mismatch,scoring_gap = (0,0,0)
            if (y[i - 1] == x[j - 1] and y[i - 1] != '-'): # 
                scoring_match = s_match
            if (y[i - 1] != x[j - 1] and y[i - 1] != '-' and x[j - 1] != '-'):
                scoring_mismatch = s_mismatch
            if (y[i - 1] == '-' or x[j - 1] == '-'):
                scoring_gap = s_gap
            
            scoring_matrix[i][j] = max(
                scoring_matrix[i][j - 1] + s_gap,
                scoring_matrix[i - 1][j] + s_gap,
                scoring_matrix[i - 1][j - 1] + scoring_match + scoring_mismatch + scoring_gap
            )

    align_X = ""
    align_Y = ""
    i = len(x)
    j = len(y)
    #print(scoring_matrix)
    while i > 0 or j > 0:
        flag = "match"
        current_score = scoring_matrix[j][i]
        #X 取 i，y 取 j
        # 两个序列一致
        '''

        IF(1)沿着对角移动：
        当前位置对应碱基  m[x-1][y-1] 相等  并且  对角位置 +1（Match_s） 等于 当前路径打分or
        当前位置对应碱基 m[x-1][y-1]不等，并且  对角位置 -1(mismatch_s) 等于 当前路径 打分  or
        当前位置对应碱基 m[x-1][y-1]相等且都是“-” 并且对角位置 -2(Gap_s) 等于 当前路径 打分or
        Elif(2)  Y轴 插入 x轴 左移 
        X轴 坐标 大于0；左侧 + gap(-2) 等于当前位置打分
        Else：(3) X 轴插入 ，y轴 上移

        '''
        if i > 0 and j > 0 and (
                # 序列相同，且不是gap"-"， and  当前打分等于 对角线 +1
                ((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == scoring_matrix[j - 1][i - 1] + s_match) or # 左上 上1 相等
                # 序列不相等，且都不是gap"-",  and 当前打分 对角线  -1
                ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == scoring_matrix[j - 1][i - 1] + s_mismatch) or  # 错配
                # 序列一致，都是"-", and 当前打分 对角线  -2
                ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == scoring_matrix[j - 1][i - 1] + s_gap) # 有gap的情况，序列一致
                #
                #
                #
        ):
            flag = "match"
            align_X = x[i - 1] + align_X
            align_Y = y[j - 1] + align_Y
            i = i - 1
            j = j - 1
        elif i > 0 and (current_score == scoring_matrix[j][i - 1] + s_gap): # Y有gap # A[j][i - 1] 左下打分
            #print(current_score,A[j][i - 1],s_gap)
            flag = "YGap"
            align_X = x[i - 1] + align_X
            align_Y = "-" + align_Y
            i = i - 1  #左移动
        else: # # X有gap
            # print(((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == scoring_matrix[j - 1][i - 1] + s_match) or
            # ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == scoring_matrix[j - 1][i - 1] + s_mismatch) or 
            # ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == scoring_matrix[j - 1][i - 1] + s_gap) 
            # )
            flag = "X,Gap"
            align_X = "-" + align_X
            align_Y = y[j - 1] + align_Y
            j = j - 1 # 上移动
        #print("align_X",align_X,flag,current_score,"y"+str(j),"x"+str(i))
        #print("align_Y",align_Y,flag,current_score,"y"+str(j),"x"+str(i))
    return  align_X, align_Y, scoring_matrix[len(y)][len(x)]

print(global_align("GAATTCAGTTA","GGATCGA"))

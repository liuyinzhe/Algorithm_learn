def getBMBC(pattern):
    '''
    # 预生成坏字符表
    bad character 除去最后一个字符的每个字符 
    记录每个字符在 pattern 中的坐标，对应0-base  则是末尾无法对齐的 next 索引号
    main_str    EXAAAAN
    index       0123456
    pattern     EXAMPL
    BMBC value  123456
    L 对不上，则移动到6 坐标
    '''
    BMBC = dict()
    for i in range(len(pattern) - 1):
        #取每个字母（除最后一个）
        char = pattern[i]
        #print(pattern[i],i + 1)
        # E 1
        # X 2
        # A 3
        # M 4
        # P 5
        # L 6
        # 记录坏字符最右位置（不包括模式串最右侧字符）

        BMBC[char] = i + 1
        #print(BMBC)
        # EXAMPLE
        # 123456
        # {'E': 1}
        # {'E': 1, 'X': 2}
        # {'E': 1, 'X': 2, 'A': 3}
        # {'E': 1, 'X': 2, 'A': 3, 'M': 4}
        # {'E': 1, 'X': 2, 'A': 3, 'M': 4, 'P': 5}
        # {'E': 1, 'X': 2, 'A': 3, 'M': 4, 'P': 5, 'L': 6}
    return BMBC

def getBMGS(pattern):
    '''
    pattern 首尾 截取 kmer 查看是否有重复的

    当序列与中有重复时，数值存储为 最后出现的坐标（BMBC中的坐标，用于移动跳过），跳过更多坐标
    坐标长度 -> main_str 的移动坐标
    '''
    # 预生成好后缀表
    BMGS = dict()

    # 无后缀仅根据坏字移位符规则
    BMGS[''] = 0

    for i in range(len(pattern)):

        # 好后缀
        GS = pattern[len(pattern) - i - 1:]
        #print(GS,len(pattern) - i - 1)
        #EXAMPLE
        # E 6
        # LE 5
        # PLE 4
        # MPLE 3
        # AMPLE 2
        # XAMPLE 1
        # EXAMPLE 0
        for j in range(len(pattern) - i - 1):
            # 匹配部分
            NGS = pattern[j:j + i + 1]
            # 
            #print(GS,NGS,j,j+i+1)
            #EXAMPLE
            # 
            #
            # G NG
            # E E 0 1  E
            # E X 1 2  EX
            # E A 2 3  EXA
            # E M 3 4  EXAM
            # E P 4 5  EXAMP
            # E L 5 6  EXAMPL

            # G NG
            # LE EX 0 2 LE  EX|AMPL
            # LE XA 1 3 LE  E|XA|MPL
            # LE AM 2 4 LE  EX|AM|PL
            # LE MP 3 5 LE  EXA|MP|L
            # LE PL 4 6 LE  EXAM|PL

            # PLE EXA 0 3 PLE EXA|MPL
            # PLE XAM 1 4 PLE E|XAM|PL
            # PLE AMP 2 5 PLE EX|AMP|L
            # PLE MPL 3 6 PLE EXA|MPL

            # MPLE EXAM 0 4 EXAM|PL
            # MPLE XAMP 1 5 E|XAMP|L
            # MPLE AMPL 2 6 EX|AMPL

            # AMPLE EXAMP 0 5 EXAMP|L
            # AMPLE XAMPL 1 6 E|XAMPL

            # XAMPLE EXAMPL 0 6 EXAMPL
            # 记录模式串中好后缀最靠右位置
            #print(GS,NGS)
            # pattern，开头取的kmer 与 末尾取的kmer  相等
            if GS == NGS:
                # 当序列与中有重复时， 跳过，数值存储为 最后出现的坐标，跳过更多坐标
                BMGS[GS] = len(pattern) - j - i - 1  # NGS[j:j+i+1]
                #print(GS,NGS,'#',len(pattern),j,i,-1)
                #E E # 7 0 0 -1
            #{'': 0, 'E': 6}
    return BMGS

def BM(string, pattern):
    """
    Boyer-Moore算法实现字符串查找
    """
    pattern_length = len(pattern) # 搜索序列 长度 # pattern_length
    string_length = len(string)  # 目标搜索序列 长度 #string_length
    i = 0  # string_length 目标序列坐标 逐渐增加
    j = pattern_length # pattern 长度坐标 逐渐减少
    indies = [] # 存储匹配的第一位索引，0-base
    BMBC = getBMBC(pattern=pattern)  # 坏字符表
    BMGS = getBMGS(pattern=pattern)  # 好后缀表
    #print(BMGS)
    #{'': 0, 'E': 6}
    while i < string_length:  # i index ，从0开始
        while (j > 0):
            #坐标 超过 n 搜索对象长度
            if i + j -1 >= string_length: # 当无法继续向下搜索就返回值
                return indies

            # 主串判断匹配部分
            # i,当前搜索的第一位，j 长度，末尾比较 （-1 变为索引）
            a = string[i + j - 1:i + pattern_length]
            

            # 模式串判断匹配部分
            b = pattern[j - 1:]
            #print(a,b,i + j - 1,":",i + pattern_length,"#",j - 1,"-")
            # EXAMPLE

            # S E 6 : 7 # 6 -
            # P E 13 : 14 # 6 -
            # E E 15 : 16 # 6 -  # a,b 相等，最后一位相等 ，j = j-1 ，取值则 变为末尾两位 LE
            # LE LE 14 : 16 # 5 -# 匹配位置，a,b 相等  ，j = j-1 ，取值则 变为末尾三位 PLE
            # PLE PLE 13 : 16 # 4 -
            # MPLE MPLE 12 : 16 # 3 -
            # IMPLE AMPLE 11 : 16 # 2 -
            # L E 22 : 23 # 6 -
            # E E 23 : 24 # 6 -
            # LE LE 22 : 24 # 5 -
            # PLE PLE 21 : 24 # 4 -
            # MPLE MPLE 20 : 24 # 3 -
            # AMPLE AMPLE 19 : 24 # 2 -
            # XAMPLE XAMPLE 18 : 24 # 1 -
            # EXAMPLE EXAMPLE 17 : 24 # 0 -
            # 当前位匹配成功则继续匹配,最后一位置匹配上了， J pattern_length 减少1，取上一位做比对
            if a == b:
                j = j - 1

            # 当前位匹配失败根据规则移位
            else:
                # setdefault 键值查找，找不到返回默认值，最后坐标，或者起始坐标； 有的话的就多动的最长 坐标长度
                i = i + max(BMGS.setdefault(b[1:], pattern_length), j - BMBC.setdefault(string[i + j - 1], 0))
                j = pattern_length

            # 匹配成功返回匹配位置
            if j == 0:
                indies.append(i)
                i += 1
                j = len(pattern)

main_str='HERE IS A SIMPLE EXAMPLE'
pattern_str='EXAMPLE'
pattern_len = len(pattern_str)
print("main_str lenght",len(main_str))
print("pattern_str",pattern_len)
index_list = BM(main_str,pattern_str) # 存储坐标第一个
#print(index_list)
for idx in index_list:
    print(idx,idx+pattern_len,main_str[idx:idx+pattern_len])


'''
HERE IS A SIMPLE EXAMPLE
0123456789
        1112131415
EXAMPLE
123456
#https://blog.csdn.net/chiang97912/article/details/83005577
'''

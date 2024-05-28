from functools import cmp_to_key
'''
// 代码来源  https://blog.csdn.net/baidu_41860619/article/details/118071986
根据C++ 代码转python代码重写
'''
MATCH = 1
DIS_MATCH = -1
INDEL = -3
INDEL_CHAR = '-'


class ResUnit:
    '''
    # 一次双序列比对后的结果
    '''
    #def __init__(self, str1,str2,res1,res2,tag,score):
    def __init__(self):

        self.str1 = ''    # 原始序列1
        self.str2 = ''    # 原始序列2
        self.res1 = ''    # 结果序列1
        self.res2 = ''    # 结果序列2
        self.score = int()   # 序列总得分，反映两个序列的相似程度 
        self.tag = int()     # 禁止迭代多次


class SingleSeq:
    '''
    # 一个序列被整合后的样子
    '''
    def __init__(self):

        self.str = ''    # 一个序列的原始序列
        self.res = ''    # 一个序列被整合后的样子

class BacktrackingUnit:
    '''
    # 一个序列被整合后的样子
    '''
    def __init__(self):

        self.goUp = 0       # 是否向上回溯
        self.goLeftUp = 0   # 是否向左上回溯
        self.goLeft = 0     # 是否向左回溯
        self.score = 0	    # 得分矩阵第(i, j)这个单元的分值

def max3(a:int, b:int, c:int) -> int:
    '''
    比较三种路径之间谁最大
    f(i-1,j-1),
    f(i-1,j)+indel,
    f(i,j-1)+indel
    '''
    temp = 0
    if a > b:
        temp = a 
    else:
        temp = b
    if temp > c:
        return temp
    else:
        return c

def myCompare(a:str, b:str) -> int:
    '''
    比较两个字符类型属于什么，match，dismatch，indel
    '''
    if a == b:
        return MATCH
    elif  a == ' ' or  b == ' ':
        return INDEL
    else:
        return DIS_MATCH
    

def traceback(item:object, i:int, j:int, str1:str, str2:str, res1:str, res2:str, n:int, resUnit:object):
    temp = item[i][j] # BacktrackingUnit class object
    if resUnit.tag != 1:
        if not (i or j): #到矩阵单元(0, 0)才算结束，这代表初始的两个字符串的每个字符都被比对到了
            resUnit.str1 = str1
            resUnit.str2 = str2
            resUnit.res1 = res1
            resUnit.res2 = res2
            resUnit.tag = 1
            return resUnit
        if temp.goUp: # 向上回溯一格
            res1 = str1[i - 1] + res1
            res2 = INDEL_CHAR + res2  # "-" + res2
            resUnit = traceback(item, i - 1, j, str1, str2, res1, res2, n + 1, resUnit)
        
        if temp.goLeftUp: #向左上回溯一格 
            res1 = str1[i - 1] + res1
            res2 = str2[j - 1] + res2
            resUnit = traceback(item, i - 1, j - 1, str1, str2, res1, res2, n + 1, resUnit)
        
        if temp.goLeft: # 向左回溯一格
            res1 = INDEL_CHAR + res1
            res2 = str2[j - 1] + res2
            resUnit = traceback(item, i, j - 1, str1, str2, res1, res2, n + 1, resUnit)
        return resUnit
    else:
        return resUnit



def RegularSeq1(tag:object, queue_finish:list,item:int) -> list:
    '''
        规整函数，规整序列1情况

        queue_finish      tag
        A1                  A2
        B                  E
        C
        D
    '''
    main_seq = queue_finish[item] # 找到和seq1相同的序列 #SingleSeq class object
    A1 = main_seq.res
    A2 = tag.res1
    E = tag.res2
    tempStr = ""
    i,j = 0,0
    while A1 != A2 and i < len(A1) and j < len(A2):
        if A1[i] == A2[j]:
            i += 1
            j += 1
        else:
            if A1[i] == '-':
                # A2.insert(j, "-");
                # E.insert(j, "-");
                A2 = A2[0:j]+"-"+A2[j:]
                E = E[0:j]+"-"+E[j:]
            elif A2[j] == '-':
                # 遍历queue_finish,给queue_finish内res洗头
                A1 = A1[0:i]+"-"+A1[i:]
                for it in queue_finish:
                    it.res = it.res[0:i]+"-"+it.res[i:]
    #
    if i == len(A1):
        # A1先到头
        for k in range(len(A2)-j):
            tempStr += "-"
        A1 += tempStr
        for it in queue_finish:
            it.res = it.res + tempStr
    elif j == len(A2):
        # A2先到头
        for k in range(len(A1)-i):
            tempStr += "-"
        A2 += tempStr
        E += tempStr
    
    # 添加
    sE = SingleSeq()
    sE.res = E
    sE.str = tag.str2
    queue_finish.append(sE)
    return queue_finish


def RegularSeq2(tag:object, queue_finish:list,item:int) -> list:
    '''
        规整函数，规整序列2情况

        queue_finish      tag
        A1                  E
        B                  A2
        C
        D
    '''
    main_seq = queue_finish[item] # 找到和seq1相同的序列 #SingleSeq class object
    A1 = main_seq.res
    A2 = tag.res2 #与 RegularSeq1 差异
    E = tag.res1  #与 RegularSeq1 差异
    tempStr = ""
    i,j = 0,0
    while A1 != A2 and i < len(A1) and j < len(A2):
        if A1[i] == A2[j]:
            i += 1
            j += 1
        else:
            if A1[i] == '-':
                # A2.insert(j, "-");
                # E.insert(j, "-");
                A2 = A2[0:j]+"-"+A2[j:] 
                E = E[0:j]+"-"+E[j:] 
            elif A2[j] == '-':
                # 遍历queue_finish,给queue_finish内res洗头
                A1 = A1[0:i]+"-"+A1[i:]
                for it in queue_finish:
                    it.res = it.res[0:i]+"-"+it.res[i:]
    #
    #print(A1,A2,E)
    if i == len(A1):
        #print("A1")
        # A1先到头
        for k in range(len(A2)-j):
            tempStr += "-"
        A1 += tempStr
        for it in queue_finish:
            it.res = it.res + tempStr
    elif j == len(A2):
        #print("A2")
        # A2先到头
        for k in range(len(A1)-i):
            tempStr += "-"
        A2 += tempStr
        E += tempStr
    
    # 添加
    sE = SingleSeq()
    sE.res = E
    #print("E",E)
    sE.str = tag.str1 # 与 RegularSeq1 差异
    queue_finish.append(sE)
    return queue_finish

def complare_customer(a:object,b:object) -> bool:

    if a.score < b.score:
        return 1
    else:
        return -1
    
# 这个函数不用，没改，弃用
def complare(a:object,b:object) -> bool:
    '''
    https://blog.csdn.net/baidu_32523857/article/details/109365115
    可以这样理解，sort第三个参数默认升序，
    这个地方是个bool函数。
    如果返回值结果为假，那么函数会互换他们的位置
    如果返回结果为真，就保持原来的位置不变 。
    如果x<y成立，那么就保持不变，否则就交换位置。 

    # https://blog.csdn.net/feifei99_8820/article/details/138781996
    # a>b为降序;a<b为升序。
    C++ 降序排序
    return a.score > b.score
    C++ 升序排序
    return b.score > a.score
    '''
    return a.score > b.score

def NeedlemanWunch(str1:str, str2:str) -> object:
    # 字符串str1,str2长度
    m = len(str1)
    n = len(str2)
    m1, m2, m3, mm = int(),int(),int(),int()

    unit = list() # 存储 BacktrackingUnit object
    for i in range(m+1):
        unit.append(list())
        #unit[i] = {}
        for j in range(n+1):
            unit[i].append(BacktrackingUnit())
            #unit[i][j] = BacktrackingUnit()
            unit[i][j].goUp = 0
            unit[i][j].goLeftUp = 0
            unit[i][j].goLeft = 0
    unit[0][0].score = 0

    for i in range(1,m+1):
        unit[i][0].score = INDEL * i
        unit[i][0].goUp = 1

    for j in range(1,n+1):
        unit[0][j].score = INDEL * j
        unit[0][j].goLeft = 1
    

    #动态规划算法计算得分矩阵每个单元的分值
    for i in range(1,m+1):
        for j in range(1,n+1):
            m1 = unit[i - 1][j].score + INDEL
            m2 = unit[i - 1][j - 1].score + myCompare(str1[i - 1], str2[j - 1])
            m3 = unit[i][j - 1].score + INDEL
            mm = max3(m1, m2, m3)
            unit[i][j].score = mm
            # 断路径来源
            if m1 == mm :
                unit[i][j].goUp = 1
            if m2 == mm :
                unit[i][j].goLeftUp = 1
            if m3 == mm :
                unit[i][j].goLeft = 1
    #开始回溯
    res = ResUnit()
    res.tag = 0
    res = traceback(unit, m, n, str1, str2, "", "", 0, res)
    res.score = unit[m][n].score
    # 释放内存,python 内存管理是自动的,会回收
    # del unit 
    return res


def  getResUnitMatrix(s:list,length:int,res:object):
    '''
        循环比较一组序列的值，返回一个ResUnit对象数组，二维，且是个倒三角形状
        其中，s是一个字符串类型的数组，存储等待序列比对的一组数据
    '''
    sLength = length
    print("sLength:",sLength)
    if sLength == 1:
        print("不符合输入规范")
    for i in range(sLength):
        for j in range(i + 1,sLength):
            # 只遍历上三角区域
            # print(i,j)
            # print(s[i],s[j])
            res[i][j] = NeedlemanWunch(s[i], s[j])
            #print(res[i][j].str1)

def RegularTwo(tag:object,temp:object,queue_finish:list) ->list:
    '''
        规整函数，规整两个序列情况

        queue_finish      temp      tag
        A1                 A2        E1
        B                  E2        F
        C
        D
    '''
    E2 = temp.res2
    E1 = tag.res1
    A1 = queue_finish[0].res
    A2 = temp.res1
    F = tag.res2
    tempStr = ""
    i = 0
    j = 0
    # 第一步,整合tag与temp
    while E2 != E1 and j < len(E1) and i < len(E2):
        if E2[i] == E1[j]:
            i += 1
            j += 1
        else:
            if E2[i] == '-':
                # https://blog.csdn.net/weixin_47830774/article/details/134957395
                # E1.insert(j, "-");
                # F.insert(j, "-");
                E1 = E1[0:j]+"-"+E1[j:]
                F = F[0:j]+"-"+F[j:]
            elif E1[j] == '-':
                # E2.insert(i, "-");
                # A2.insert(i, "-");
                E2 = E2[0:i]+"-"+E2[i:]
                A2 = A2[0:i]+"-"+A2[i:]
    if i == len(E2):
        # E2先到头
        #for (int k = 0; k < E1.length() - j; k++)
        for k in range(len(E1) - j):
            tempStr += "-"
        E2 += tempStr
        A2 += tempStr
        #print(tempStr)
    elif j == len(E1):
        # E1先到头
        for k in range(len(E2) - i):
            tempStr += "-"
        E1 += tempStr
        F += tempStr
    
    # 将tempStr置空
    tempStr = ""

    # 第二步 融合进queue_finish
    i = 0
    j = 0
    while A1 != A2 and i < len(A1) and j < len(A2):
        if A1[i] == A2[j]:
            i +=1
            j +=1
        else:
            if A1[i] == '-':
                A2 = A2[0:j]+"-"+A2[j:]
                E1 = E1[0:j]+"-"+E1[j:]
                F = F[0:j]+"-"+F[j:]
            elif A2[j] == '-':
                A1 = A1[0:i]+"-"+A1[i:]
                for it in queue_finish:
                    it.res = it.res[0:i]+"-"+it.res[i:]
    #
    if i == len(A1):
        # A1先到头 #A1 长度短，后面补充 "-"
        for k in range(len(A2) -j):
            tempStr += "-"
        A1 += tempStr
        for it in queue_finish:
            it.res = it.res + tempStr
    elif j == len(A2):
        # A2先到头
        for k in range(len(A1) -i):
            tempStr += "-"
        A2 += tempStr
        E1 += tempStr
        F += tempStr
    # 规划好之后，，将 E F 插入queue_finish尾部

    sE, sF = SingleSeq(),SingleSeq()
    sE.res = E1
    sE.str = tag.str1
    sF.res = F
    sF.str = tag.str2
    queue_finish.append(sE)
    queue_finish.append(sF)
    return queue_finish



# def ifStrInQueueFinish(str:str, queue_finish:list)->int:
#     for i,it in enumerate(queue_finish):
#         if str == it.str:
#             return i
#     return -1
def ifStrInQueueFinish(str:str, queue_finish:list)->int:
    i = 0
    for it in queue_finish:
        if str == it.str:
            return i
        i += 1
    return -1


def main():

    # clock_t startTime, endTime;
    # startTime = clock();//计时开始
    
    # clust算法
    sequence_groups = 7  #  序列条数
    ss = [
        "ACCTTGGGAAAATTCCGGGACA",
        "AACGGAAAATTCCGGGACCTT",
        "AATTCCGGAATTCCGGGACA",
        "AATTCGGAAAATTCCGGGACA",
        "AATTCCGGAAAATTCCGACA",
        "AACCCGGAAAATTCCGGGACA",
        "AATTCCGGAAAACTCGGGACA"
        # "AATGGAAAATTCCGCGGCA",
        # "AATGTCCGGAAAATTCCGGGACA",
        # "ATGCGGAAAATTCCCAAGGGACA",
        # "AATCGGAAATTATTCCGGGACA",
        # "CCTCCCGGATTCCGGGAGCA",
        # "AACTGCGGAAAATTCCGGGACA",
        # "AATTCCGGAAAATTCCGGATCCA",
        # "AATATCCGAAAATTCCGGGACA",
        # "AATTCCGGAAAATCCATCCACA",
        # "AATCGGAAAATTCGGGACA",
        # "AACCGGAAAATTCCCCTGGGACA",
        # "ATTTCCGGAAATTCCGGGACA",
        # "AATTCCGGAAATTCCGGCCACA",
        # "AAGGCGGAAAATTCGCCGGACA",
        # "AATGGCGAAAATTCCGGGACA",
        # "AATCCGGAAAATTCCTCCACA",
        # "AATTTCGGGAAAATTCCGGGACA",
        # "AATTCCGGAAAATTCCGGGCTACA",
        # "AACCTCGGAAAATTCCGGGACA",
        # "AATTAACCGGAAAATGGGGACA",
        # "ACCATCCGGAAAATTCCGGGACA",
        # "AATTCCGGAAAATTCATGCGGACA",
        # "AATTCCCATGAAAATTCCGGGACA",
        # "AACCTAGGAAAATTCCGGGACA"
    ]

    queue_initial = []  #存储ResUnit对象 # 定义等待整合的队列，是一个ResUnit对象vector
    queue_finish = []   #存储 String # 定义整合完毕的队列，是一个String类型的vector

    #res = dict()
    res = list()

    for i in range(sequence_groups):
        res.append(list())
        #print(res)
        for j in range(sequence_groups):
            #res[i][j] = str(i)+'_'+str(j)
            #res[i].append(str(i)+'_'+str(j))
            res[i].append(ResUnit())
    #print(len(res))
    #exit()
    #print(ss[5])
    #
    getResUnitMatrix(ss, sequence_groups, res)

    #开始多序列比对
    #定义队列长度
    queue_length = int(((sequence_groups - 1)*sequence_groups) / 2)
    print("queue_length:",queue_length)

    # 将res内元素放入等待整合队列--按分数从高到低排列
    for i in range(sequence_groups):
        for j in range(i + 1,sequence_groups):
            # 放入容器
            queue_initial.append(res[i][j])

    # for it in queue_initial:
    #     print("it->res2:",it.res2)
    #     print("it->res1:",it.res1)
    #     print("it->score:",it.score)

    # 排序(直接修改原始列表),调用complare 函数自定义排序
    # 降序排序,lambda 获取类属性用来排序
    #queue_initial.sort(key=lambda x:x.score, reverse=True)
    queue_initial.sort(key=cmp_to_key(complare_customer))

    # for it in queue_initial:
    #     print("it->res2:",it.res2)
    #     print("it->res1:",it.res1)
    #     print("it->score:",it.score)
    
    # 最多循环queue_length次
    for i in range(queue_length):
        # 当结果队列长度与sequence_groups相等之后,就说明全部放入了结果队列,可以跳出循环了
        if sequence_groups == len(queue_finish):
            break
        #print(ifStrInQueueFinish(queue_initial[i].str1, queue_finish))
        # 一个ResUnit对象的str1属性和str2均不在
        if ifStrInQueueFinish(queue_initial[i].str1, queue_finish) < 0 and \
            ifStrInQueueFinish(queue_initial[i].str2, queue_finish) < 0:
            singleSeq1 = SingleSeq()
            singleSeq2 = SingleSeq()
            singleSeq1.str = queue_initial[i].str1
            singleSeq1.res = queue_initial[i].res1
            singleSeq2.str = queue_initial[i].str2
            singleSeq2.res = queue_initial[i].res2
            # 如果结果队列已经有元素,且又来了俩不相干的,却很匹配的序列对
            if len(queue_finish)>0:
                #将结果队列第一个的序列和queue_initial.at(i).str1进行双序列比对
                #print(i)
                #print(queue_finish[0].str,queue_initial[i].str1)
                temp = NeedlemanWunch(queue_finish[0].str, queue_initial[i].str1) # ResUnit class object
                #进行规整操作
                queue_finish = RegularTwo(queue_initial[i], temp, queue_finish)
            else:
                queue_finish.append(singleSeq1)
                queue_finish.append(singleSeq2)
        #
        # str1在,str2不在
        elif ifStrInQueueFinish(queue_initial[i].str1, queue_finish) > -1 and \
            ifStrInQueueFinish(queue_initial[i].str2, queue_finish) < 0 :
            item = ifStrInQueueFinish(queue_initial[i].str1, queue_finish)
            queue_finish = RegularSeq1(queue_initial[i], queue_finish, item)
        # str2在,str1不在
        elif ifStrInQueueFinish(queue_initial[i].str2, queue_finish) > -1 and \
            ifStrInQueueFinish(queue_initial[i].str1, queue_finish) < 0:
            item = ifStrInQueueFinish(queue_initial[i].str2, queue_finish)
            #print(queue_initial[i].res1,i)
            queue_finish = RegularSeq2(queue_initial[i], queue_finish, item)
    #
    # 声明一个迭代器，来访问vector容器
    print("--------------------------------------------------------------------")
    print("\n原序列\n")
    for it_finish in queue_finish:
        print("  "+it_finish.str)
    print("\n\n比对后\n")
    for it_finish in queue_finish:
        print("  "+it_finish.res)
    # endTime = clock();//计时结束
    # cout << endl << endl << "The run time is: " << (double)(endTime - startTime) / CLOCKS_PER_SEC << "s" << endl;
    print("--------------------------------------------------------------------")
    # system("pause");
    return 0

if __name__ == "__main__":
    main()

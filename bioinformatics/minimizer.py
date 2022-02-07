#https://homolog.us/blogs/bioinfo/2017/10/25/intro-minimizer/

from collections import deque
#seq="ACGCCGATC"
seq="ATGCGATATCGTAGGCGTCGATGGAGAGCTAGATCGATCGATCTAAATCCCGATCGATTCCGAGCGCGATCAAAGCGCGATAGGCTAGCTAAAGCTAGCA"
# rev=seq[::-1]

# rev=rev.replace("A","X")
# rev=rev.replace("T","A")
# rev=rev.replace("X","T")
# rev=rev.replace("C","X")
# rev=rev.replace("G","C")
# rev=rev.replace("X","G")

# Kmer=4
# M=2
# L=len(seq)

# for i in range(0, L-Kmer+1):

#         sub_f=seq[i:i+Kmer]
#         sub_r=rev[L-Kmer-i:L-i]

#         min="ZZZZZZZZZZZZZ"
#         for j in range(0, Kmer-M+1):
#                 sub2=sub_f[j:j+M]
#                 if sub2 < min:
#                         min=sub2
#                 sub2=sub_r[j:j+M]
#                 if sub2 < min:
#                         min=sub2

#         print(sub_f,min)



#
def get_kmer_minimizers(seq, k_size, w_size):
    '''
    window_kmers  弹栈 压栈新的kmer
    minimizers  # 存储 minimizer 中 ascii最小的kmer 与坐标 [[kmer,pos],[..]]
    '''
    # kmers = [seq[i:i+k_size] for i in range(len(seq)-k_size) ]
    #窗口减去第一个kmer大小,因为后面取序列时，要在向后取 k_size 大小的序列 seq[i:i+k_size]
    w = w_size - k_size
    # 序列前面0-w 长度序列里取k_size 大小的 minimizer
    #窗口(原先意义上的kmer)范围内，所有碱基 取k_size大小的minimizers
    window_kmers = deque([seq[i:i+k_size] for i in range(w +1)])
    # 固定长度的 kmer 取值 list [k1,k2,k3,k4,k5]
    curr_min = min(window_kmers) #根据ascii 排序取最小的作为 minimizer
    minimizers = [ (curr_min, list(window_kmers).index(curr_min)) ] # [(当前集合，序列中的坐标)]

    # 第二部分从 w+1 到 seq全场 取minimizers
    for i in range(w+1,len(seq) - k_size):
        new_kmer = seq[i:i+k_size] # 累计kmer，一个一个碱基挪动kmer
        # updateing window # 左侧弹栈，丢弃数值
        discarded_kmer = window_kmers.popleft()
        window_kmers.append(new_kmer) # 右侧压栈,补充list
        #pop <-||||||<- push

        # we have discarded previous windows minimizer, look for new minimizer brute force
        # kmer 移动后最小 minimizer 没有变化
        if curr_min == discarded_kmer: 
            curr_min = min(window_kmers)
            minimizers.append( (curr_min, list(window_kmers).index(curr_min) + i - w ) ) #[(当前最小kmer，完整序列中的坐标，index()导致永远是第一个出现的)]

        # Previous minimizer still in window, we only need to compare with the recently added kmer 
        elif new_kmer < curr_min:
            curr_min = new_kmer
            minimizers.append( (curr_min, i) )

    return minimizers

k_size=7
w_size=31
print(seq)
result = get_kmer_minimizers(seq, k_size, w_size)
print(result)

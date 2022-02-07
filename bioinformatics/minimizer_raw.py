#https://homolog.us/blogs/bioinfo/2017/10/25/intro-minimizer/


seq="ATGCGATATCGTAGGCGTCGATGGAGAGCTAGATCGATCGATCTAAATCCCGATCGATTCCGAGCGCGATCAAAGCGCGATAGGCTAGCTAAAGCTAGCA"
rev=seq[::-1]

rev=rev.replace("A","X")
rev=rev.replace("T","A")
rev=rev.replace("X","T")
rev=rev.replace("C","X")
rev=rev.replace("G","C")
rev=rev.replace("X","G")

Kmer=31 # 正常意义上的kmer
M=7 #  ascii(American Standard Code for Information Interchange)最小的子kmer(minimizer) 长度
L=len(seq)

for i in range(0, L-Kmer+1):

        sub_f=seq[i:i+Kmer]
        sub_r=rev[L-Kmer-i:L-i]# 反向

        min="ZZZZZZZZZZZZZ"  # minimizer
        for j in range(0, Kmer-M+1):
                sub2=sub_f[j:j+M] # 正向
                if sub2 < min:
                        min=sub2
                
                sub2=sub_r[j:j+M] # 反向
                if sub2 < min:
                        min=sub2

        print(sub_f,min) #正反最小的kmer minimizer

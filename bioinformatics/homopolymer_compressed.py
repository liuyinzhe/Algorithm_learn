import itertools

#https://www.liaoxuefeng.com/wiki/1016959663602400/1017783145987360
#ch, g in itertools.groupby(seq)
#A ['A', 'A', 'A']

seq="ATGCGATATCGTAGGCGTCGATGGAGAGCTAGATCGATCGATCTAAATCCCGATCGATTCCGAGCGCGATCAAAGCGCGATAGGCTAGCTAAAGCTAGCA"
print(seq)
seq_hpol_comp = ''.join(ch for ch, _ in itertools.groupby(seq))
print(seq_hpol_comp)
#all_read_hpol_lengths = [len([c for c in g]) for ch, g in itertools.groupby(seq)]
#print(all_read_hpol_lengths)

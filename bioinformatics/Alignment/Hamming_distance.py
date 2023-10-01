
def hamming_distance(string1, string2):
	dist_counter = 0
	for idx in range(len(string1)):
		if string1[idx] != string2[idx]:
			dist_counter += 1
	return dist_counter

def hamming_distance_zip(string1, string2):
    dist_counter = sum(xi != yi for xi, yi in zip(string1, string2))
    return dist_counter

# pip install Levenshtein
# import Levenshtein

# # 汉明距离 # 长度一致
# hamming_distance(string1, string2)

# # 编辑距离 # 长度不一致
# Levenshtein.distance(string1, string2)

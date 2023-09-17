from sklearn import datasets
from sklearn.manifold import TSNE 
from matplotlib import pyplot as plt


def main():
    '''
    算法 降维最多3个维度，一般选择降低到2，n_components=2
    :return:
    '''
    digits = datasets.load_digits()
    X = digits.data[:500]
    y = digits.target[:500]
    print(X.shape) # [500,64] # 共500行64列
    tsne = TSNE(n_components=2, random_state=0)
    X_2d = tsne.fit_transform(X)
    
    print(type(X_2d)) # <class 'numpy.ndarray'>
    print(X_2d.shape) # 共500行2列 相当于500个样品的64个维度将为到2个维度

    print(tsne.kl_divergence_)
    # 0.39606231451034546
    # T-SNE的KL散度
    print(tsne.n_features_in_)
    # 64
    # 输入的特征个数
    print(tsne.n_iter_)
    # 999 迭代次数
    
    target_ids = range(len(digits.target_names))
    print(digits.target_names) # [1,2,3,4,5,6,7,8,9]


    plt.figure(figsize=(6, 5))
    colors = 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'w', 'orange', 'purple'

    for i, c, label in zip(target_ids, colors, digits.target_names):
        plt.scatter(X_2d[y == i, 0], X_2d[y == i, 1], c=c, label=label)

    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()

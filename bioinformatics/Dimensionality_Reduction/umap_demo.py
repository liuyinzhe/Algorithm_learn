from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import umap
import numpy as np
'''
pip install umap-learn
'''
def main():
    digits = load_digits()
    # fig, ax_array = plt.subplots(20, 20)
    # axes = ax_array.flatten()
    # for i, ax in enumerate(axes):
    #     ax.imshow(digits.images[i], cmap='gray_r')
    # plt.setp(axes, xticks=[], yticks=[], frame_on=False)
    # plt.tight_layout(h_pad=0.5, w_pad=0.01)
    # plt.show()

    reducer = umap.UMAP() #n_components=2
    '''
    n_neighbors=100, #default 15, The size of local neighborhood (in terms of number of neighboring sample points) used for manifold approximation.
    n_components=3, # 默认是2 降低到2维度 ## default 2, The dimension of the space to embed into.
    metric='euclidean', # default 'euclidean', The metric to use to compute distances in high dimensional space.
    n_epochs=1000, # default None, The number of training epochs to be used in optimizing the low dimensional embedding. Larger values result in more accurate embeddings.
    min_dist=0.1, # default 0.1, The effective minimum distance between embedded points.
    learning_rate=1.0, # default 1.0, The initial learning rate for the embedding optimization.
    local_connectivity=2,
    init='spectral', # default 'spectral', How to initialize the low dimensional embedding. Options are: {'spectral', 'random', A numpy array of initial embedding positions}.
    transform_seed=42, # default 42, Random seed used for the stochastic aspects of the transform operation.
    spread=1.0, # default 1.0, The effective scale of embedded points. In combination with ``min_dist`` this determines how clustered/clumped the embedded points are.
    low_memory=False, # default False, For some datasets the nearest neighbor computation can consume a lot of memory. If you find that UMAP is failing due to memory constraints consider setting this option to True.
    '''
    embedding = reducer.fit_transform(digits.data)
    print(embedding.shape)

    plt.scatter(embedding[:, 0], embedding[:, 1], c=digits.target, cmap='Spectral', s=5)
    plt.gca().set_aspect('equal', 'datalim')
    plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
    plt.title('UMAP projection of the Digits dataset')
    plt.show()

if __name__ == '__main__':
    main()

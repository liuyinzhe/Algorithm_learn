import umap
#from umap import UMAP

# Skleran
from sklearn.datasets import load_digits # for MNIST data
from sklearn.model_selection import train_test_split # for splitting data into train and test

# Visualization
import plotly.express as px # for data visualization
import matplotlib.pyplot as plt 

# Data manipulation
import pandas as pd
import numpy as np
'''
pip install umap-learn
pip install plotly
'''

def chart(X, y):
    #--------------------------------------------------------------------------#
    # This section is not mandatory as its purpose is to sort the data by label
    # so, we can maintain consistent colors for digits across multiple graphs

    # Concatenate X and y arrays
    arr_concat=np.concatenate((X, y.reshape(y.shape[0],1)), axis=1)
    # Create a Pandas dataframe using the above array
    df=pd.DataFrame(arr_concat, columns=['x', 'y', 'z', 'label'])
    # Convert label data type from float to integer
    df['label'] = df['label'].astype(int)
    # Finally, sort the dataframe by label
    df.sort_values(by='label', axis=0, ascending=True, inplace=True)
    #--------------------------------------------------------------------------#

    # Create a 3D graph
    fig = px.scatter_3d(df, x='x', y='y', z='z', color=df['label'].astype(str), height=900, width=950)

    # Update chart looks
    fig.update_layout(title_text='UMAP',
    showlegend=True,
    legend=dict(orientation="h", yanchor="top", y=0, xanchor="center", x=0.5),
    scene_camera=dict(up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=-0.1),
    eye=dict(x=1.5, y=-1.4, z=0.5)),
    margin=dict(l=0, r=0, b=0, t=0),
    scene = dict(xaxis=dict(backgroundcolor='white',
    color='black',
    gridcolor='#f0f0f0',
    title_font=dict(size=10),
    tickfont=dict(size=10),
    ),
    yaxis=dict(backgroundcolor='white',
    color='black',
    gridcolor='#f0f0f0',
    title_font=dict(size=10),
    tickfont=dict(size=10),
    ),
    zaxis=dict(backgroundcolor='lightgrey',
    color='black',
    gridcolor='#f0f0f0',
    title_font=dict(size=10),
    tickfont=dict(size=10),
    )))
    # Update marker size
    fig.update_traces(marker=dict(size=3, line=dict(color='black', width=0.1)))

    fig.show()

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

    # Load arrays containing digit data (64 pixels per image) and their true labels
    X, y = load_digits(return_X_y=True)
    # Some stats
    print('Shape of digit images: ', digits.images.shape)
    print('Shape of X (main data): ', X.shape)
    print('Shape of y (true labels): ', y.shape)
    
    reducer = umap.UMAP(n_components=3) #
    # Fit and transform the data
    X_trans = reducer.fit_transform(X)

    # Check the shape of the new data
    print('Shape of X_trans: ', X_trans.shape)
    #UMAP应用于我们的MNIST数据，并打印转换后的数组的形状，以确认已经成功地将维数从64降至3
    chart(X_trans, y)
    # 可以看到1 2 有一点点混在一起啊

    #监督的UMAP

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)

    # Configure UMAP hyperparameters
    reducer2 = umap.UMAP(n_neighbors=100, n_components=3, n_epochs=1000,
    min_dist=0.5, local_connectivity=2, random_state=42,
    )

    # Training on MNIST digits data - this time we also pass the true labels to a fit_transform method
    X_train_res = reducer2.fit_transform(X_train, y_train)

    # Apply on a test set
    X_test_res = reducer2.transform(X_test)

    # Print the shape of new arrays
    print('Shape of X_train_res: ', X_train_res.shape)
    print('Shape of X_test_res: ', X_test_res.shape)

    # 训练集(真集) 原本区分情况
    chart(X_train_res, y_train)
    # 测试集(预测集)训练效果
    chart(X_test_res, y_test)

if __name__ == '__main__':
    main()

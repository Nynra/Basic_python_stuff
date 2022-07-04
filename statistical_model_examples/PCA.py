# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:20:56 2022
source: https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
@author: baskl
"""
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler


def get_PCs(df, features, target='Naam', var_thresh=None, components=None):
    """
    Calculate the principle components from the given dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataFrame containing all the features and the target.
    features : list
        List containing the features that will be used in the PCA calculation.
    target : string
        The name of the target column (name of the sample).
    var_thresh : float, optional
        Floating point number between 0-1 representing the minimal amound of
        variance that has to be explained by a principle component to be
        concidered a valid component. The default is None.
    components : int, optional
        Integer representing the maximum amound of components that can be
        returned. The maximum components is Nfeatures - 1. The default is None.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the principle component and feature values.

    """
    """Return the Principle components of the dataframe."""
    if var_thresh is None and components is None:
        return 'Ether give a minimum variance or number of components.'
    if var_thresh is not None:
        components = len(features) - 1  # Maximum number of components
    if components is not None:
        var_thresh = None

    # Separating out the features and scale the data
    x = df.loc[:, features].values  # Separating out the target
    # y = df.loc[:, [target]].values  # Standardizing the features
    x = StandardScaler().fit_transform(x)

    # Calculate the principle components
    pca = PCA(n_components=components)
    principalComponents = pca.fit_transform(x)

    ratio = pca.explained_variance_ratio_
    cutoff = None
    if var_thresh is not None:
        for c, i in enumerate(ratio):
            if i < var_thresh:
                cutoff = c
                break

    principalDf = pd.DataFrame(data=principalComponents,
                               columns=[str(i) for i in range(components)])
    if cutoff is not None:
        principalDf = principalDf[:cutoff + 1]

    return principalDf


if __name__ == '__main__':
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

    # load dataset into Pandas DataFrame
    df3 = pd.read_csv(url,
                      names=['sepal length', 'sepal width', 'petal length',
                             'petal width', 'target'])
    df = pd.read_excel('kast_data.xlsx')
    df = df.dropna().reset_index(drop=True)
    samples = df[['Naam', 'State']]
    df = df.drop('State', axis=1)

    features = list(df.columns)[1:-1]
    for i in features:
        df[i] /= df['Verpakking (g)']

    components = get_PCs(df=df, features=features, components=3)
    ##############
    # Plot the data
    ##############
    plt.scatter(components['0'], components['1'])
    plt.grid(True)
    # =============================================================================
    # fig = plt.figure(figsize=(4, 4))
    #
    # ax = fig.add_subplot(111, projection='3d')
    #
    # # plot the point (2,3,4) on the figure
    # ax.scatter(principalDf['pc1'], principalDf['pc2'], principalDf['pc3'])
    #
    # =============================================================================
    plt.show()
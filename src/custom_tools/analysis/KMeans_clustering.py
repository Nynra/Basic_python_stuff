# -*- coding: utf-8 -*-
# Load the dataset
# ----------------
# We will start by loading the `digits` dataset. This dataset contains
# handwritten digits from 0 to 9. In the context of clustering, one would like
# to group images such that the handwritten digits on the image are the same.
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import pandas as pd


def get_metrics(name, k_means_model, test_data, labels=None):
    """Get some metrics on the current cluster model."""
    # Define the metrics which require only the true labels and estimator
    # labels
# =============================================================================
#     clustering_metrics = [
#         metrics.homogeneity_score,
#         metrics.completeness_score,
#         metrics.v_measure_score,
#         metrics.adjusted_rand_score,
#         metrics.adjusted_mutual_info_score,
#     ]
#     results = [m(labels, kmeans.labels_) for m in clustering_metrics]
# =============================================================================

    # The silhouette score requires the full dataset
    results = [
        metrics.silhouette_score(
            data,
            kmeans.labels_,
            metric="euclidean",
            sample_size=300,
        )
    ]

    # Collect the results in a dict
# =============================================================================
#     formatted_results = {'init': name,
#                          'homo': round(results[0], 3),
#                          'compl': round(results[1], 3),
#                          'v-meas': round(results[2], 3),
#                          'ARI': round(results[3], 3),
#                          'AMI': round(results[4], 3),
#                          'silhouette': round(results[5], 3)}
# =============================================================================
    # Collect the results in a dict
    formatted_results = {'init': name,
                         'silhouette': round(results[0], 3)}
    for key in formatted_results:
        print('{}: {}'.format(key, formatted_results[key]))
    return formatted_results


if __name__ == '__main__':
    # load dataset into Pandas DataFrame
    df = pd.read_excel('kast_data.xlsx')
    df = df.dropna().reset_index(drop=True)
    samples = df[['Naam', 'State']]
    df = df.drop(['State', 'Naam'], axis=1)

    features = list(df.columns)[1:-1]
    for i in features:
        df[i] /= df['Verpakking (g)']
        
    data = df.to_numpy()

    # Create the clusters
    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init="k-means++", n_clusters=3, n_init=4)
    kmeans.fit(reduced_data)

    get_metrics('PCA', kmeans, reduced_data)

    ###################
    # Plot the data
    ###################
    # Step size of the mesh. Decrease to increase the quality of the VQ.
    # Picel distance
    h = 0.02  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    # Predict the colour of each pixcel (result is called the label)
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation="nearest", extent=(xx.min(), xx.max(), yy.min(),
                                                   yy.max()), cmap=plt.cm.Pastel2,
               aspect="auto", origin="lower",)
# =============================================================================
#     plt.scatter(reduced_data[:, 0], reduced_data[:, 1],
#                 s=2, c=kmeans.labels_, alpha=1, cmap=plt.cm.tab20)
# =============================================================================
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1],
                    s=2, c='black', alpha=1)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], s=30, linewidths=3, zorder=10,
                color='w')


    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()
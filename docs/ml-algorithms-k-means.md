# K-Means

K-Means is an unsupervised learning algorithm used for clustering tasks. It partitions data points into K distinct clusters based on their features, aiming to minimize the variance within each cluster.

## Hyperparameters

- K: The number of clusters to form. Choosing the right value for K is crucial as it directly affects the clustering results.
  - Elbow Method: A technique to determine the optimal K by plotting the explained variance as a function of K and looking for an "elbow" point where the rate of decrease sharply changes.
- mini_batch_size: The number of samples to use in each mini-batch when updating the cluster centroids. A smaller batch size can lead to faster convergence but may introduce more noise.
- extra_center_factor: A factor that determines the number of extra centroids to initialize. This can help improve the quality of the final clusters by providing more initial options for centroid placement.
- init_method: The method used to initialize the cluster centroids. Common methods include 'k-means++' (which spreads out the initial centroids) and 'random' (which selects random points from the dataset).

# KNN

K-Nearest Neighbors (KNN) is a simple, instance-based learning algorithm used for classification and regression tasks. It operates on the principle that similar instances are likely to have similar outcomes.

- Both classification and regression tasks.
- **Classification**:
  - Find the K closest points to a sample point and return the most frequent label
- **Regression**:
  - Find the K closest points to a sample point and return the average of their values

## Hyperparameters

- K: The number of nearest neighbors to consider when making predictions. A larger K value can smooth out noise but may also overlook local patterns.
- sample_size: The number of samples to use from the training data when making predictions. A larger sample size can improve accuracy but may increase computation time.

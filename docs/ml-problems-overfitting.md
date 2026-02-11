# Overfitting

## Prevention techniques

Is possible to prevent overfitting by diversify and scale the training data or using some other data science techniques.

### Early Stopping

Early stopping is a regularization technique that halts training when validation performance no longer improves according to a monitored metric. The metric is typically a loss or error measure such as cross-entropy, MSE, RMSE, or MAE, depending on the task. Training stops after a fixed number of consecutive epochs without improvement (patience), optionally restoring the best-performing weights, preventing overfitting by avoiding optimization beyond the generalization optimum.

- Most commonly used in _Neural Networks_.

### Pruning

**Feature selection** technique that removes less important features from the dataset, which can help reduce overfitting by simplifying the model and reducing the risk of capturing noise in the data.

### Regularization

Regularization is a set of training techniques that reduce overfitting by penalizing large weights, which can effectively reduce the influence of less important features.

Less important features don’t naturally have large weights—they only get them when the model overfits, and regularization exists to prevent exactly that.

#### L1 Regularization (Lasso)

L1 is the sum of weights

- Remove less important features performing feature selection, by driving some weights to zero.
- Computationally inefficient
- Sparse output

#### l2 Regularization (Ridge)

L2 is the sum of squared weights

- All features remain considered, just weighted
- Computationally efficient
- Dense output

### Ensemble Methods

Ensembling combines predictions from several separate machine learning algorithms. Some models are called weak learners because they perform only slightly better than random guessing. Ensemble methods combine all the weak learners to get more accurate results.

There are two main types of ensemble methods, bagging and boosting.

#### Bagging

Bagging, or bootstrap aggregating, trains multiple models on different subsets of the training data and then averages their predictions. This can help reduce overfitting by reducing the variance of the model.

#### Boosting

Boosting trains multiple models sequentially, where each model tries to correct the errors of the previous one. This can help reduce overfitting by focusing on the most difficult cases and improving the overall performance of the model.

### Dropout

Dropout layers randomly set a fraction of input units(neurons) to 0 at each update during training time, which helps prevent overfitting by introducing noise into the training process. This encourages the model to learn more generalized patterns.

- Most commonly used in _Neural Networks_.

## Data Augmentation

Data augmentation is a technique that artificially increases the size of the training dataset by creating modified versions of the existing data. This can help reduce overfitting by providing more diverse examples for the model to learn from.

Examples of data augmentation include:

- For image data: rotating, flipping, scaling, and adding noise to images.
- For text data: synonym replacement, random insertion, and back-translation.

## Glossary

- **Epoch**: One training cycle through the entire dataset. It is common to have multiple iterations per an epoch. The number of epochs you use in training is unique on your model and use case.
- **Loss Function**: A mathematical function that measures the difference between the predicted output and the actual output. The goal of training is to minimize this loss function. Some metrics that can be used as loss functions include Mean Squared Error (MSE) for regression tasks and Cross-Entropy Loss for classification tasks.
- **Sparse**: A dataset is considered sparse when it contains a large number of features, but only a small subset of those features are relevant or have non-zero values for each data point. In the context of regularization, L1 regularization can lead to sparse models by driving some weights to zero, effectively performing feature selection.

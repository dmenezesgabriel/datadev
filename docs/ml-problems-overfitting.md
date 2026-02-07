# Overfitting

## Prevention techniques

Is possible to prevent overfitting by diversify and scale the training data or using some other data science techniques.

### Early Stopping

Early stopping monitors the performance of the model on the validation dataset and stops training when validation performance stops improving. This prevents overfitting by stopping training at the optimal number of epochs, before it learns noise data. Getting the time right is important, else the model still not give accurate results.

- Specific to Neural Networks.

### Pruning

**Feature selection** technique that removes less important features from the dataset, which can help reduce overfitting by simplifying the model and reducing the risk of capturing noise in the data.

### Regularization

Regularization is a set of training techniques that reduce overfitting by penalizing large weights, which can effectively reduce the influence of less important features.

Less important features don’t naturally have large weights—they only get them when the model overfits, and regularization exists to prevent exactly that.

#### L1 Regularization

L1 is the sum of weights

- Performs feature selection by driving some weights to zero.
- Computationally inefficient
- Sparse output

#### l2 Regularization

L2 is the sum of squared weights

- All features remain considered, just weighted
- Computationally efficient
- Dense output

### Dropout

Dropout layers randomly set a fraction of input units(neurons) to 0 at each update during training time, which helps prevent overfitting by introducing noise into the training process. This encourages the model to learn more generalized patterns.

- Specific to Neural Networks.

## Glossary

- **Epoch**: One complete pass through the entire training dataset. During each epoch, the model's parameters are updated based on the loss calculated from the training data.
- **Loss Function**: A mathematical function that measures the difference between the predicted output and the actual output. The goal of training is to minimize this loss function.
- **Sparse**: A dataset is considered sparse when it contains a large number of features, but only a small subset of those features are relevant or have non-zero values for each data point. In the context of regularization, L1 regularization can lead to sparse models by driving some weights to zero, effectively performing feature selection.

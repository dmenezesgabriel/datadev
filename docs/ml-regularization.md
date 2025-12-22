# Regularization

Is a technique used in machine learning to prevent overfitting by adding a penalty to the loss function. Regularization helps to constrain the model complexity, ensuring that it generalizes better to unseen data.

## Types of Regularization

### L1 Regularization

L1 is the sum of weights

- Performs feature selection by driving some weights to zero.
- Computationally inefficient
- Sparse output

### l2 Regularization

L2 is the sum of squared weights

- All features remain considered, just weighted
- Computationally efficient
- Dense output

### Dropout

Dropout is a regularization technique where randomly selected neurons are ignored during training.

- Specific to Neural Networks.

### Early Stopping

Using less epochs during training to prevent the model from overfitting the training data.

- Specific to Neural Networks.

# XGBoost

It is a series of decision trees built sequentially, where each new tree attempts to correct the errors of the previous trees.

It uses gradient descent to minimize the loss function, making it highly effective for both regression and classification tasks.

Used for both regression and classification tasks.

- Memory-bound, not compute-bound.

## Hyperparameters

- Subsample: The fraction of samples to be used for fitting the individual base learners. It helps prevent overfitting.
- Learning Rate: Controls the step size at each iteration while moving toward a minimum of the loss function. A smaller learning rate requires more trees but can lead to better performance.
- Gamma: Minimum loss reduction required to make a further partition on a leaf node of the tree. It helps control overfitting.
- Alpha: L1 regularization term on weights. It can help with feature selection by penalizing large coefficients.
- Lambda: L2 regularization term on weights. It helps prevent overfitting by penalizing large coefficients.
- eval_metric: The metric used to evaluate the performance of the model during training. Common choices include 'rmse' for regression and 'logloss' for classification. For false positive rate control, `AUC` is often used.
- scale_pos_weight: Controls the balance of positive and negative weights, useful for unbalanced classes. It helps improve model performance on imbalanced datasets.
- max_depth: The maximum depth of a tree. Increasing this value makes the model more complex and more likely to overfit.

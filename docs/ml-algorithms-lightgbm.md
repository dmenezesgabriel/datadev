# LightGBM

- Gradient Boosting Decision Tree
- Similar to XGBoost
- More like to CatBoost
- Used for regression, classification, and ranking tasks.
- requires txt/csv input data format
- memory-bound, not compute-bound.

## Hyperparameters

- learning_rate: Controls the step size at each iteration while moving toward a minimum of the loss function. A smaller learning rate requires more trees but can lead to better performance.
- num_leaves: The number of leaves in one tree. Increasing this value makes the model more complex and more likely to overfit.
- feature_fraction: The fraction of features to be used for fitting the individual base learners. It helps prevent overfitting.
- bagging_fraction: The fraction of data to be used for fitting the individual base learners.
- max_depth: The maximum depth of a tree. Increasing this value makes the model more complex and more likely to overfit.
- min_data_in_leaf: The minimum number of data points required in a leaf. It helps prevent overfitting.

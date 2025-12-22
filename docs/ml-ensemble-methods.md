# Ensemble Methods

Ensemble methods combine multiple machine learning models to improve overall performance and robustness. By aggregating the predictions of several models, ensemble methods can reduce variance, bias, and improve generalization.

## Bagging

Generate N new training sets by random sampling with replacement. Each resampled model can be trained independently and in parallel.

- Better at reducing overfitting.

## Boosting

Assign weights to each training instance. Train models sequentially, with each model focusing on the instances that were misclassified by previous models. Combine the predictions of all models to make a final prediction.

- Better accuracy

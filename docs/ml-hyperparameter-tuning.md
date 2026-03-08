# Hyperparameter Tuning

Unlike model parameters (such as weights or coefficients), which are automatically learned during training, hyperparameters are not learned by the model itself. Instead, they define aspects like model complexity, learning behavior, and regularization, influencing how well the model fits the training data and generalizes to new data.

## Some Common Hyperparameters

| Hyperparameter     | What it Controls                        | Simple Explanation                                        | Real-Life Example                                               | Impact if Too Low                   | Impact if Too High                                        | Typical Values                             | Common Algorithms                                       |
| ------------------ | --------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------- |
| **learning_rate**  | Size of each learning update            | How big a step the model takes when adjusting predictions | Adjusting your aim when learning to throw darts                 | Learning is very slow               | Training becomes unstable and overshoots optimal solution | 0.01 – 0.1                                 | XGBoost, LightGBM, Gradient Boosting, Neural Networks   |
| **max_depth**      | Maximum depth of decision trees         | How complex the decision rules can become                 | Loan approval rules adding more conditions                      | Model too simple → underfitting     | Model memorizes training data → overfitting               | 3 – 10                                     | XGBoost, LightGBM, Random Forest, Decision Trees        |
| **n_estimators**   | Number of trees/iterations              | Number of models combined to make the final prediction    | A committee where many members vote                             | Model may not learn enough patterns | Training slower and higher overfitting risk               | 100 – 1000                                 | XGBoost, LightGBM, Random Forest, Gradient Boosting     |
| **subsample**      | Fraction of training data used per tree | Each tree trains on a random subset of data               | Political polling using a sample instead of the full population | Model may miss useful patterns      | Less randomness → higher overfitting                      | 0.6 – 0.9                                  | XGBoost, LightGBM, Gradient Boosting                    |
| **regularization** | Penalty for model complexity            | Discourages overly complex models                         | Speed limits preventing reckless driving                        | Model can overfit                   | Model becomes too simple and underfits                    | 0.01 – 10 (varies)                         | XGBoost, LightGBM, Logistic Regression, Neural Networks |
| **class_weight**   | Importance assigned to each class       | Makes the model pay more attention to minority classes    | Fraud detection where fraud is rare                             | Model ignores minority class        | Too many false positives                                  | `balanced` or custom (e.g., `{0:1, 1:10}`) | Logistic Regression, Random Forest, SVM, Decision Trees |
| **n_clusters**     | Number of clusters to form              | Defines how many groups the algorithm should find         | Customer segmentation into groups                               | Groups become too broad             | Groups become fragmented and noisy                        | 2 – 20 (problem dependent)                 | K-Means, Gaussian Mixture Models, Spectral Clustering   |

## Approaches

- [automatic-model-tuning-how-it-works](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-how-it-works.html)

### Grid search

Chooses a combination of values from the range of categorical values specified when you create the tuning job. Only categorical parameters are supported when using grid search. The number of training jobs is automatically calculated by to be the total number of distinct categorical combinations possible.

### Random search

Chooses a random combination of hyperparameter values in the specified range for each training job. The choice of hyperparameters does not depend on the results of previous runs, so you can run multiple training jobs in parallel.

### Bayesian optimization

Bayesian optimization is a method for choosing good hyperparameters by learning from previous training runs. You start by trying a few different hyperparameter values and training the model. After each run, you record how well the model performed using a chosen metric.

Using these past results, Bayesian optimization builds an internal model that estimates which hyperparameter values are likely to work well. It then selects the next set of hyperparameters to test based on what it has learned so far. This cycle repeats until you reach a limit, such as a maximum number of training runs or a time limit.

### Hyperband

Hyperband is a hyperparameter tuning method that speeds up training by stopping bad runs early. It starts many training jobs with different hyperparameter values and gives each one a small amount of resources, such as a few training epochs.

As results come in, Hyperband compares their intermediate performance and allocates more resources to the best-performing configurations, while automatically stopping those that perform poorly. It works best for iterative models that report metrics during training (like neural networks) and often finds good hyperparameters faster than random search and some Bayesian optimization approaches.

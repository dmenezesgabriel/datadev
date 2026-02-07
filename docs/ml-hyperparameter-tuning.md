# Hyperparameter Tuning

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

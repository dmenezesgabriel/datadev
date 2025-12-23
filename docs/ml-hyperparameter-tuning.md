# Hyperparameter Tuning

## Approaches

### Grid search

- Limited to categorical parameters
- Brute force, tries every possible combination

### Random search

- Chooses a random combination of hyperparameter values on each job
- No dependence on prior runs, so they can run in parallel

### Bayesian optimization

- Treats tuning as a regression problem
- Learns from each run to converge on optimal values

### Hyperband

- Appropriate for algorithms that publish results iteratively (like training a neural network over several epochs)
- Dynamically allocates resources, early stopping, parallel
- Much faster than random search or Bayesian

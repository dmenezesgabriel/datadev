# Tunning Neural Networks

## Hyperparameters

### Learning Rate

We start at some random point, and sample difference solutions (weights) seeking to minimize some cost function over many epochs. How far apart these samples are is the learning rate.

- Neural Networks are trained by gradient descendent algorithms.
- too high learning rate means we might overshoot the optimal solution.
- too low learning rate means we might take too long to get the optimal solution.

### Batch Size

The batch size is the number of training examples utilized in one iteration.

- Small batch sizes tend to not get stuck in local minima, but take longer to converge.
- Large batch sizes can converge on the wrong solution at random

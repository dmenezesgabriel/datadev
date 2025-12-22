# Activation Functions

Is the function inside of a neuron and define the output of a node given an input or set of inputs.

## Activation Functions Types

### Linear Activation Function

It does not really do anything. Just returns the input as output.

### Binary Step Activation Function

It is used for binary classification problems. It returns 0 if the input is less than a certain threshold and 1 otherwise.

### Sigmoid/Logistic Activation Function

It maps the input to a value between 0 and 1. It is commonly used in the output layer for binary classification problems.

- Non linear

### Hyperbolic Tangent (Tanh) Activation Function

It maps the input to a value between -1 and 1.

- Non linear

### Rectified Linear Unit (ReLU) Activation Function

It returns the input if it is positive and 0 otherwise.

- Dying ReLU problem: instead of go to 0, it goes to a small value like 0.01 to fix it.

### Parametric ReLU (PReLU) Activation Function

It is a variant of ReLU where the slope of the negative part is learned during training.

### Leaky ReLU Activation Function

It is a variant of ReLU where the slope of the negative part is a small constant value (e.g., 0.01).

### Exponential Linear Unit (ELU) Activation Function

It is similar to ReLU but it smooths the negative part using an exponential function.

### Swish Activation Function

It is a smooth, non-monotonic function defined as f(x) = x \* sigmoid(x). It has been shown to outperform ReLU in some deep learning models.

### Softmax Activation Function

It is used in the output layer for multi-class classification problems. It converts outputs to probabilities of each classification.

## Choosing the Right Activation Function

- For multiple classification problems, use Softmax in the output layer.
- RNNs often use Tanh
- For everything else, start with ReLU
- If ReLU is not working well, try Leaky ReLU, then PReLU or Maxout
- Swish for really deep networks

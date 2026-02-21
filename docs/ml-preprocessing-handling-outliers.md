# Handling Outliers

Outliers are data points that differ significantly from other observations in a dataset. They can arise due to measurement errors, data entry errors, or genuine variability in the data.

## Identifying Outliers

### Variance

Variance measures how "spread out" the data points are around the mean. A high variance indicates that the data points are more dispersed, while a low variance suggests they are closer to the mean. Outliers can significantly increase the variance of a dataset.

Variance is simply the average of the squared differences from the Mean.

Example:

**Dataset:**

$$
[2, 4, 4, 4, 5, 5, 7, 9]
$$

**Mean:**

$$
\mu = \frac{2 + 4 + 4 + 4 + 5 + 5 + 7 + 9}{8} = 5
$$

**Variance:**

$$
\sigma^2 = \frac{
(2-5)^2 + (4-5)^2 + (4-5)^2 + (4-5)^2 + (5-5)^2 + (5-5)^2 + (7-5)^2 + (9-5)^2
}{8}
$$

$$
= \frac{9 + 1 + 1 + 1 + 0 + 0 + 4 + 16}{8}
$$

$$
= \frac{32}{8} = 4
$$

## Handling Outliers

### Removal

Removing outliers from the dataset can help improve model performance. However, this approach should be used cautiously, as it may lead to loss of valuable information.

We can filter values between two standard deviations from the mean for example.

# Feature Engineering - Missing data

From simpler to more complex and effective techniques for handling missing data:

- Mean replacement: Filling missing values with the mean of the column.
- Median replacement: Using the median value to fill in missing data. Used when outliers are present.
- Mode replacement: Filling missing values with the most frequently occurring value in the column. Used with categorical data.
- Dropping rows: Removing rows with missing values entirely. Useful when the dataset is large and missing data is minimal.
- KNN imputation: Using the k-nearest neighbors algorithm to estimate and fill in missing values based on similar data points. Better for numerical data, for categorical data can be used with Hamming distance.
- Deep learning imputation: Leveraging neural networks to predict and fill in missing values based on patterns in the data. Works well for categorical data.
- Regression imputation: Using regression models to predict missing values based on other features in the dataset. Suitable for numerical data. One of the most advanced techniques is MICE (Multiple Imputation by Chained Equations).
- Get more data: If possible, gather additional data to fill in the gaps.

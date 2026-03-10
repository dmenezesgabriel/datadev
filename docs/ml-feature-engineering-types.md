# Feature engineering Types

## Feature Creation (Encoding, Binning)

Refers to the creation of new features from existing data to help with better predictions.

Examples:

- one-hot-encoding: transform values in columns with boolean 1 or 0 (Ex: cities, product categories)
- binning: continuous numerical values into groups (ex: age, salary, temperature)
- splitting (Ex: date to year, month and day, and full name to first and last name)
- calculated features (ex: Body Mass Index, total purchase value, account age from signup date)

## Feature Transformation

- Imputation (missing)
- Missing indicators (1 or 0 for missing)
- Outlier clipping
- Feature interaction (Cartesian product. Ex: age_income, age \* income)
- Outlier clipping
- Scaling/normalization
- Invalid value replacement

## Feature Extraction (PCA, LDA)

Involves reducing the amount of data to be processed using dimensionality reduction and noise removal techniques, reducing the amount of memory and computing power required while still maintaining the original data characteristics.

Examples:

- PCA (Principal Component Analysis)
- LDA (Linear Discriminant Analysis)
- IDA (Independent Component Analysis)

### Principal Component Analysis

PCA is a dimensionality reduction technique that converts many correlated features into a smaller number of new features (principal components) while keeping as much variance(information) as possible.

- Unsupervised: does not use labels
- Linear transformation

Imagine you have 2 features:

| height | weight |
| ------ | ------ |
| 170    | 70     |
| 180    | 80     |
| 160    | 60     |

These features are high correlated, so instead of using both PCA uses a new axis that captures the largest variation in data

Use cases:

- image compression
- feature reduction before training

## Feature Selection

Is the process of selecting a subset of extracted features.

Examples:

- Feature importance score
- Correlation matrix

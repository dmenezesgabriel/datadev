# Feature Engineering – Handling Missing Data

- **MCAR** – Missing Completely At Random
- **MAR** – Missing At Random (depends on observed variables)
- **MNAR** – Missing Not At Random (depends on unobserved value itself)

# Mean Replacement

**Definition**
Replace missing numerical values with the column mean.

**When to Use**:

- Numerical features
- Data roughly normally distributed
- Low percentage of missing values
- Baseline / quick prototype

**Pros**

- Very simple and fast
- Keeps dataset size unchanged
- Easy to implement in pipelines

**Cons**

- Reduces variance
- Distorts distribution
- Sensitive to outliers
- Can bias correlations

!!! note "Note"

    Avoid when distribution is skewed or when missingness is not random.

# Median Replacement

**Definition**
Replace missing values with the column median.

**When to Use**:

- Numerical data
- Skewed distributions
- Presence of outliers
- Robust baseline

**Pros**

- Robust to outliers
- Simple
- Maintains dataset size

**Cons**

- Still reduces variance
- Ignores relationships between features

!!! note "Note"

    Often better default than mean in real-world tabular datasets.

# Mode Replacement

**Definition**
Fill missing values with the most frequent value.

**When to Use**:

- Categorical features
- Low missing percentage

**Pros**

- Very simple
- Preserves dataset size
- Works well for low-cardinality categorical features

**Cons**

- Can distort class distribution
- Adds bias toward dominant category

# Dropping Rows (Listwise Deletion)

**Definition**
Remove rows containing missing values.

**When to Use**:

- Missing percentage is very small
- Large dataset
- Missingness is completely random (MCAR)

**Pros**

- No artificial data introduced
- Statistically clean if MCAR

**Cons**

- Reduces dataset size
- Risk of bias if missingness is not random
- Dangerous for small datasets

# KNN Imputation

**Definition**
Use k-nearest neighbors to estimate missing values from similar samples.

**When to Use**:

- Numerical data
- Moderate dataset size
- Features correlated
- Non-linear relationships

**Pros**

- Uses multivariate information
- More accurate than mean/median
- Works for complex patterns

**Cons**

- Computationally expensive
- Sensitive to feature scaling
- Poor performance in high dimensions

!!! note "Note"

    Requires scaling (e.g., StandardScaler) before applying.

# Regression Imputation

**Definition**
Predict missing values using regression models trained on other features.

Advanced approach: MICE (Multiple Imputation by Chained Equations).

**When to Use**:

- Numerical data
- Strong relationships between variables
- Medium to large datasets

**Pros**

- Preserves relationships between features
- More statistically sound
- MICE handles uncertainty via multiple imputations

**Cons**

- Assumes model is correct
- Risk of data leakage if not careful
- Computationally heavier

---

# Deep Learning Imputation

**Definition**
Use neural networks (e.g., autoencoders) to reconstruct missing values.

**When to Use**:

- Large datasets
- High-dimensional data
- Complex nonlinear dependencies
- Image, text, or complex structured data

**Pros**

- Captures complex nonlinear patterns
- Works well in high-dimensional spaces
- Powerful for large-scale data

**Cons**

- Requires large data
- Harder to interpret
- Risk of overfitting
- Computationally expensive

!!! note "Note"

    More common in research or high-scale ML systems.

# Get More Data

**Definition**
Acquire missing values from external systems, users, logs, or other sources.

**When to Use**:

- Business-critical feature
- Missingness is systematic
- High ROI feature

**Pros**

- Most accurate solution
- Improves overall data quality
- No statistical distortion

**Cons**

- Costly
- Time-consuming
- Sometimes impossible

## Summary

- Small dataset + low missing rate = Median or Drop
- Skewed data = Median
- Correlated features = Regression or KNN
- High dimensional + complex data = Deep learning
- High-stakes model (finance/health) = MICE
- Production quick baseline = Median

# Machine Learning Monitoring

1. Service Health
2. Model Performance
   - Regression: RMSE, MAE, R²
   - Classification: Accuracy, Precision, Recall, F1-score, AUC-ROC

3. Data quality and integrity
   - Amount of missing values
   - Counts
   - Value ranges

4. Data and concept drift
   - Changes in data distribution

5. Performance by segment
6. Model bias/ fairness
7. Outliers
8. Explainability

## Batch Deployment

Based on training data or past batch predictions:

- Expected data quality
- Data distribution type (e.g., Gaussian, Poisson)
- Descriptive statistics (mean, median, mode, stddev, min, max, percentiles)

## Non-Batch Deployment

Descriptive statistics and quality:

- Calculate metrics continuously or incrementally

Statistical tests on a continuous data stream:

- Pick a window function (e.g, moving windows or without moving reference) and "compare" windows.

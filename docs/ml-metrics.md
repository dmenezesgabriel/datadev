# Metrics

## Recall

$$ Recall = \frac{TruePositives}{TruePositives + FalseNegatives} $$

- Also known as Sensitivity or True Positive Rate (TPR)
- Percent of positives rightly predicted
- Good choice when _False Negatives_ are very important. Ex: Fraud detection

## Precision

$$ Precision = \frac{TruePositives}{TruePositives + FalsePositives} $$

- Correct positives
- Good choice when _False Positives_ are very important. Ex: drug testing

## Specificity

$$ Specificity = \frac{TrueNegatives}{TrueNegatives + FalsePositives} $$

- Also known as True Negative Rate (TNR)
- Percent of negatives rightly predicted

## F1-Score

$$ F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall} $$

- Harmonic mean of Precision and Recall

## MAE

$$ MAE = \frac{1}{n} \sum\_{i=1}^{n} |y_i - \hat{y}\_i| $$

- Mean Absolute Error

## RMSE

$$ RMSE = \sqrt{\frac{1}{n} \sum\_{i=1}^{n} (y_i - \hat{y}\_i)^2} $$

- Root Mean Squared Error
- Accuracy measurement

## ROC Curve

Receiver Operating Characteristic Curve

- Plots TPR vs FPR at various threshold settings
- Points above represent good classification performance, better than random guessing
- Ideal curve would be a point in the upper left corner (100% TPR, 0% FPR)
- The more is the curve bows towards the upper left corner, the better the model is

## AUC - Area Under the ROC Curve

Equal to the probability that a classifier will rank a randomly chosen positive instance higher than a randomly chosen negative one.

- Commonly used metric for comparing classifiers

## P-R Curve

Precision-Recall Curve

- Higher area under the curve represents both high recall and high precision
- Similar to ROC curve, but better suited for information retrieval tasks

## R² - Coefficient of Determination

Squared correlation between observed and predicted values.

# Unbalanced data

Large discrepancies in class distribution (positives vs. negatives) can lead to biased models that favor the majority class. Here are some techniques to handle unbalanced data:

- Oversampling: Increase the number of instances in the minority class by duplicating existing ones or generating synthetic samples (e.g., using SMOTE - Synthetic Minority Over-sampling Technique).
- Undersampling: Reduce the number of instances in the majority class by randomly removing samples to balance the class distribution. Usually not recommended for small datasets.
- Adjusting class weights: Modify the learning algorithm to give more importance to the minority class during training. Many machine learning libraries allow setting class weights.

## SMOTE

SMOTE (Synthetic Minority Over-sampling Technique) is a popular method for addressing class imbalance by generating synthetic samples for the minority class. It works by selecting a minority class instance and finding its k-nearest neighbors. New synthetic samples are created by interpolating between the selected instance and its neighbors.

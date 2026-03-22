# ✅ MLOps Requirements Gathering

## 1. Process Data (Collect → Preprocess → Feature Engineering)

### 💼 Business

- [ ] What decision will this model support?
- [ ] What is the cost of false positives vs false negatives?
- [ ] What are the business success metrics (revenue, churn, risk)?
- [ ] How often are predictions needed (real-time vs batch)?
- [ ] Are there regulatory or compliance constraints?

### 🧠 Data Science

- [ ] What data sources are available? Are they reliable?
- [ ] How is the label defined? Is it noisy or delayed?
- [ ] How is data collected (batch, streaming, manual)?
- [ ] What are known data quality issues?
- [ ] What preprocessing steps are required?
- [ ] Can features be reproduced consistently in production?

## 2. Feature Store (Online / Offline)

### 💼 Business

- [ ] Is real-time prediction required?
- [ ] What is the acceptable latency SLA?

### 🧠 Data Science

- [ ] Which features are needed online vs offline?
- [ ] Are features point-in-time correct (no leakage)?
- [ ] What is the required feature freshness?
- [ ] Can features be reused across models?

## 3. Develop Model (Train, Tune, Evaluate)

### 💼 Business

- [ ] What is the minimum acceptable performance?
- [ ] What is the current baseline (rules or human)?
- [ ] How do model metrics map to business KPIs?

### 🧠 Data Science

- [ ] What evaluation metrics best reflect business impact?
- [ ] How do we handle class imbalance?
- [ ] Do we need explainability?
- [ ] What validation strategy will be used?
- [ ] Are experiments reproducible?

## 4. Deploy (Batch / Real-Time Inference)

### 💼 Business

- [ ] What latency is required (ms, seconds, hours)?
- [ ] What is expected traffic volume?
- [ ] What happens if the model fails?

### 🧠 Data Science

- [ ] Are training and inference features consistent?
- [ ] Batch or real-time inference?
- [ ] What are compute and model size constraints?
- [ ] Do we need A/B testing or shadow deployment?

## 5. Monitor (Model + Data + System)

### 💼 Business

- [ ] What signals indicate business impact degradation?
- [ ] How quickly must issues be detected and resolved?

### 🧠 Data Science

- [ ] How do we detect data drift?
- [ ] How do we detect concept drift?
- [ ] How do we monitor prediction distributions?
- [ ] What alert thresholds are defined?
- [ ] Do we monitor inputs, outputs, and performance?
- [ ] Do we have ground truth feedback loops?

## 6. Feedback Loop (Retraining / Continuous Learning)

### 💼 Business

- [ ] How often should the model be updated?
- [ ] What is the cost vs benefit of retraining?
- [ ] Can users provide feedback?

### 🧠 Data Science

- [ ] How do we collect new labeled data?
- [ ] Is retraining scheduled or triggered?
- [ ] How do we prevent data leakage in retraining?
- [ ] Are data, features, and models versioned?

## 7. Governance (Registry, Lineage, Compliance)

### 💼 Business

- [ ] Are there auditability requirements?
- [ ] Who owns and is accountable for the model?

### 🧠 Data Science

- [ ] Can we trace model → data → code → features?
- [ ] Are models versioned and reproducible?
- [ ] Are training artifacts and metadata stored?

## 🧠 Final Alignment Check

- [ ] Business Goal is clearly defined
- [ ] Decision supported by the model is clear
- [ ] Prediction output is well specified
- [ ] Data required is available and reliable
- [ ] System constraints (latency, scale, cost) are defined

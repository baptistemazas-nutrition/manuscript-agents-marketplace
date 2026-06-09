# Machine Learning Protocol (research-grade)

Prediction has different validity rules than explanation. Optimism from leakage/overfitting is the default failure — design against it.

## 1. Frame
- Task: classification / regression / time-to-event / clustering (unsupervised).
- Goal: prediction (this protocol) vs explanation (use regression in the inference path).
- Remove ids and **any variable that encodes the outcome or is measured after it** (leakage).

## 2. Leakage-safe pipeline
All preprocessing — imputation, scaling, encoding, feature selection, resampling — inside a `sklearn.Pipeline` fit within each training fold. Never `fit` a transformer on the full dataset before splitting. `stats_toolkit.ml_classify` does this by construction.

## 3. Validation design
- Stratified k-fold (default 5–10) for classification; **grouped** k-fold when rows cluster (patients, sites) to prevent group leakage.
- Tuning → **nested CV** (inner loop tunes, outer loop estimates performance) or a held-out test set; never report tuned performance from the same folds used to tune.
- Small data → repeated CV; report variability.

## 4. Class imbalance
Class weights or in-fold resampling (SMOTE inside the pipeline). Report **PR-AUC** and sensitivity/specificity at a justified threshold, not accuracy alone.

## 5. Metrics
- Discrimination: ROC-AUC, PR-AUC.
- Calibration: calibration curve, Brier score, calibration slope/intercept.
- Regression: RMSE, MAE, R².
- Always report a CI / cross-fold spread.

## 6. Interpretability
Linear models → standardized coefficients; trees/boosting → permutation importance + SHAP. Importances are associational, not causal.

## 7. Overfitting & honesty
Compare train vs CV performance (learning curves). **AUC ≈ 1.0 is a red flag** — investigate leakage. Pre-register the analysis where possible.

## 8. Reporting — TRIPOD+AI
Follow TRIPOD+AI (see manuscript-guidelines): data source, participants, predictors, outcome, sample size, missing-data handling, model development, validation (internal/external), performance with uncertainty, and limitations. Predictive models for clinical use need external/temporal validation before claims.

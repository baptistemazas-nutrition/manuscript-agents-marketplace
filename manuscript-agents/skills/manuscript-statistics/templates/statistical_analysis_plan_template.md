# Statistical Analysis Plan — {study title}

**Version**: {n}  **Date**: {date}  **Status**: locked before confirmatory analysis

## 1. Objectives & hypotheses
- Primary: {H1, with direction and estimand}
- Secondary: {…}
- Exploratory: {…}

## 2. Design & analysis populations
- Design: {cross-sectional / cohort / case-control / RCT / repeated-measures / survival}
- Analysis sets: {ITT / per-protocol / complete-case / full}

## 3. Outcomes
| Outcome | Type | Role |
|---|---|---|
| {name} | {continuous/binary/ordinal/count/time-to-event} | primary/secondary/exploratory |

## 4. Predictors & covariates
- Exposure(s): {…}
- Adjustment set (causal rationale / DAG): {…}  (no stepwise selection on p-values)

## 5. Methods per hypothesis
| Hypothesis | Primary method | Assumption handling |
|---|---|---|
| {H1} | {test/model} | {parametric→nonparametric rule, etc.} |

## 6. Missing data
- Mechanism assumption: {MCAR/MAR/MNAR}; Primary: {complete-case / MICE, m=…}; Sensitivity: {…}

## 7. Multiplicity
- Family: {…}; Correction: {Holm/Bonferroni/BH/hierarchical}

## 8. Sample size / power
- {a priori calc OR achieved-precision statement; no post-hoc observed power}

## 9. Sensitivity analyses
- {outliers in/out; imputed vs complete-case; alternative specs}

## 10. Software & reproducibility
- {Python x.y; statsmodels/scikit-learn/lifelines versions}; seed = {n}

## Amendments
| Date | Change | Rationale | Results re-labeled? |
|---|---|---|---|

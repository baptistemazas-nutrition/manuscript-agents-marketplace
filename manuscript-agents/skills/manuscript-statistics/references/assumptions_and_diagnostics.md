# Assumptions & Diagnostics

For each test/model: the assumption, how to check, and the remedy if violated.

## t-test / ANOVA
- **Normality** (of residuals or per group): Shapiro-Wilk (n≤5000) / D'Agostino; Q-Q plot. Violated → non-parametric (Mann-Whitney/Kruskal) or transform (log, Box-Cox).
- **Homogeneity of variance**: Levene (median-centered). Violated → Welch t / Welch ANOVA.
- **Independence**: design-level; clustered data → mixed model.

## Linear regression (OLS)
- **Linearity**: residual-vs-fitted; partial-residual plots → add splines/polynomials.
- **Homoscedasticity**: residual plot / Breusch-Pagan → robust (HC3) SE or WLS.
- **Normality of residuals**: Q-Q (mainly affects small-sample inference).
- **Multicollinearity**: VIF > 5–10 → drop/combine predictors.
- **Influential points**: Cook's distance, leverage → sensitivity analysis.

## Logistic regression
- Linearity of logit for continuous predictors (Box-Tidwell / splines).
- No perfect separation (watch huge SEs) → penalized (Firth) logistic.
- Adequate events-per-variable (EPV ≥ ~10) or use penalization.
- Calibration + discrimination (Hosmer-Lemeshow cautiously; calibration plot, C-statistic).

## Count models
- Mean ≈ variance for Poisson; overdispersion (Pearson χ²/df ≫ 1) → negative binomial; excess zeros → zero-inflated/hurdle.

## Cox proportional hazards
- **Proportional hazards**: `proportional_hazard_test` / Schoenfeld residuals. Violated → stratified Cox, time-varying covariate, or report time-window HRs.
- Linearity of continuous covariates (martingale residuals); influential points (dfbeta).

## Mixed models / GEE
- Correct random-effects/correlation structure; check ICC; residual diagnostics at each level.

## General
Report which checks were done and the decisions in the Methods. A failed assumption is not a dead end — it selects a different valid method.

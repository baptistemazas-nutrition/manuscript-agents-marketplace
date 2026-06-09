# Method Selection Decision Trees

Pick the method from **outcome type × design × number of groups × pairing/clustering** — never from the result you want.

## Step 1 — Classify the outcome
- **Continuous** (interval/ratio): weight, blood pressure, score.
- **Binary**: responder yes/no, dead/alive.
- **Categorical (>2, nominal)**: tumor subtype.
- **Ordinal**: stage I–IV, Likert.
- **Count / rate**: exacerbations per year.
- **Time-to-event**: months to relapse (+ censoring).

## Step 2 — Comparing groups (one exposure/grouping)

### Continuous outcome
| Groups | Independent | Paired/repeated |
|---|---|---|
| 2 | normal → Student (equal var) / Welch (unequal); non-normal → Mann-Whitney | normal → paired t; non-normal → Wilcoxon signed-rank |
| ≥3 | normal → one-way ANOVA (+ Tukey); non-normal → Kruskal-Wallis (+ Dunn) | repeated-measures ANOVA / mixed model; non-normal → Friedman |

### Binary / categorical outcome
- 2×2, expected cell ≥5 → chi-square; any expected <5 → Fisher exact.
- R×C → chi-square (+ standardized residuals); ordinal exposure → Cochran-Armitage trend.
- Paired binary → McNemar; paired multi-category → Stuart-Maxwell.

### Ordinal outcome
- 2 groups → Mann-Whitney; ≥3 → Kruskal-Wallis; or proportional-odds (ordinal logistic) model.

### Count outcome
- Poisson; if variance ≫ mean (overdispersion) → negative binomial; excess zeros → zero-inflated.

### Time-to-event
- Curves → Kaplan-Meier; 2+ group comparison → log-rank; adjusted → Cox PH (check PH); competing events → Fine-Gray.

## Step 3 — Association between two continuous variables
- Linear + ~bivariate normal → Pearson; monotonic/ranks/outliers → Spearman; with adjustment → linear regression.

## Step 4 — Multivariable / adjusted models (outcome dictates the model)
| Outcome | Model | Reports |
|---|---|---|
| Continuous | Linear (OLS); robust SE if heteroscedastic | β (95% CI) |
| Binary | Logistic | OR (95% CI) |
| Ordinal | Proportional-odds logistic | OR (95% CI) |
| Nominal >2 | Multinomial logistic | OR (95% CI) |
| Count/rate | Poisson / negative binomial (+ offset) | IRR/RR (95% CI) |
| Time-to-event | Cox proportional hazards | HR (95% CI) |
| Clustered/repeated | Linear/GLMM mixed-effects or GEE | as above + ICC |

## Step 5 — Predictive (vs explanatory) goal
If the goal is prediction, route to `machine_learning_protocol.md` (CV, calibration, TRIPOD+AI) — different validity criteria than explanatory modeling.

## Covariate selection (adjustment)
Choose confounders by causal reasoning / DAG and prior knowledge — NOT by stepwise selection on p-values. Pre-specify in the SAP. Avoid adjusting for mediators or colliders.

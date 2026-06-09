# Effect Sizes & Confidence Intervals

Report magnitude + uncertainty for every comparison. A p-value alone is never sufficient (IRON RULE 3).

## Which effect size
| Analysis | Effect size | Notes |
|---|---|---|
| 2-group mean diff | Mean difference (units) + Cohen's d / Hedges' g | g corrects small-sample bias |
| ANOVA | η² / ω² (variance explained) | ω² less biased |
| Correlation | r (Pearson) / ρ (Spearman) | report r and CI |
| 2×2 / logistic | Odds ratio; risk ratio / risk difference (clinically clearer) | OR overstates risk when outcome common |
| Categorical assoc | Cramér's V / φ | |
| Count/rate | Rate ratio (IRR) | |
| Survival | Hazard ratio; also median survival, RMST | HR assumes PH |
| Regression (cont.) | Standardized β; partial R² | |
| Prediction | AUC-ROC, PR-AUC, R², calibration slope | see ML protocol |

## Confidence intervals
- Report 95% CI for every primary estimate; state the estimate, CI, and exact p together.
- Prefer CIs to bare significance; interpret width as precision.
- For non-normal/small samples consider bootstrap CIs.
- Keep CI and p consistent (a 95% CI excluding the null ⇔ p<0.05 for the same test).

## Reporting
"Drug reduced weight by 3.5 kg (95% CI 2.1–4.9; Welch t-test, p = 3.8×10⁻⁵; Hedges' g = 1.10)."

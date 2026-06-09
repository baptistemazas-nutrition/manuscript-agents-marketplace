# Missing Data Protocol

## 1. Quantify
Per-variable and per-pattern missingness; visualize patterns. Report counts, not just percentages.

## 2. Reason about the mechanism
- **MCAR** (missing completely at random): missingness unrelated to observed/unobserved data. Testable-ish (Little's test) but rarely strictly true.
- **MAR** (missing at random): missingness depends only on observed data → principled imputation works.
- **MNAR** (missing not at random): depends on the unobserved value itself → needs sensitivity analysis / pattern-mixture; no method fully fixes it.
Mechanism is a judgment from the data-collection context, not a pure statistical test.

## 3. Choose a strategy
| Situation | Strategy |
|---|---|
| Tiny missingness (<~5%), plausibly MCAR | Complete-case (note it) |
| Non-trivial, MAR | **Multiple imputation** (MICE), pool by Rubin's rules |
| Missing predictor in prediction model | In-pipeline imputation (inside CV folds) |
| MNAR suspected | Pattern-mixture / delta-adjustment **sensitivity** analysis |

**Never**: single mean/median imputation of a primary outcome; imputing then treating values as observed without uncertainty; imputing the outcome to inflate n.

## 4. Always
- Pre-specify the approach in the SAP.
- Run a **complete-case sensitivity analysis** alongside the imputed primary analysis and compare.
- Report the software, number of imputations, and variables in the imputation model.

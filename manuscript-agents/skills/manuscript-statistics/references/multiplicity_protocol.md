# Multiplicity Protocol

Testing many hypotheses inflates the false-positive rate. Decide the strategy in the SAP, before testing.

## 1. Define the family
A family = the set of tests over which you want to control error (e.g., all secondary endpoints; all pairwise group contrasts). Primary confirmatory endpoints are usually kept few and may be tested without correction if truly primary and pre-specified.

## 2. Choose the control
| Goal | Method | When |
|---|---|---|
| Strong FWER control | **Bonferroni** | few tests, simple |
| FWER, more power | **Holm** (step-down) | default FWER choice |
| FWER with correlated tests | Hochberg / Westfall-Young | correlated endpoints |
| Control false discovery rate | **Benjamini-Hochberg (FDR)** | many exploratory tests (e.g., screening) |
| Ordered hypotheses | **Hierarchical / gatekeeping** | endpoint hierarchy |
| Pairwise after ANOVA | Tukey HSD (means), Dunn (ranks) | post-hoc group contrasts |

## 3. Apply & report
- Use `stats_toolkit.p_adjust(pvals, method=...)` (`holm`, `bonferroni`, `fdr_bh`).
- Report both raw and adjusted p-values and the family definition.
- Subgroup analyses are exploratory unless pre-specified and powered; label them and correct.

## 4. Don't
- Don't test everything then narrate only the significant ones (outcome/​subgroup fishing).
- Don't switch the primary endpoint after seeing results.

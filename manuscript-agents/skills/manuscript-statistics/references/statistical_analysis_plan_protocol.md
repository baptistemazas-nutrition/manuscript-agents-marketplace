# Statistical Analysis Plan (SAP) Protocol

A SAP pre-commits the analysis so results are confirmatory, not constructed. Write it before confirmatory testing (IRON RULE 1).

## Required sections
1. **Objectives & hypotheses** — primary and secondary, with direction; estimands defined.
2. **Design & populations** — analysis sets (ITT/per-protocol; full/complete-case).
3. **Outcomes** — primary outcome(s) (few!), secondary, exploratory — explicitly separated.
4. **Predictors/exposures & covariates** — adjustment set chosen by causal reasoning/DAG, pre-specified (no stepwise on p).
5. **Methods per hypothesis** — the test/model from the decision tree; assumption-handling rules in advance.
6. **Missing data** — mechanism assumption + primary approach (e.g., MICE) + complete-case sensitivity.
7. **Multiplicity** — family definition + correction (FWER/FDR/hierarchical).
8. **Sample size / power** — a priori if available; otherwise the precision the achieved n yields (no post-hoc observed power).
9. **Sensitivity analyses** — list them now (outliers in/out, alternative specs, imputed vs complete-case).
10. **Software & reproducibility** — language, key libraries, random seed.

## Discipline
- Lock the SAP (one user confirmation) before running confirmatory analyses.
- Any later change is an amendment: logged, dated, with rationale, and the affected results re-labeled exploratory if the change was outcome-informed.

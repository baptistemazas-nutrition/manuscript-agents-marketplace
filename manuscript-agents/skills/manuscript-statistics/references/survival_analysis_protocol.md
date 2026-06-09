# Survival (Time-to-Event) Protocol

## Setup
- Define time origin, event, and censoring precisely. Confirm non-informative censoring.
- Variables: duration column + event indicator (1=event, 0=censored).

## Description
- Kaplan-Meier estimator per group; report median survival (+ 95% CI) and survival at key landmarks; include a **number-at-risk** table.

## Group comparison
- **Log-rank** test (equal weight) for the primary unadjusted comparison; Wilcoxon (Gehan) if early differences matter.

## Adjusted modeling — Cox PH
- `stats_toolkit.cox_model` → HR (95% CI).
- **Check proportional hazards** (`proportional_hazard_test` / Schoenfeld). If violated:
  - stratify on the offending covariate, or
  - add a time-varying coefficient/interaction with time, or
  - report time-segmented HRs / use RMST difference.
- Check functional form (martingale residuals) and influence (dfbeta).

## Competing risks
If other events preclude the event of interest, KM overestimates incidence — use cumulative incidence functions and **Fine-Gray** subdistribution hazards.

## Alternatives
- Restricted mean survival time (RMST) when PH fails or for an absolute-time interpretation.
- Parametric (Weibull/AFT) models when a smooth hazard is justified.

## Reporting
n, events, follow-up (median + IQR), HR (95% CI), PH check result, and the KM figure.

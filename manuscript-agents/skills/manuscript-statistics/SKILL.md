---
name: manuscript-statistics
description: "Autonomous statistical analysis agent team for study data. Give it a CSV/Excel dataset and a research question; it runs the analysis end-to-end in Python: data profiling and cleaning, a pre-specified analysis plan, a descriptive Table 1, assumption checks, univariate tests, multivariable models (linear/logistic/Cox/mixed), survival analysis, and machine learning (leakage-safe cross-validation, AUC, SHAP), with effect sizes, 95% CIs, multiplicity control, figures, a Methods+Results draft, and reproducible code. Hands results to academic-paper and academic-pipeline. Modes: auto, sap, descriptive, univariate, multivariable, survival, ml, report, review. Triggers on: analyze my data, statistical analysis, run statistics, Table 1, t-test, ANOVA, chi-square, regression, logistic regression, Cox, survival analysis, Kaplan-Meier, machine learning, predictive model, which test should I use, cross these variables, analyse statistique, analyse mes donnees, quel test, croiser les variables."
---

# Manuscript Statistics — Autonomous Statistical Analysis Agent Team

Turn a raw study dataset (CSV / Excel / TSV) into analysis-ready, publication-quality results and a Methods+Results draft — autonomously, in Python, end to end. This is the **data → results** stage that lets the suite go from a spreadsheet to a finished manuscript.

> **Division of labor.** The researcher owns the *question* and the *interpretation*: which outcome, which exposures/covariates, the study design, the hypotheses, and what the findings mean. Everything mechanical — choosing the correct test for the design, checking assumptions, fitting models, correcting for multiplicity, building tables and figures, and writing the numbers up — is done autonomously. Ask the user **only** the scoping questions that genuinely require their domain knowledge; do not ask the user to choose statistical methods.

## IRON RULES

1. **Pre-specify before you peek.** Write the Statistical Analysis Plan (SAP) — primary/secondary outcomes, the test/model for each hypothesis, multiplicity strategy, sensitivity analyses — *before* running confirmatory tests on the outcome. Anything decided after seeing outcome associations is labeled **exploratory**, never confirmatory. This is the core defense against p-hacking.
2. **Every number traces to code.** No statistic appears in any table, figure, or sentence unless it was produced by a script that ran in this session and whose output is shown. No hand-computed or remembered numbers. The reproducibility bundle (script + seed + library versions + data dictionary) is mandatory.
3. **Effect size + 95% CI always; p-value never alone.** Report magnitude and uncertainty, not just significance. State the effect direction and units.
4. **Match the method to the design, not to the desired result.** Respect pairing/clustering, variable types, and assumptions. Do not dichotomize continuous variables to force a simpler test. Do not run a parametric test whose assumptions fail without a stated remedy.
5. **Privacy first.** Study data may contain identifiable or sensitive information. Process it **locally in the sandbox only**; never send raw records to any external tool or web search. De-identify before any output leaves the analysis. See `references/data_access_and_privacy.md`.
6. **Declare every data transformation.** Cleaning, recoding, exclusions, and imputation are logged in the Data Quality Report with counts. Never silently drop or alter rows.

## Modes

| Mode | When | Produces |
|---|---|---|
| `auto` (default) | "analyze my data", a dataset + a question | Full flow: intake → quality → SAP → descriptives → assumptions → inference → (survival/ML if applicable) → figures → integrity → Methods+Results draft + reproducibility bundle |
| `sap` | Before data collection or before unblinding | A pre-registered Statistical Analysis Plan only — no outcome analysis run |
| `descriptive` | "just describe / Table 1" | Data dictionary + Table 1 (overall and by group) + distribution figures |
| `univariate` | "which variables are associated with the outcome" | Bivariate association tests, correctly chosen, with effect sizes + multiplicity note |
| `multivariable` | "adjusted analysis / build a model" | Regression model (linear/logistic/ordinal/Poisson-NB/Cox/mixed/GEE) with diagnostics, adjusted estimates + CIs, forest plot |
| `survival` | time-to-event outcome | Kaplan–Meier, log-rank, Cox PH (+ PH check, competing risks if needed) |
| `ml` | "predict / machine learning / risk model" | Leakage-safe pipeline, nested/CV evaluation, AUC-ROC/PR, calibration, permutation importance + SHAP, TRIPOD+AI-aligned reporting |
| `report` | results already exist | Methods + Results prose + formatted tables, ready for academic-paper |
| `review` | audit an existing analysis | Adversarial statistical review (see `statistical_integrity_agent`) — catches p-hacking, leakage, wrong tests, uncorrected multiplicity |

Modes compose: `auto` runs the relevant subset based on what the data and question require.

## Workflow (auto mode)

**Phase 0 — Environment.** Bootstrap the analysis environment once per session (`assets/bootstrap_env.sh`): installs scipy, statsmodels, scikit-learn, lifelines, pingouin, openpyxl on top of pandas/numpy/matplotlib/seaborn. Load `assets/stats_toolkit.py` as the reusable engine.

**Phase 1 — Intake & data dictionary** (`data_intake_agent`). Load the file, profile every column (type, n, missing %, distribution, levels), infer a draft data dictionary, then ask the *minimal* scoping questions: primary outcome(s); exposure(s)/predictor(s); grouping variable; study design (cross-sectional / cohort / case-control / RCT / repeated-measures / clustered); pairing or clustering id; candidate covariates; the specific cross-tabulations the user wants; directional hypotheses. Confirm the Data Configuration Record.

**Phase 2 — Data quality** (`data_quality_agent`). Missingness rate + plausible mechanism (MCAR/MAR/MNAR) and a matching strategy (complete-case vs multiple imputation), impossible values, outliers, duplicates, type coercion, derived variables. Emit the Data Quality Report; log every transformation.

**Phase 3 — Statistical Analysis Plan** (`analysis_planner_agent`). Map each hypothesis to a method via `references/method_selection_decision_trees.md`; pre-specify primary vs secondary, the multiplicity strategy (`references/multiplicity_protocol.md`), sensitivity analyses, and a sample-size/power note. **Present the SAP and get one confirmation before running confirmatory analyses.**

**Phase 4 — Descriptives** (`descriptive_agent`). Table 1 with per-type summaries (mean±SD or median[IQR] or n(%)), by group, with standardized differences.

**Phase 5 — Assumptions** (`assumption_agent`). For each planned test: normality, variance homogeneity, linearity, proportional hazards, independence, multicollinearity (VIF). Route to parametric / non-parametric / transformed / robust as needed.

**Phase 6 — Inference** (`inferential_agent`). Univariate tests then multivariable models, with effect sizes + 95% CIs, interactions where pre-specified, and model diagnostics.

**Phase 7 — Specialized** (as applicable). `machine_learning_agent` for prediction; survival handled within inference for time-to-event.

**Phase 8 — Figures** (`statistical_visualization_agent`). Publication-quality, colorblind-safe figures with captions.

**Phase 9 — Integrity gate** (`statistical_integrity_agent`). Adversarial review; blocks handoff until every number traces to output and no IRON RULE is violated.

**Phase 10 — Write-up & handoff** (`results_writer_agent` + `reproducibility_agent`). Methods (statistical-analysis paragraph) + Results prose following SAMPL, the StatsResults handoff for academic-paper, and the reproducibility bundle.

## Agent Roster (11)

| Agent | Tier | Responsibility |
|---|---|---|
| `data_intake_agent` | Scoping | Profile data, build dictionary, run the minimal scoping interview |
| `data_quality_agent` | Preparation | Missingness, outliers, duplicates, recoding, imputation — all logged |
| `analysis_planner_agent` | Planning | Author the pre-specified SAP; select methods via decision trees |
| `descriptive_agent` | Analysis | Table 1 / summary statistics by group |
| `assumption_agent` | Analysis | Test assumptions, route to the valid method |
| `inferential_agent` | Analysis | Univariate tests + multivariable & survival models, effect sizes + CIs |
| `machine_learning_agent` | Analysis | Leakage-safe predictive modeling, validation, interpretability, TRIPOD+AI |
| `statistical_visualization_agent` | Output | Forest/KM/ROC/calibration/heatmap/SHAP figures + captions |
| `results_writer_agent` | Output | Methods+Results draft; StatsResults handoff |
| `statistical_integrity_agent` | Gate | Adversarial review; trace-to-output enforcement; p-hacking/leakage detection |
| `reproducibility_agent` | Gate | Save script, seed, versions, dictionary, log; Reproducibility Card |

## Autonomy contract

Given a dataset and a confirmed Data Configuration Record + SAP, run the entire analysis without further questions, choosing every test, model, correction, diagnostic, and figure yourself. Return to the user only at the two designed checkpoints (confirm scoping; confirm SAP) and if a genuine domain decision arises (e.g., a clinically impossible value that only the researcher can adjudicate). Default to the conservative, defensible choice and state it.

## Handoff & integration

- **Into academic-pipeline**: this skill is **Stage 0 (DATA → RESULTS)**. When the user supplies raw data, run here first; the StatsResults artifact then feeds Stage 2 (WRITE). See `references/pipeline_integration.md`.
- **To academic-paper**: emits the **StatsResults** handoff (Methods paragraph, Results prose, Table 1, results tables, figures + captions, reproducibility card) — see `references/pipeline_integration.md` for the schema.
- **With manuscript-guidelines**: the design detected here selects the reporting checklist (STROBE / CONSORT / TRIPOD+AI / ARRIVE…) and statistical reporting follows SAMPL (`references/sampl_reporting_standards.md`).
- **With deep-research**: a research question or methodology blueprint from deep-research pre-populates the SAP.

## References

- `references/method_selection_decision_trees.md` — the "which test/model" logic by outcome type × design × groups × pairing
- `references/assumptions_and_diagnostics.md` — assumption catalog, tests, remedies
- `references/missing_data_protocol.md` — MCAR/MAR/MNAR, complete-case vs multiple imputation, sensitivity
- `references/effect_sizes_and_ci.md` — which effect size per test and how to report it
- `references/multiplicity_protocol.md` — family-wise vs FDR; when to correct
- `references/machine_learning_protocol.md` — leakage, CV design, imbalance, tuning, calibration, interpretability, TRIPOD+AI
- `references/survival_analysis_protocol.md` — KM, log-rank, Cox, PH checks, competing risks
- `references/statistical_analysis_plan_protocol.md` — how to write a pre-specified SAP
- `references/sampl_reporting_standards.md` — SAMPL statistical reporting
- `references/data_access_and_privacy.md` — PHI handling, de-identification, local-only processing
- `references/python_stats_cookbook.md` — runnable recipes + how to drive `stats_toolkit.py`
- `references/reproducibility_card.md` — the reproducibility artifact schema
- `references/pipeline_integration.md` — Stage 0 wiring + StatsResults handoff schema

## Assets

- `assets/stats_toolkit.py` — the reusable Python engine (load, profile, Table 1, auto-test, models, survival, ML, plots)
- `assets/bootstrap_env.sh` — one-line environment bootstrap

## Templates

- `templates/statistical_analysis_plan_template.md`
- `templates/table1_template.md`
- `templates/statistical_methods_section_template.md`
- `templates/results_section_template.md`
- `templates/reproducibility_card_template.md`

## Examples

- `examples/clinical_weight_response_example.md` — group comparison + adjusted model (the "weight response to a molecule" case)
- `examples/ml_prediction_example.md` — predictive model done right
- `examples/autonomous_data_to_paper_example.md` — full data → manuscript run

# Cohort study (STROBE) — manuscript template

For prospective and retrospective cohort studies. Composes with STROBE
2007's 22 items. For case-control or cross-sectional studies, the same
checklist applies but the section structure differs slightly — see
notes inline.

> **Anchoring discipline.** Cohort studies typically have many
> quantitative claims. Every n, every percent, every effect estimate
> with CI is a DataCard.

---

## Title (STROBE Item 1a)

`[Exposure or intervention] and [outcome] in [population]: a
[prospective | retrospective] cohort study`

Include the design term ("cohort study", "case-control study",
"cross-sectional study") in the title.

---

## Abstract (STROBE Item 1b)

Structured per STROBE Item 1b: balanced summary (background, objectives,
methods, results, conclusions). Some journals require an additional
"Importance / Findings / Implications" structure — adopt the journal's
preferred form.

Anchors: DataCard for headline n and primary effect estimate;
FactCards for cited literature.

---

## Introduction

### Background and rationale (STROBE Item 2)

Scientific background and rationale for the investigation.

### Objectives (STROBE Item 3)

Specific objectives, including any pre-specified hypotheses.

Anchors: FactCards for cited literature.

---

## Methods

### Study design (STROBE Item 4)

Present key elements of study design early (cohort prospective vs.
retrospective; case-control matched vs. unmatched; cross-sectional
sampling frame).

### Setting (STROBE Item 5)

Setting, locations, and relevant dates: periods of recruitment,
exposure, follow-up, and data collection.

Anchors: DataCard (`source_type: protocol`) for the study protocol with
dates.

### Participants (STROBE Item 6)

- **Cohort**: eligibility criteria, sources, methods of selection,
  methods of follow-up. For exposed and unexposed groups, give the
  matching criteria and number per group.
- **Case-control**: eligibility, sources, methods of case ascertainment
  and control selection, rationale for case/control choices.
- **Cross-sectional**: eligibility, sources, methods of selection.

Anchors: DataCards for total candidates, eligible, enrolled (with reasons
for non-participation per STROBE Item 13).

### Variables (STROBE Item 7)

Define all outcomes, exposures, predictors, potential confounders, and
effect modifiers. Diagnostic criteria where applicable.

Anchors: MethodCard for any non-trivial diagnostic instrument (DSM-5
SCID, MoCA, MMSE, etc.) with tool_version.

### Data sources / measurement (STROBE Item 8)

For each variable of interest, give sources of data and details of
methods of assessment. Comparability of assessment methods across groups.

Anchors: MethodCard per assessment instrument; DataCards (sample) for
representative measurements.

### Bias (STROBE Item 9)

Efforts to address potential sources of bias. Specific strategies
(matching, stratification, blinded outcome assessment, sensitivity
analyses).

### Study size (STROBE Item 10)

How the study size was arrived at. For underpowered or pragmatic
reasons, document those reasons explicitly rather than retrofitting a
post-hoc power calculation.

Anchors: MethodCard for the power calculation software (G*Power,
PowerAnalysis in R, etc.) with version, OR a DataCard pointing to the
underpowering / pragmatic-size justification.

### Quantitative variables (STROBE Item 11)

How quantitative variables were handled. If categorized, why and on
what cutpoints.

### Statistical methods (STROBE Item 12)

All statistical methods including:

- Methods to control for confounding.
- Methods to examine subgroups and interactions.
- How missing data were addressed.
- Cohort: how loss to follow-up was addressed.
- Case-control: how matching was addressed.
- Cross-sectional: how sampling strategy is reflected in the analysis.
- Sensitivity analyses.

Anchors: MethodCard for the statistical software (R + specific packages
+ versions; SAS; Stata; SPSS) with `configuration:` listing the relevant
packages (e.g., `survival 3.5-5`, `lme4 1.1-31`).

---

## Results

### Participants (STROBE Item 13)

Numbers at each stage: eligible, examined for eligibility, confirmed
eligible, included, completing follow-up, analyzed. Reasons for
non-participation. Flow diagram strongly recommended.

Anchors: DataCards for each per-stage count.

### Descriptive data (STROBE Item 14)

Characteristics of study participants (Table 1). Information on
exposures and potential confounders. Number with missing data per
variable. Cohort: summarize follow-up time.

Anchors: every cell of Table 1 is a DataCard.

### Outcome data (STROBE Item 15)

- Cohort: numbers of outcome events or summary measures over time.
- Case-control: numbers in each exposure category, or summary measures
  of exposure.
- Cross-sectional: numbers of outcome events or summary measures.

### Main results (STROBE Item 16)

Unadjusted estimates AND, if applicable, confounder-adjusted estimates
and their precision (95% CI). Confounders adjusted for and rationale.
Translation of relative risk to absolute risk where meaningful.

Anchors: DataCards for unadjusted and adjusted estimates with CIs.

### Other analyses (STROBE Item 17)

Subgroups, interactions, sensitivity analyses. Distinguish pre-specified
from exploratory.

Anchors: DataCards for each analysis result.

---

## Discussion

### Key results (STROBE Item 18)

Summarize key results with reference to objectives.

### Limitations (STROBE Item 19)

Discuss limitations taking into account sources of potential bias or
imprecision; discuss both direction and magnitude of any potential bias.

### Interpretation (STROBE Item 20)

Cautious overall interpretation considering objectives, limitations,
multiplicity of analyses, results from similar studies, and other
relevant evidence.

### Generalisability (STROBE Item 21)

Discuss generalisability (external validity). Bound to population,
setting, exposure intensity, follow-up duration.

Anchors: FactCards for prior cohorts cited in the comparison.

---

## Funding (STROBE Item 22)

Source of funding and role of funders for the present study (and, if
applicable, for the original study on which the present article is
based).

---

## Data availability statement

Per modern requirement and PRISMA-trAIce / RAISE compliance: explicit
statement on whether the dataset can be shared, with conditions.

---

## See also

- `manuscript-guidelines/checklists/strobe.md` — 22-item checklist this
  template aligns with.
- `manuscript-guidelines/templates/case_series.md` — for small series
  without a comparator.
- `manuscript-guidelines/templates/systematic_review_PRISMA.md` — for
  meta-analytic synthesis of cohort studies.
- `shared/data_card_schema.yaml` — for own-data anchoring.
- `manuscript-citations/references/citeaudit_pattern.md` — for
  per-citation verification at Stages 2.5 / 4.5.

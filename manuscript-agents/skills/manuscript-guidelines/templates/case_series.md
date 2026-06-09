# Case series (small n, no comparator) — manuscript template

For small case series (n ≤ ~5 per CARE 2017 extended scope; n 6–20
borderline — see `manuscript-guidelines/references/checklist_routing.md`
for case-series-vs-cohort routing). Larger series with comparators
should use `cohort_study_STROBE.md`.

> **Routing reminder.** Case series with no comparison group route to
> mode `care`. Series with a comparator (case-control or pseudo-cohort
> structure) route to `strobe`. Mixed or borderline cases trigger user
> escalation per the routing reference.

---

## Title

`Case series: [intervention] in [n] patients with [condition]`

Anchors: none for the title. Include the n in the title or abstract per
common biomedical convention.

---

## Abstract

Structured. Elements:

- **Background** — clinical problem and rationale for compiling a case
  series rather than a single report.
- **Methods** — patient identification, inclusion criteria, intervention,
  assessment timeline.
- **Results** — pooled summary statistics or per-patient detail (n
  determines the appropriate level).
- **Conclusions** — what this small series suggests; explicitly bounded
  by the absence of a comparator.

Anchors: DataCard for headline n; DataCards for any pooled outcome
values; FactCards for cited prior work.

---

## Introduction

Standard. For case series, the introduction often grounds against:

- Why this n is reportable (rare condition, novel intervention).
- The gap between single case reports and full cohort studies in this
  literature.

---

## Methods

### Patient identification and inclusion

- Source population (single-center / multi-center).
- Inclusion criteria (e.g., consecutive patients meeting X criteria
  between dates Y and Z).
- Exclusion criteria.
- Total candidates considered vs. total included; reasons for exclusion.

Anchors: DataCard (`source_type: clinical_record`) for each enrolled
patient's identifying tags (de-identified patient ID, enrollment date,
exclusion reasons if applicable).

### Intervention and assessment

For each patient:

- Intervention details (matching CARE Item 9 specificity).
- Assessment timepoints and instruments (matching CARE Item 10).

Anchors: per-patient MethodCards for the intervention protocol;
DataCards for each assessment timepoint × instrument combination.

### Statistical / summary approach

Small-n case series typically report descriptive statistics (median,
range) rather than inferential statistics. Justify the chosen
descriptors. If any inferential test is used, motivate why it is
appropriate at this n.

Anchors: MethodCard for the analysis software (with version).

---

## Results

### Per-patient table

Standard for case series: a Patient × Variable table with rows for each
patient and columns for demographics, intervention details, primary
outcome, key secondary outcomes, AEs.

Anchors: every cell of the table is a DataCard (anchored to the source
record). Each AE has its own DataCard.

### Pooled summary (if appropriate)

Median + range for each outcome. For series of n ≤ 5, individual data
points are usually more informative than pooled statistics.

Anchors: DataCards for each pooled value.

---

## Discussion

- Pattern across the series (where homogeneous; where heterogeneous).
- Comparison with prior case reports / case series in the literature
  (FactCards).
- Limitations: small n, no comparator, selection bias, single-center,
  follow-up duration.
- What this series adds; what would be needed for the next study (a
  matched cohort? a registry? an RCT?).

Anchors: FactCards for cited literature.

---

## Limitations (mandatory section, not buried in Discussion)

- **No comparator** — every claim about the intervention's effect must
  be presented as descriptive, not causal.
- **Selection bias** — patients reaching the report may differ from the
  underlying clinical population.
- **Small n** — point estimates are unstable.
- **Single-center** (if applicable) — generalizability bounded.

---

## Ethics / consent / funding / disclosures

Standard. Each patient's informed consent for publication is a separate
DataCard. If consent was waived (e.g., retrospective deceased-patient
review), the IRB waiver document is a DataCard.

---

## See also

- `manuscript-guidelines/checklists/care_2017.md` — checklist for small
  case series.
- `manuscript-guidelines/templates/clinical_case_report_CARE.md` — for
  n = 1 cases.
- `manuscript-guidelines/templates/cohort_study_STROBE.md` — for case
  series with comparator structure (effectively a cohort).

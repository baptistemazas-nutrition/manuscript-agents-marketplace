# Systematic review (PRISMA 2020) — manuscript template

For systematic reviews and meta-analyses. Composes with PRISMA 2020's
27 items. The 12-item PRISMA 2020 Abstract checklist is folded into the
Abstract section below.

> **Composition with Wu's compliance_agent.** Systematic reviews trigger
> Wu's `compliance_agent` (v3.4.0+) at Stages 2.5 / 4.5 for PRISMA-trAIce
> + RAISE methodological compliance (Schema 12). Our `guideline_verifier_agent`
> runs the PRISMA 2020 reporting-completeness check (Schema 14) in parallel.
> The two layers do not overlap.

---

## Title (PRISMA Item 1)

`[Topic]: a systematic review [and meta-analysis]`

Identify the report as a systematic review (or systematic review +
meta-analysis). Avoid "review of the literature" without "systematic"
qualifier — that's a narrative review and routes to mode `none`.

---

## Abstract (PRISMA Item 2; PRISMA-2020 Abstract checklist)

Structured. Abstract elements that must be present (12 items):

- Background, objectives, eligibility criteria, information sources,
  risk-of-bias assessment, synthesis methods, results, limitations,
  conclusions, registration, funding, abstract length.

Anchors: DataCard for headline n studies + n participants; DataCards for
primary effect estimates with precision; FactCards (none typical in
abstract — mostly own analysis).

---

## Introduction

### Rationale (PRISMA Item 3)

Why the review is needed; what gap or controversy motivates it.

### Objectives (PRISMA Item 4)

Explicit objective(s) in PICO / PEO / PECO / PICOS form.

Anchors: FactCards for prior reviews referenced.

---

## Methods

### Eligibility criteria (PRISMA Item 5)

Inclusion and exclusion criteria. How studies were grouped for the
syntheses.

Anchors: DataCard (`source_type: protocol`) for the protocol document
that pre-specified these criteria.

### Information sources (PRISMA Item 6)

All databases, registers, websites, organizations, reference lists, and
other sources searched. Date of last search per source.

For biomedical SRs, the **biomedical-first cascade**
(`shared/biomedical_verification_protocol.md`) applies: PubMed primary,
ClinicalTrials.gov for trials, Cochrane CENTRAL for trials, bioRxiv for
preprints, S2 fallback. Document each.

Anchors: DataCard for the search-source list with last-search dates.

### Search strategy (PRISMA Item 7)

Full search strategies for all databases (in main text or appendix);
reproducible.

Anchors: DataCard per database's search strategy. The verbatim_anchor
is the actual search string; verifier checks it round-trips against the
database.

### Selection process (PRISMA Item 8)

Number of reviewers screening each record / report; independence;
automation tools used.

Anchors: MethodCard for screening software (Covidence, Rayyan, etc.)
with version.

### Data collection process (PRISMA Item 9)

Methods used to collect data; reviewer independence; investigator
contact; automation.

### Data items (PRISMA Item 10a, 10b)

- 10a: All outcomes for which data were sought; methods to decide which
  results to include.
- 10b: All other variables (participant characteristics, intervention
  details, funding sources). Assumptions about missing data.

Anchors: DataCard for each outcome's definition; DataCard for each
extracted variable's source.

### Study risk of bias assessment (PRISMA Item 11)

Tool used (RoB 2 / ROBINS-I / NIH Quality Assessment / etc.). Reviewer
count and independence.

Anchors: MethodCard for the RoB tool with version.

### Effect measures (PRISMA Item 12)

Per outcome, the effect measure(s) used in synthesis (RR, OR, HR, MD,
SMD, etc.).

### Synthesis methods (PRISMA Item 13a–f)

- 13a: Eligibility for synthesis (tabulating characteristics, comparing
  to intended groupings).
- 13b: Methods to prepare data (handling of missing summary stats; data
  conversions).
- 13c: Methods to tabulate / display individual studies and syntheses.
- 13d: Methods to synthesize (synthesis approach; if meta-analysis: model,
  heterogeneity assessment, software).
- 13e: Methods to explore heterogeneity (subgroup, meta-regression).
- 13f: Sensitivity analyses.

Anchors: MethodCard for the meta-analysis software (R `meta` /
`metafor`, RevMan, Stata `meta`, etc.) with version and configuration
(model: random vs fixed; heterogeneity: I² + tau²).

### Reporting bias assessment (PRISMA Item 14)

Methods to assess risk due to missing results (funnel plot, Egger's
test, ORBIT).

### Certainty assessment (PRISMA Item 15)

Methods to assess certainty / confidence in the body of evidence (GRADE
or comparable).

Anchors: MethodCard for GRADEpro GDT (or equivalent) with version.

---

## Results

### Study selection (PRISMA Item 16a, 16b)

- 16a: PRISMA flow diagram with numbers at each stage.
- 16b: Borderline-exclusion list with reasons.

Anchors: DataCards for each per-stage count; DataCards for each
borderline exclusion.

### Study characteristics (PRISMA Item 17)

Per-study characteristics table.

Anchors: DataCards for each cell of the characteristics table.

### Risk of bias in studies (PRISMA Item 18)

Per-study RoB judgments (table or traffic-light figure).

Anchors: DataCards for each per-study RoB judgment with rationale.

### Results of individual studies (PRISMA Item 19)

Per-outcome, per-study summary statistics + effect estimate + precision.

### Results of syntheses (PRISMA Item 20a–d)

- 20a: Brief summary of contributing studies' characteristics + RoB.
- 20b: Pooled effect estimate with precision; statistical heterogeneity
  measures.
- 20c: Causes of heterogeneity investigated.
- 20d: Sensitivity analyses.

Anchors: DataCards for pooled estimates, heterogeneity measures (I², tau²,
prediction intervals), subgroup results, sensitivity analyses.

### Reporting biases (PRISMA Item 21)

Per-synthesis assessment of reporting bias risk.

### Certainty of evidence (PRISMA Item 22)

GRADE summary-of-findings table per outcome.

---

## Discussion

### Discussion (PRISMA Item 23a–d)

- 23a: General interpretation in context of other evidence.
- 23b: Limitations of the evidence.
- 23c: Limitations of the review processes.
- 23d: Implications for practice, policy, future research.

Anchors: FactCards for cited literature. The
`citation_coherence_verifier_agent` cross_section mode is particularly
relevant here — SRs often cite the same paper multiple times across
Methods (for inclusion rationale), Results (where the paper appears in
synthesis), and Discussion (for interpretation context). Each FactCard's
`source_claim_region` should be set to disambiguate uses.

---

## Other information

### Registration and protocol (PRISMA Item 24a–c)

- 24a: Registration name, number, or "not registered".
- 24b: Protocol location, or "no protocol prepared".
- 24c: Amendments to registration / protocol with explanations.

Anchors: DataCard pointing to registry record (PROSPERO, etc.) and
protocol document.

### Support (PRISMA Item 25)

Sources of financial / non-financial support; role of funders.

### Competing interests (PRISMA Item 26)

Per-author declaration.

### Availability of data, code and other materials (PRISMA Item 27)

Per-artifact availability statement: data extraction forms, extracted
data, analysis code, other materials.

---

## See also

- `manuscript-guidelines/checklists/prisma_2020.md` — 27-item checklist.
- `shared/biomedical_verification_protocol.md` — search-source cascade
  for biomedical SRs.
- `shared/compliance_checkpoint_protocol.md` — Wu's PRISMA-trAIce + RAISE
  methodology compliance (Schema 12) that runs alongside our PRISMA
  reporting-completeness check (Schema 14).
- `manuscript-citations/agents/citation_coherence_verifier_agent.md` —
  Phase F use-coherence check, especially relevant for SR Discussions.

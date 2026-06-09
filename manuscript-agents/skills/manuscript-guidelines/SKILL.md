---
name: manuscript-guidelines
description: "EQUATOR reporting-guideline compliance for biomedical manuscripts. Eight modes covering CARE (case reports), STROBE (observational), PRISMA 2020 (systematic reviews / meta-analyses), CONSORT 2010 (RCTs), SRQR (qualitative), ARRIVE 2.0 (animal), TRIPOD+AI (prediction models), and SQUIRE 2.0 (quality improvement). Auto-detects research design from the manuscript draft, runs the matching checklist, and emits a per-item compliance report (Schema 14) for the integrity gate. Triggers on: case report, case series, cohort study, randomized trial, systematic review, qualitative study, animal study, prediction model, AI model paper, quality improvement, EQUATOR, CARE, STROBE, PRISMA, CONSORT, SRQR, ARRIVE, TRIPOD, SQUIRE, reporting checklist, reporting guideline."
---

# manuscript-guidelines — EQUATOR reporting-guideline compliance

Reporting-guideline enforcement layer for biomedical manuscripts. Sits next
to Wu's existing integrity layers (5-type Ansari taxonomy in
`integrity_verification_agent`, PRISMA-trAIce + RAISE in `compliance_agent`)
without duplicating their work. Where Wu's gates check that citations are
real and that systematic-review methodology is sound, this skill checks that
the manuscript reports what the chosen study design requires the manuscript
to report.

This skill is part of the manuscript-agents v2.0 fork. It is original to the
fork; the upstream Cheng-I Wu academic-research-skills suite does not include
EQUATOR-checklist coverage.

## Quick Start

```
Run the CARE compliance check on this case report draft.
Run STROBE compliance on the cohort manuscript.
Auto-detect the appropriate guideline and run it.
```

## When this skill triggers

Any time a biomedical manuscript needs a reporting-guideline compliance
check, and on every Stage 2.5 / Stage 4.5 integrity boundary inside the
`academic-pipeline` orchestrator (see Phase 2.2 wiring).

The skill **does not** apply to:
- Editorials, commentaries, viewpoints, opinion pieces — these have no
  EQUATOR guideline. Mode `none` returns a brief non-blocking report.
- Narrative reviews (use mode `none`; PRISMA is for *systematic* reviews).
- Conference abstracts, letters to the editor, book chapters — mode `none`.
- Pure theoretical / methodological papers without empirical data — mode
  `none`.

## Routing — paper type → checklist

The orchestrator selects a checklist in three steps:

1. **Mode parameter wins.** If the user supplies an explicit mode
   (e.g., `manuscript-guidelines care`), the verifier uses that checklist.
   No detection runs.
2. **Auto-detect.** If no mode parameter, `paper_type_detector_agent` reads
   the manuscript's title + abstract + methods and returns one of:
   `care | strobe | prisma | consort | srqr | arrive | tripod_ai | squire | none`.
3. **Verifier runs.** `guideline_verifier_agent` loads the matching
   `checklists/<name>.md`, evaluates the manuscript item-by-item, emits a
   Schema 14 EQUATOR Compliance Report.

When the detector is uncertain (low confidence between two designs), it
returns its best guess plus an `alternatives[]` field; the orchestrator
surfaces this to the user for confirmation before running the verifier.

See `references/checklist_routing.md` for the full mapping table including
edge cases (case series vs. cohort, scoping vs. systematic review,
quasi-experimental designs, etc.).

## Modes

| Mode | Checklist | Items | Applies to | Spectrum |
|------|-----------|-------|------------|----------|
| `care` | `checklists/care_2017.md` | 13 | Single case reports, small case series | fidelity |
| `strobe` | `checklists/strobe.md` | 22 | Cohort, case-control, cross-sectional | fidelity |
| `prisma` | `checklists/prisma_2020.md` | 27 | Systematic reviews + meta-analyses | fidelity |
| `consort` | `checklists/consort_2010.md` | 25 | Randomized controlled trials | fidelity |
| `srqr` | `checklists/srqr.md` | 21 | Qualitative research | fidelity |
| `arrive` | `checklists/arrive_2.md` | 21 | Animal research (Essential 10 + Recommended 11) | fidelity |
| `tripod_ai` | `checklists/tripod_ai.md` | 27 | Prediction-model studies (incl. AI/ML) | fidelity |
| `squire` | `checklists/squire_2.md` | 18 | Quality improvement reports | fidelity |
| `none` | (no checklist) | 0 | Manuscripts with no applicable EQUATOR guideline | balanced |

All checklist counts above are the canonical item counts of the underlying
guideline; sub-items (CONSORT 1a/1b style) are documented inside the
checklist file but not double-counted in this table.

## Operational workflow

```
Stage 2.5 / Stage 4.5 entry
     |
     |-- (mode parameter present?)
     |       Yes -> use it; skip detection
     |       No  -> [paper_type_detector_agent] -> detected_type + confidence
     |             (low-confidence case escalates to user)
     |
     |-- detected_type == "none"?
     |       Yes -> emit "no applicable EQUATOR guideline" report; do NOT block
     |       No  -> [guideline_verifier_agent] with checklists/<type>.md
     |
     +-- emit Schema 14 EQUATOR Compliance Report
         to the integrity-gate consumer (academic-pipeline orchestrator).
```

## Integration with Wu's existing integrity layers

| Layer | Source | Role | Output |
|-------|--------|------|--------|
| Citation integrity | upstream `integrity_verification_agent` | Detects fabricated/misrepresented references (5-type Ansari taxonomy) | Schema 5: Integrity Report |
| Methodology compliance | upstream `compliance_agent` | PRISMA-trAIce + RAISE for systematic reviews | Schema 12: Compliance Report |
| **EQUATOR reporting completeness** | **this skill** | **Per-design reporting-checklist coverage** | **Schema 14: EQUATOR Compliance Report** |

These three layers compose at Stage 2.5 / 4.5. They do not overlap.
- Wu's `compliance_agent` enforces *methodological rigour* in systematic
  reviews specifically.
- This skill enforces *reporting completeness* across all eight EQUATOR
  domains (including SR via PRISMA, but also case reports, RCTs, etc.).

## Verdict semantics

For each checklist item the verifier emits one of:

| Verdict | Meaning |
|---------|---------|
| `PASS` | Item is reported clearly and completely. |
| `PARTIAL` | Item is mentioned but missing required detail (e.g., confidence intervals omitted, sample-size justification thin). |
| `MISSING` | Item is required by the guideline but absent from the manuscript. |
| `NOT_APPLICABLE` | Item does not apply to this manuscript (e.g., CARE Patient Perspective for an unconscious patient at all timepoints). Justification required. |

`MISSING` items below a configurable severity threshold do not block the
pipeline; the report surfaces them as revision recommendations. Critical
`MISSING` items (those flagged `severity: critical` in the checklist file)
do block at Stage 4.5.

## Anti-patterns

| # | Anti-pattern | Why it fails | Correct behavior |
|---|--------------|--------------|------------------|
| 1 | Treating `NOT_APPLICABLE` as default | Hides reporting gaps behind a non-applicability claim | Justify every `NOT_APPLICABLE` verdict in the report; the user must accept |
| 2 | Mode-forcing a poor fit | Running CARE on a cohort study because "it's a clinical paper" | The detector + routing reference exist for a reason; trust them |
| 3 | Asserting compliance from absence | Marking PASS because nothing contradicts the item | PASS requires positive evidence (a quoted passage from the manuscript) |
| 4 | ⚠️ IRON RULE: Silent disagreement with the user-supplied mode | User says "CARE" but the manuscript is clearly STROBE-shaped | Run user-requested mode AND surface a routing warning; never silently override the user |
| 5 | Padding `PARTIAL` instead of `MISSING` | "Partial" is the polite verdict; misuse hides genuine omissions | If the required content is absent, it is `MISSING`, not `PARTIAL` |

## Quality standards

1. ⚠️ **IRON RULE**: Every verdict must cite a verbatim passage from the
   manuscript (or quote its absence in a specific location). No bare
   verdicts.
2. The verifier never generates content for the manuscript; it only grades
   what is written.
3. The detector outputs must be reproducible for a given manuscript text;
   if confidence is below 0.7, escalate to user.
4. The `none` verdict is non-blocking and informational; it does not
   prevent the pipeline from advancing.

## Agent file references

| Agent | File |
|-------|------|
| paper_type_detector_agent | `agents/paper_type_detector_agent.md` |
| guideline_verifier_agent | `agents/guideline_verifier_agent.md` |

## Reference files

| Reference | Purpose |
|-----------|---------|
| `references/checklist_routing.md` | Paper-type → checklist mapping; edge cases; escalation rules |

## Templates

| Template | Purpose |
|----------|---------|
| (deferred to Phase 6) | Domain templates for case reports, cohort studies, etc. |

## Examples

| Example | Demonstrates |
|---------|-------------|
| `examples/care_compliance_report_example.md` | Shape of a Schema 14 EQUATOR Compliance Report on a hypothetical TOC/TCA-style case report |

## Output language

Follows user input. Checklist item names retained in English (canonical
EQUATOR terminology); rationale and recommendations follow user language.

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 0.1.0 |
| Last Updated | 2026-04-29 |
| Maintainer | Gonzague de France |
| License | CC-BY-NC 4.0 (inherited from upstream) |
| Origin | Original to manuscript-agents v2.0 fork (Phase 2.1) |

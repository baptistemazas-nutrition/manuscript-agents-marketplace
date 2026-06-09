# Checklist Routing — paper type → EQUATOR guideline

Reference document for `paper_type_detector_agent` and the `academic-pipeline`
orchestrator. Defines how a manuscript draft maps to one of nine routing
outcomes (eight EQUATOR checklists + `none`), how edge cases resolve, and
when the orchestrator must escalate to the user.

## Canonical mapping

| Research design | Routed mode | Guideline | Items |
|-----------------|-------------|-----------|-------|
| Single case report | `care` | CARE 2017 | 13 |
| Small case series (n ≤ ~5, no comparison group) | `care` | CARE 2017 (extended) | 13 |
| Cohort study (prospective or retrospective) | `strobe` | STROBE | 22 |
| Case-control study | `strobe` | STROBE | 22 |
| Cross-sectional study / survey | `strobe` | STROBE | 22 |
| Systematic review | `prisma` | PRISMA 2020 | 27 |
| Meta-analysis | `prisma` | PRISMA 2020 | 27 |
| Randomized controlled trial (any) | `consort` | CONSORT 2010 | 25 |
| Pilot / feasibility RCT | `consort` | CONSORT 2010 + extension caveats | 25 |
| Cluster RCT | `consort` | CONSORT 2010 (cluster extension noted) | 25 |
| Qualitative research | `srqr` | SRQR | 21 |
| Animal experimental research | `arrive` | ARRIVE 2.0 | 21 |
| Prediction-model study (development or validation) | `tripod_ai` | TRIPOD+AI 2024 | 27 |
| ML/AI clinical-prediction paper | `tripod_ai` | TRIPOD+AI 2024 | 27 |
| Quality improvement project | `squire` | SQUIRE 2.0 | 18 |

## `none` outcomes

| Manuscript class | Why `none` | Notes |
|------------------|------------|-------|
| Editorial, commentary, viewpoint, opinion | No EQUATOR guideline applies | Verifier emits brief non-blocking note |
| Narrative review (non-systematic) | PRISMA is for systematic reviews only | Suggest the author note "narrative review" explicitly in the title to avoid PRISMA confusion |
| Letter to the editor | Insufficient structure for any full checklist | — |
| Conference abstract | Length precludes full reporting checklists | — |
| Scoping review | PRISMA-ScR applies but is not in our eight | Add PRISMA-ScR in a future phase if the user needs it |
| Pure theoretical / conceptual paper | No empirical data to grade | — |
| Protocol-only paper | SPIRIT applies but is not in our eight | Add SPIRIT in a future phase if needed |
| Mixed methods, balanced components | GRAMMS applies but is not in our eight; no dominant component to route to | Verifier's `rationale` should suggest splitting into parallel STROBE + SRQR runs if the user wants component-wise grading |
| Book chapter or educational material | Out of scope | — |

## Edge cases and disambiguation

### Case-like designs

| Detail | Route | Why |
|--------|-------|-----|
| 1 patient, narrative timeline | `care` | Single case report — primary CARE use |
| 2–5 patients, no controls | `care` | Case series, CARE-extended scope |
| 6–20 patients, no controls | Borderline. Default `care`; surface STROBE alternative | Case series at this size sometimes reported under STROBE for cohort-like analysis |
| 6+ patients with a comparator | `strobe` | Has cohort/case-control structure regardless of label |
| Retrospective chart review with comparison | `strobe` | Cross-sectional or cohort, depending on temporality |

### Review-type designs

| Detail | Route | Why |
|--------|-------|-----|
| Systematic search + flow diagram + appraisal | `prisma` | Canonical systematic review |
| Meta-analysis only | `prisma` | PRISMA 2020 covers meta-analyses |
| Network meta-analysis | `prisma` | PRISMA-NMA exists; for now route to `prisma` and surface NMA caveat in rationale |
| Scoping review | `none` | PRISMA-ScR not implemented at v0.1 |
| Umbrella review (review of reviews) | `prisma` | PRISMA 2020 covers it; surface "umbrella" caveat |

### Trial designs

| Detail | Route | Why |
|--------|-------|-----|
| Randomized assignment, individual-level | `consort` | Canonical CONSORT use |
| Cluster randomization | `consort` | CONSORT 2010 + cluster extension; surface caveat |
| Stepped-wedge | `consort` | Cluster extension; surface caveat |
| Crossover design | `consort` | CONSORT extension; surface caveat |
| Quasi-experimental, no randomization | `strobe` | Treat as cohort study |
| Pragmatic trial | `consort` | CONSORT-PRO extension exists; route to `consort` for v0.1 |

### Mixed and ambiguous

| Detail | Route | Why |
|--------|-------|-----|
| Mixed methods, qualitative-dominant | `srqr` | Treat as qualitative; flag the quantitative component in rationale |
| Mixed methods, quantitative-dominant | `strobe` or `consort` (per design) | Treat as the dominant component; flag qualitative |
| Mixed methods, balanced | `none` | GRAMMS not in our eight; surface that in rationale |
| Hybrid effectiveness-implementation | Pick by primary outcome's design | Implementation-only → `squire`; effectiveness-only → `consort`/`strobe` |

### AI / prediction-model edge cases

| Detail | Route | Why |
|--------|-------|-----|
| Model development with internal validation | `tripod_ai` | TRIPOD+AI development scope |
| External validation only (others' model) | `tripod_ai` | TRIPOD+AI validation scope |
| Model with explainability/interpretability focus, no prediction outcome | Borderline. Default `tripod_ai`; if no clinical outcome, consider `none` | TRIPOD+AI requires a prediction outcome |
| Diagnostic-accuracy study (sensitivity/specificity only) | `none` | STARD applies; not in our eight |

## Escalation rules

The detector escalates to the user (asks for confirmation before the
verifier runs) when any of the following hold:

1. **Confidence below 0.70.** The detector returns its best guess plus
   1–2 alternatives; the orchestrator pauses for user confirmation.
2. **User-supplied mode parameter mismatches detected type at confidence ≥ 0.85.**
   The verifier runs the user-supplied checklist (per the IRON RULE in
   SKILL.md anti-pattern #4) AND surfaces a `routing_warning` in the report.
3. **Detected type is `none` but the manuscript is long-form empirical research.**
   This usually means the design is unrecognized rather than truly
   guideline-free; surface to user with the closest-fit alternative.

## Future additions (out of scope for v0.1)

| Guideline | Use | Status |
|-----------|-----|--------|
| PRISMA-ScR | Scoping reviews | Defer |
| PRISMA-NMA | Network meta-analyses | Defer |
| SPIRIT | Trial protocols | Defer |
| STARD | Diagnostic accuracy | Defer |
| CHEERS | Economic evaluation | Defer |
| CONSORT-PRO | Patient-reported outcomes in RCTs | Defer |
| COREQ | Qualitative interview / focus group reporting | Defer (SRQR covers most qualitative research) |
| GRAMMS | Mixed methods | Defer |

When the user requests a guideline in this list, route to `none` and
surface the gap in the rationale. Adding any of these is a follow-up
phase: new checklist file under `checklists/`, update this routing
reference, update detector closed vocabulary, update SKILL.md modes
table.

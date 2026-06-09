# Pipeline integration — manuscript-guidelines at Stages 2.5 / 4.5

This document specifies how `manuscript-guidelines` slots into Wu's
`academic-pipeline` orchestrator at the integrity boundaries (Stages 2.5
and 4.5). It is the canonical reference for the [WIRE] in
`academic-pipeline/SKILL.md` (one paragraph under "Integrity Review
Protocol").

## Where it runs

Stage 2.5 (pre-review) and Stage 4.5 (post-revision). Same boundaries as
Wu's `integrity_verification_agent` and `compliance_agent`. The three
checks compose; they do not duplicate each other.

| Layer | Source | What it checks |
|-------|--------|----------------|
| Citation integrity | upstream `integrity_verification_agent` | Reference fabrication, citation hallucination (5-type Ansari taxonomy) |
| Methodology compliance | upstream `compliance_agent` | PRISMA-trAIce + RAISE for systematic reviews |
| **EQUATOR reporting completeness** | **this skill** | **Per-design reporting-checklist coverage (8 guidelines + `none`)** |

## Decision flow at Stage 2.5 / 4.5

```
Stage 2.5 / 4.5 entry
   |
   |-- (existing layers run unchanged: integrity_verification_agent + compliance_agent)
   |
   +-- manuscript-guidelines hook
         |
         |-- mode parameter present?
         |     yes -> use it; skip detection
         |     no  -> [paper_type_detector_agent]
         |             returns: detected_type, confidence, alternatives[]
         |
         |-- detector confidence < 0.70?
         |     yes -> orchestrator pauses; surfaces best guess + alternatives;
         |            user confirms before verifier runs
         |     no  -> proceed
         |
         |-- detected_type == "none"?
         |     yes -> emit short non-blocking report; no verifier run
         |     no  -> [guideline_verifier_agent] with checklists/<type>.md
         |
         +-- emit Schema 14 EQUATOR Compliance Report
             (appended to Material Passport compliance_history[]
              alongside Schema 12 entries)
```

## Composition rules with existing layers

1. **Order is irrelevant for grading.** Wu's two layers and ours read the
   same manuscript draft and emit independent reports. The orchestrator
   may run them in any order or in parallel.
2. **All three reports appear on the same Material Passport.** Schema 5
   (Integrity Report), Schema 12 (Compliance Report), and Schema 14
   (EQUATOR Compliance Report) all append to the passport's
   `compliance_history[]` (Schema 5 lives in its own field; 12 and 14
   share the compliance history with `schema` literal disambiguation).
3. **Block semantics combine via OR.** Stage 4.5 advancement requires
   PASS on all three layers. Any single blocking layer halts the pipeline
   until resolved (or overridden via the 3-round ladder).
4. **Override ladder is shared.** Wu's Schema 12 uses a 3-round override
   protocol described in `shared/compliance_checkpoint_protocol.md`. We
   reuse that ladder for Schema 14 critical-severity blocks. No new
   override protocol introduced.

## IRON RULES

1. **User-mode disagreement.** If the user supplied a mode parameter
   AND the detector would have classified differently at confidence ≥ 0.85,
   the verifier runs the user-supplied checklist AND emits a
   `routing_warning` field on the report. The verifier never silently
   switches to its preferred classification. (Schema 14 spec; SKILL.md
   anti-pattern #4.)

2. **Verbatim evidence.** Every per-item verdict carries either a
   verbatim manuscript quote (`PASS` / `PARTIAL` / `NOT_APPLICABLE`) or
   an absence anchor (`MISSING`). A bare verdict is a verifier failure.
   (`shared/handoff_schemas.md` Schema 14.)

3. **`none` does not block.** A `none` verdict (manuscript with no
   applicable EQUATOR guideline) emits a brief informational report and
   advances the pipeline. It does not consume an override-ladder round.

## Detector escalation rules

| Detector confidence | Orchestrator behavior |
|---------------------|------------------------|
| ≥ 0.85 | Run verifier; no user pause |
| 0.70 – 0.85 | Surface best guess + alternatives in the FULL/SLIM checkpoint dashboard for that stage; verifier runs after user confirms |
| < 0.70 | Pause pipeline; require user to confirm or override mode before verifier runs |

## What this WIRE does NOT do

- It does NOT modify `integrity_verification_agent.md`. Wu's agent stays
  focused on the 5-type Ansari taxonomy.
- It does NOT modify `compliance_agent.md`. Wu's agent stays focused on
  PRISMA-trAIce + RAISE.
- It does NOT modify `shared/compliance_checkpoint_protocol.md`. We
  reuse the existing override ladder by reference.
- It does NOT add a new `data_access_level` or `task_type` value to the
  closed vocabularies. Our SKILL.md uses existing values (`raw`,
  `outcome-gradable`).
- It does NOT touch `.claude/CLAUDE.md` Skills Overview table. Adding
  manuscript-guidelines there would force `check_version_consistency` to
  audit our skill against Wu's table; we keep it outside.

## Material Passport interaction

Schema 14 entries follow the same compliance-history append-only rule as
Schema 12. A Stage 2.5 EQUATOR run produces one entry; a Stage 4.5 run
produces another. Both are kept (per Schema 12's append-only rule). At
Stage 4.5 the verifier reads the prior Stage 2.5 entry from the passport
and computes per-item delta (`unchanged | improved | regressed | new_issue | resolved`).

## Test coverage

Phase 2.1 ships a structural manifest at
`tests/baseline/expected_output/layer_b_manuscript_guidelines/baseline_manifest.yaml`.
Phase 2.2 (this WIRE) is covered by:

1. The `assertions.ci_lint_floor_green_with_new_skill` re-run, which
   continues to pass after the SKILL.md edit.
2. A new assertion (added at the time of this WIRE) verifying the
   `[manuscript-agents v2.0 fork]` line is present in
   `academic-pipeline/SKILL.md`.

A real LLM run of the verifier on a manuscript is deferred to Phase 7
(end-to-end on the TOC/TCA case report).

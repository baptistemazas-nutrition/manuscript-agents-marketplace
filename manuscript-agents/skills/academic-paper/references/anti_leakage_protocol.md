# Anti-Leakage Protocol (Knowledge Isolation)

**Status**: v3.3
**Used by**: `draft_writer_agent`, `report_compiler_agent`
**Source**: Adapted from PaperOrchestra (Song et al., 2026, Appendix D.4)

---

## Purpose

When the user provides comprehensive research materials (RQ Brief, Synthesis Report, Annotated Bibliography, experimental data), the writing agent should construct the paper **primarily from those materials**, not from LLM parametric memory. This prevents:

1. **Methodology fabrication (Failure Mode 6)**: The LLM writes a plausible Methods section from training data rather than the user's actual procedure
2. **Implicit knowledge leakage**: The LLM fills gaps with memorized content that may be inaccurate, outdated, or from a different context
3. **Unintentional plagiarism**: The LLM reproduces near-verbatim passages from training data

---

## Protocol

### When to activate

Activate when ALL of the following are true:
- The user has provided research materials via the pipeline handoff (RQ Brief + Synthesis Report + Annotated Bibliography)
- The paper is in `full` or `revision` mode (not `plan` or `outline-only`)
- The materials are substantive (not placeholder stubs)

### When NOT to activate

Do NOT activate when:
- The user is in `plan` or `socratic` mode (exploratory — LLM knowledge is expected)
- The materials are minimal (e.g., only a RQ Brief with no bibliography)
- The user explicitly requests the LLM to supplement with its own knowledge

### Prompt insertion

When activated, prepend the following to the draft_writer_agent's working context:

```
## Knowledge Isolation Directive

You are writing this paper based on the research materials provided in this session:
- RQ Brief, Synthesis Report, and Annotated Bibliography (from deep-research)
- Any additional materials the user has provided (experimental logs, datasets, prior drafts)

Priority rules:
1. PREFER session materials over your parametric knowledge for all factual claims
2. Every claim in the paper MUST be traceable to a source in the Annotated Bibliography or user-provided data
3. If the materials do not cover a topic the outline requires, flag it as [MATERIAL GAP] rather than filling from memory
4. Do NOT introduce references not present in the Annotated Bibliography unless explicitly asked by the user
5. The Methods section must describe ONLY what is documented in the user's materials — do not infer or interpolate experimental procedures

This is NOT a prohibition on using language skills or academic writing knowledge.
You may use your knowledge of academic conventions, writing style, logical argumentation,
and discipline norms. The restriction applies only to FACTUAL CONTENT — claims, citations,
data, and methodology descriptions must come from session materials.
```

### [MATERIAL GAP] handling

> **Tag vocabulary.** The `[MATERIAL GAP]`, `[WEAK EVIDENCE]`, `[GAP]` tags used throughout this protocol are canonically defined in [`shared/compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary`](../../shared/compliance_checkpoint_protocol.md#canonical-gap-tag-vocabulary). This section describes how the anti-leakage writing-time flag interacts with that vocabulary during manuscript production.

When a `[MATERIAL GAP]` is flagged:
1. The gap is surfaced at the next checkpoint
2. The user can provide additional materials, or authorize LLM supplementation for that specific gap
3. If supplemented: the gap section is tagged `[LLM-SUPPLEMENTED]` in the draft metadata for integrity review

---

## Relationship to existing checks

| Check | What it catches | Anti-leakage adds |
|-------|----------------|-------------------|
| Integrity gate (Stage 2.5) | Fabricated citations post-hoc | Prevents fabrication at writing time |
| Failure Mode 6 (Methodology fabrication) | Methods don't match actual procedures | Prevents LLM from inventing procedures |
| Writing Quality Check | AI-typical phrasing patterns | Anti-leakage prevents AI-typical *content* (as opposed to style) |

---

## DataCard / MethodCard discipline ([manuscript-agents v2.0 fork])

The fork adds two card types parallel to FactCard, both targeting
own-experiment materials rather than cited literature:

- **DataCard** (`shared/data_card_schema.yaml`) — anchors a single
  data point (a Y-BOCS score, an electrode coordinate, a stimulator
  amplitude) to a source file with an exact `verbatim_anchor` and
  the `tool_version` that produced it.
- **MethodCard** (`shared/method_card_schema.yaml`) — anchors a
  Methods-section sentence to a protocol document plus every tool
  version named in the sentence.

The anti-leakage protocol above is extended on the fork as follows:

1. **Three legitimate anchors per claim, not just two.** Every
   factual claim in Methods/Results sections must trace to at least
   one of: a FactCard (literature), a DataCard (own data), or a
   MethodCard (own procedure). Claims with no anchor are
   `[MATERIAL GAP]`, same handling as the v3.3 protocol.

2. **Quantitative claims require a DataCard.** Any number that
   appears in Methods or Results — sample size, score, percent
   change, electrode coordinate, stimulation parameter, p-value —
   MUST be anchored to a DataCard. A Methods/Results sentence with
   a quantitative claim and no DataCard anchor is `[MATERIAL GAP]`,
   not LLM-supplied. The draft writer agent emits the gap rather
   than guessing the number.

3. **Tool-naming requires a MethodCard.** Any sentence that names
   a software tool, atlas, model, or pipeline (Lead-DBS, OSS-DBSv2,
   FreeSurfer, fMRIPrep, ANTs, etc.) MUST anchor to a MethodCard
   whose `tool_versions[]` list includes that tool with its version.
   "We used Lead-DBS to localize the electrodes" with no MethodCard
   is a `[METHOD GAP — no protocol]` flag.

4. **Reviewer-side anti-leakage.** When `academic-paper-reviewer`
   agents (and the `revision_coach_agent`) generate revision
   requests, they MUST NOT request data that would force the
   author to fabricate. Requests like "please add subgroup analysis
   by gender" are legitimate ONLY if the data exist and the user
   can produce a DataCard anchored to those data. If no such
   DataCard exists, the appropriate response is `[REVIEWER REQUEST
   UNANSWERABLE — no anchor]` rather than a fabricated subgroup
   analysis. This clause exists to close the loop where reviewer
   pressure becomes a back-door for the failure modes the
   v3.3 protocol catches at writing time.

5. **`[LLM-SUPPLEMENTED]` extends to card-less assertions.** When
   the user explicitly authorizes supplementation for a Methods or
   Results sentence (e.g., "this is well-known boilerplate, you can
   write it"), the resulting passage carries the `[LLM-SUPPLEMENTED]`
   tag AND a note explaining that no FactCard / DataCard / MethodCard
   was provided. The integrity gate (Schema 5 / Schema 14 / Schema 15)
   surfaces these for review at Stage 2.5 / 4.5.

When this fork's pipeline runs against a manuscript that does not
provide DataCards or MethodCards (e.g., a literature-only systematic
review with no own-experiment data), clauses 2 and 3 are no-ops; the
discipline applies only when own-experiment material is in scope.

See `shared/data_card_schema.yaml` and `shared/method_card_schema.yaml`
for the canonical schemas and their per-field anti_leakage_obligations.

## References

- Song, Y. et al. (2026). PaperOrchestra. *arXiv:2604.05018*. Appendix D.4 (Anti-Leakage Prompt).
- Lu, C. et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919. — Mode 6 (Methodology fabrication).

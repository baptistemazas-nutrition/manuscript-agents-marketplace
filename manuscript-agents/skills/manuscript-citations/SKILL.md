---
name: manuscript-citations
description: "Citation coherence verification (BUILD_PLAN extension B, Phase F). Adds Type 6 (source-claim incoherence) coverage on top of Wu's 5-type Ansari taxonomy. Cache-aware verifier with lazy ArticleProfile cache that persists across manuscripts. Two modes: per_citation (Stages 2.5 / 4.5) and cross_section (Stage 4.5 only). Triggers on: citation coherence, citation use, cite audit, source-claim coherence, cross-section consistency, FactCard verification, ArticleProfile, Profile cache."
---

# manuscript-citations — Citation Coherence Verification (Phase F)

Adds use-coherence verification to the manuscript-agents pipeline. Detects
**source-claim incoherence** (Ansari Type 6) — the failure mode where a
citation passes Wu's existing 5-type taxonomy (the paper exists, the
citation matches its metadata, the quote is real) but the way the
manuscript USES that quote either overreaches what the source actually
supports or contradicts how the same source is used in another section.

This skill is original to the manuscript-agents v2.0 fork. The upstream
Cheng-I Wu academic-research-skills suite does not include use-coherence
verification.

## Why this layer

Wu's `integrity_verification_agent` covers the 5-type Ansari taxonomy
(TF/PAC/IH/PH/SH — fabricated refs, partially attributable claims,
identical hallucinations, paraphrasing hallucinations, source
hallucinations). His own self-audit on the v3.6.5 showcase paper
documented a **31% post-publication error rate** despite three rounds of
automated integrity checking. The errors that survived are the ones his
taxonomy doesn't cover: real sources used in misleading ways.

The `citation_coherence_verifier_agent` here is built on the CiteAudit
pattern (arXiv 2602.23452) — a 5-stage pipeline (claim extraction →
source retrieval → passage matching → reasoning → calibrated judgment) —
extended with a lazy ArticleProfile cache that makes verification
tractable across long manuscripts (and amortizes across multiple
manuscripts that cite the same paper).

## How it composes with Wu's existing layers

Three layers run at Stages 2.5 / 4.5, **in parallel**, each emitting
independent verdicts:

| Layer | Source | Catches |
|-------|--------|---------|
| 5-type Ansari | upstream `integrity_verification_agent` | Fabricated refs, hallucinated content, paraphrasing drift |
| PRISMA-trAIce + RAISE | upstream `compliance_agent` (v3.4+) | Methodological compliance (SR-only) |
| EQUATOR reporting | `manuscript-guidelines` (Phase 2) | Reporting-checklist completeness per design |
| **Use coherence (Type 6)** | **this skill (Phase F)** | **Overreach, misrepresentation, caveat omission, cross-section inconsistency** |

The four layers do not overlap. Block semantics combine via OR — Stage
4.5 advancement requires PASS on all four. The 3-round override ladder
(`shared/compliance_checkpoint_protocol.md`) applies to Schema 15
critical blocks the same way it applies to Schemas 5 / 12 / 14.

## Architecture (three layers internal to this skill)

```
LAYER 1 — FactCard (one per claim)
   shared/fact_card_schema.yaml
   Produced by section writers; consumed here.
   New fields vs v1: use_intent, source_study_design, parent_profile_id.

LAYER 2 — ArticleProfile (one per cited paper, LAZY)
   shared/article_profile_schema.yaml
   Built on first citation, enriched incrementally.
   Storage: ~/.manuscript-agents/profiles/{slugified-doi}.yaml
            (project-local override at ./working/profiles/)
   Persists across manuscripts.

LAYER 3 — citation_coherence_verifier_agent (this skill's only agent)
   manuscript-citations/agents/citation_coherence_verifier_agent.md
   Cache-aware (Profile-first). Two modes:
     - per_citation (Stage 2.5 + 4.5): grades each FactCard.
     - cross_section (Stage 4.5 only): grades multi-cited papers
       for rhetorical-direction consistency.
```

## Modes

| Mode | When | What it produces |
|------|------|------------------|
| `per_citation` | Stage 2.5 (pre-review), Stage 4.5 (post-revision) | One verdict per FactCard: `VERIFIED \| OVERREACH \| MISREP \| CAVEAT_OMITTED \| 2ND_STAGE` |
| `cross_section` | Stage 4.5 only | One verdict per multi-cited paper: `CONSISTENT \| INCONSISTENT`. Groups FactCards by `parent_profile_id` × `source_claim_region` before evaluating rhetorical direction. |

Both modes emit Schema 15 (Citation Coherence Report) — see
`shared/handoff_schemas.md`.

## Verdict semantics

### per_citation

| Verdict | Meaning |
|---------|---------|
| `VERIFIED` | The verbatim quote supports the manuscript-side claim in the direction declared by `use_intent`. |
| `OVERREACH` | The quote partially supports the claim, but the claim makes a stronger or broader assertion than the quote licenses. |
| `MISREP` | The quote contradicts the use_intent (e.g., manuscript says "supports" but source actually refutes). |
| `CAVEAT_OMITTED` | The quote supports the claim, but the source paper attaches a material caveat the manuscript ignores. |
| `2ND_STAGE` | Verifier needs additional context (more of the source paper) before issuing a verdict. Triggers an on-demand fetch + Profile enrichment, then re-grade. |

### cross_section

| Verdict | Meaning |
|---------|---------|
| `CONSISTENT` | All FactCards anchored to the same source-claim region use the source in mutually compatible directions. Different `use_intent` values across regions are fine. |
| `INCONSISTENT` | Two failure shapes: (a) same source-claim region cited in opposite manuscript-side directions; (b) selective heterogeneity — manuscript anchors to favorable subset of source in one section and unfavorable subset in another without acknowledging the source's own heterogeneity. |

## When `cross_section` is and isn't appropriate

Multiple `use_intent` values for one source paper are **normal and
legitimate** when they target different aspects of the source. Example:
a meta-analysis cited in Introduction to support feasibility (`provides_supporting_evidence`,
anchored to pooled response rate) AND in Discussion to identify a gap
(`identifies_gap`, anchored to a section where the source notes long-term
follow-up is sparse). Two FactCards, two distinct `source_claim_region`
values, no INCONSISTENT.

The check fires only when the SAME `source_claim_region` is being used
in incompatible directions. This nuance is encoded in
`citation_coherence_verifier_agent.md` (cross_section step) and
illustrated in `examples/coherence_report_example.md`.

## Quality standards

1. ⚠️ **IRON RULE**: Every verdict must cite a verbatim passage from the
   source (matched against the FactCard's `verbatim_quote`) or a quoted
   absence anchored to a specific source location. No bare verdicts.
2. ⚠️ **IRON RULE**: The verifier never modifies a FactCard's `claim`
   or `verbatim_quote`. It only emits verdicts and writes to the Profile.
3. ⚠️ **IRON RULE**: ArticleProfile writes are append-only. Existing
   entries in `known_findings` / `caveats_encountered` / `usage_log` /
   `author_stated_limitations` may be added to but never removed or
   reordered.
4. The verifier is cache-aware: at invocation, check Profile first; only
   fetch new source content for sections not yet in `sections_processed`
   or when `completeness < 0.7`.
5. `cross_section` mode runs ONLY at Stage 4.5. Running at 2.5 produces
   noisy false positives because revision is expected to consolidate
   citations.

## Anti-patterns

| # | Anti-pattern | Why it fails | Correct |
|---|--------------|--------------|---------|
| 1 | Flagging INCONSISTENT on different use_intents alone | Most multi-cited papers have legitimate multi-use | Group by `(parent_profile_id, source_claim_region)` first; only flag within-group conflicts |
| 2 | Generating "fixes" for the manuscript | Verifier is read-only by design | Emit recommendations only |
| 3 | Re-fetching every section every run | Defeats the lazy cache | Use Profile.sections_processed + completeness ≥ threshold to skip |
| 4 | Overwriting ArticleProfile fields | Breaks the append-only invariant | Use add operations only; user_annotations are user-only |
| 5 | Running cross_section at Stage 2.5 | Pre-revision multi-cite patterns are noisy | cross_section is Stage 4.5 only |
| 6 | Treating CAVEAT_OMITTED as minor in all cases | Severity depends on the caveat | Use the Profile's caveats_encountered.severity_when_omitted field |

## Agent files

| Agent | File |
|-------|------|
| citation_coherence_verifier_agent | `agents/citation_coherence_verifier_agent.md` |

## Reference files

| Reference | Purpose |
|-----------|---------|
| `references/citeaudit_pattern.md` | 5-stage pipeline detail (claim extraction → retrieval → matching → reasoning → judgment) |
| `references/profile_storage.md` | Storage protocol: slugification, locking, project-local override, append-only writeback |

## Examples

| Example | Demonstrates |
|---------|--------------|
| `examples/article_profile_example.yaml` | Realistic Profile shape (hypothetical OCD-DBS meta-analysis) |
| `examples/coherence_report_example.md` | Schema 15 with per_citation + cross_section blocks, including one INCONSISTENT case |

## Output language

Follows user input. Verdict labels (`VERIFIED`, `OVERREACH`, etc.) stay
in English (canonical CiteAudit / Ansari vocabulary).

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 0.1.0 |
| Last Updated | 2026-04-30 |
| Maintainer | Gonzague de France |
| License | CC-BY-NC 4.0 (inherited from upstream) |
| Origin | Original to manuscript-agents v2.0 fork (Phase 3.1) |

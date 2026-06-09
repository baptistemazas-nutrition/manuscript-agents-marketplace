# CiteAudit pattern — 5-stage citation verification pipeline

Reference document for `citation_coherence_verifier_agent.md`. Specifies
the per-stage I/O contract, retrieval cost accounting, and the
verdict-decision matrix.

Source: Janse van Rensburg, *zero-assumption citation verification*
(arXiv 2511.04683, 2025); CiteAudit (arXiv 2602.23452, Feb 2026).
Adapted for the lazy ArticleProfile cache architecture (BUILD_PLAN
extension B).

## Stage map

```
FactCard
   |
   v
[Stage 1 — Claim extraction]
   |   schema-validates the card; extracts (claim, use_intent, quote, doi)
   v
[Stage 2 — Source retrieval] <-- ArticleProfile cache (read; write on miss)
   |   Profile-first; fetch only on cache miss or completeness < 0.7
   v
[Stage 3 — Passage matching]
   |   whitespace-normalized substring match; locate quote in source
   v
[Stage 4 — Reasoning]
   |   evaluate quote+context against claim+use_intent
   v
[Stage 5 — Calibrated judgment]
   |   emit verdict; write back to Profile (append-only)
   v
Schema 15 entry
```

## Per-stage contract

### Stage 1 — Claim extraction

| Field | Type | Notes |
|-------|------|-------|
| input | FactCard | Per `shared/fact_card_schema.yaml` |
| validation | "schema_required" check | If a required field is missing → `HANDOFF_INCOMPLETE` for this card |
| output.claim | string | The manuscript-side claim |
| output.use_intent | enum | From the FactCard |
| output.verbatim_quote | string | From the FactCard |
| output.doi | string | From the FactCard |
| output.factcard_locator | object | Where in the manuscript |
| failure_modes | `HANDOFF_INCOMPLETE`, `MALFORMED_CARD` | Surface in report; continue with next card |

### Stage 2 — Source retrieval (cache-first)

| Field | Type | Notes |
|-------|------|-------|
| input | (doi, verbatim_quote, source_locator) | From Stage 1 |
| step_2a | Profile lookup at `./working/profiles/{slug}.yaml` (project-local override) then `~/.manuscript-agents/profiles/{slug}.yaml` (user-global) | Slugification per `profile_storage.md` |
| step_2b | Cache-hit eligibility check | Hit iff Profile exists AND `completeness ≥ 0.7` AND quote-section in `sections_processed` |
| step_2c | On miss: fetch source paper section | Targeted fetch via `source_locator`; PubMed / S2 / publisher API per source DOI prefix |
| step_2d | On materialization: write Profile updates | Append `sections_processed`; populate `canonical_metadata` if null; bump `completeness` |
| step_2e | parent_profile_id back-reference | If the FactCard's `parent_profile_id` was null, set to Profile.id and emit a `factcard_update_event` |
| output | source_content (cached or freshly fetched) | Sufficient context for Stage 3 |
| failure_modes | `SOURCE_INACCESSIBLE` (paywall / retracted), `PROFILE_LOCKED`, `PROFILE_CACHE_CORRUPT` | See agent's failure-paths table |

**Retrieval cost note.** A naive 1-fetch-per-citation strategy on a
manuscript with N citations costs N fetches. With the cache, the cost
becomes:
- N_papers (distinct DOIs) on first manuscript using each paper, plus
- 0 fetches on subsequent citations of the same paper within the same
  manuscript (cache reads), plus
- 0–small fetches on subsequent manuscripts citing the same papers
  (cache reads, possibly with completeness top-ups).

For a typical biomedical manuscript citing ~50 papers with ~120
FactCards, expect ~50 fetches first run, ~5 fetches second run on a
similar topic.

### Stage 3 — Passage matching

| Field | Type | Notes |
|-------|------|-------|
| input | (verbatim_quote, source_content) | |
| algorithm | Whitespace-normalized substring match | `re.sub(r'\s+', ' ', x).strip()` on both sides |
| fuzzy_fallback | None at v0.1 | Future: PDF extraction can introduce hyphenation/ligature drift; consider Levenshtein-1 fuzzy match in v0.2 if false-MISREP rate is high |
| output_on_match | (location, surrounding_context_excerpt) | ±2 paragraphs around match |
| output_on_miss | None | Treat as `MISREP` with rationale "verbatim quote not located"; SKIP Stage 4/5 reasoning for this card |
| failure_modes | `QUOTE_NOT_FOUND` | Surfaces as `MISREP` verdict |

### Stage 4 — Reasoning

| Field | Type | Notes |
|-------|------|-------|
| input | (claim, use_intent, verbatim_quote, surrounding_context) | |
| evaluation_axis_1 | Does the quote support the claim? | Direct entailment from quote text |
| evaluation_axis_2 | Does the use_intent match the support direction? | A "supports" use_intent on a refuting quote → `MISREP` |
| evaluation_axis_3 | Does the surrounding context attach material caveats the claim ignores? | If yes → `CAVEAT_OMITTED` |
| evaluation_axis_4 | Is the claim a strict superset of what the quote licenses? | If the claim quantifies more strongly than the quote → `OVERREACH` |
| evaluation_axis_5 | Is more context needed for a confident verdict? | If yes → `2ND_STAGE` (returns to Stage 2 for an expanded fetch) |
| convergence_cap | Max 2 `2ND_STAGE` re-fetches per FactCard | After the second, emit `2ND_STAGE` with `unresolvable: true` |
| output | (verdict, reasoning) | Verdict from {VERIFIED, OVERREACH, MISREP, CAVEAT_OMITTED, 2ND_STAGE} |

### Stage 5 — Calibrated judgment

| Field | Type | Notes |
|-------|------|-------|
| input | (verdict, reasoning, FactCard, Profile) | |
| severity_assignment | Per the agent's severity-defaults table | OVERREACH → major; MISREP → critical; CAVEAT_OMITTED → severity from Profile.caveats_encountered |
| profile_writeback | Append `usage_log[]`, `known_findings[]` (if new region), `caveats_encountered[]` (if caveat surfaced); update `last_verified` | Append-only; never overwrite |
| output | Schema 15 per_citation entry | See SKILL.md for shape |

## Decision matrix (Stage 4 → verdict)

| Quote supports claim? | use_intent direction match? | Caveats attached? | Strict superset? | Verdict |
|----------------------|----------------------------|-------------------|------------------|---------|
| Yes | Yes | No | No | `VERIFIED` |
| Yes | Yes | Yes (material) | No | `CAVEAT_OMITTED` |
| Partial | Yes | n/a | Yes | `OVERREACH` |
| No (contradicts) | n/a | n/a | n/a | `MISREP` |
| Inconclusive | n/a | n/a | n/a | `2ND_STAGE` |

Edge case: quote NOT located in source → `MISREP` regardless of other axes.

## Profile updates per verdict

| Verdict | Profile additions |
|---------|-------------------|
| `VERIFIED` | usage_log entry; known_findings entry if new region |
| `OVERREACH` | usage_log entry; known_findings entry if new region |
| `MISREP` | usage_log entry; (no known_findings — quote was not actually grounded) |
| `CAVEAT_OMITTED` | usage_log entry; known_findings entry; **caveats_encountered entry** with `severity_when_omitted` |
| `2ND_STAGE (final, unresolvable)` | usage_log entry with `unresolvable: true`; sections_processed updated for any sections fetched during the attempt |

## Determinism notes

The verbatim-quote requirement strongly constrains LLM stochasticity:
- Stage 1 / 3: deterministic by construction (schema check + substring match).
- Stage 4: LLM judgment, but anchored to a fixed quote + fixed context. Verdict variance across reruns should be < 5% on `MISREP` and `VERIFIED` (the easy cases) and may approach 15% on `OVERREACH` vs `VERIFIED` borderlines and `CAVEAT_OMITTED` borderline cases.
- Stage 5: deterministic mapping from Stage 4.

For calibration (deferred to Phase 3.5 or 7), repeat-runs on the same
FactCard against the same Profile state should be the determinism
benchmark.

## See also

- `manuscript-citations/agents/citation_coherence_verifier_agent.md` — operational contract
- `manuscript-citations/references/profile_storage.md` — cache layer
- `shared/fact_card_schema.yaml` — input schema
- `shared/article_profile_schema.yaml` — cache schema
- `shared/handoff_schemas.md` — Schema 15 output schema

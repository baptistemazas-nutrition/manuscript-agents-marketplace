# Pipeline Integration — Stage 0 (DATA → RESULTS)

## Where this skill sits
manuscript-statistics is **Stage 0** of academic-pipeline. When the user provides raw data (CSV/Excel) and intends to write a paper, run here first; results then feed Stage 2 (WRITE).

```
Stage 0 DATA→RESULTS (manuscript-statistics)
   └─> StatsResults handoff
Stage 1 RESEARCH (deep-research)            # optional / parallel: framing + literature
Stage 2 WRITE (academic-paper)             # consumes StatsResults for Methods/Results/Tables/Figures
Stage 2.5 INTEGRITY  ... (unchanged)
```

The pipeline's `integrity_verification_agent` (Stage 2.5/4.5) additionally verifies that every statistic in the manuscript traces to the StatsResults bundle.

## StatsResults handoff (Schema — manuscript-statistics → academic-paper)
| Field | Type | Description |
|---|---|---|
| `design` | enum | detected design (drives the EQUATOR checklist in manuscript-guidelines) |
| `sap_ref` | string | path to the locked SAP |
| `methods_paragraph` | string | SAMPL-compliant statistical methods text |
| `table_one` | table | descriptive Table 1 (CSV + markdown) |
| `results_tables` | list[table] | estimate tables: term, estimate/OR/HR/IRR, 95% CI, p (raw + adjusted) |
| `figures` | list | {path, caption} for each figure |
| `results_text` | string | Results prose (confirmatory vs exploratory labeled) |
| `effect_summary` | list | primary estimates with CI + exact p |
| `confirmatory_vs_exploratory` | map | which analyses were pre-specified |
| `reproducibility_card` | object | see `reproducibility_card.md` |
| `data_access_level` | enum | `redacted` — handoff carries aggregates, not raw records |

## Consumers
- **academic-paper**: `structure_architect_agent` places Table 1 + results tables/figures; `draft_writer_agent` integrates `methods_paragraph`/`results_text`; `visualization_agent` reuses the figures.
- **manuscript-guidelines**: `paper_type_detector_agent` uses `design` to pick STROBE/CONSORT/TRIPOD+AI/ARRIVE; statistical items map to SAMPL.
- **academic-paper-reviewer**: `methodology_reviewer_agent` checks the analysis against the SAP and assumptions.

## Trigger from the pipeline
The orchestrator detects an attached dataset + writing intent → routes to Stage 0 before WRITE. If the user only wants analysis (no paper), run this skill standalone and stop at the StatsResults bundle.

# Data Access & Privacy

Study datasets often contain identifiable or sensitive information (health, minors, protected attributes). Handle with care (IRON RULE 5).

## Rules
1. **Local-only processing.** Analyze raw records in the sandbox only. **Never** send raw rows, identifiers, or record-level data to web search or any external/3rd-party tool.
2. **De-identify before output.** Outputs (tables, figures, text) contain aggregates, not identifiable records. No small-cell counts that could re-identify (consider suppressing cells with n < 5 in sensitive contexts).
3. **Minimize.** Load only the columns needed. Drop direct identifiers (names, MRNs, exact dates of birth, addresses) at intake; keep a separate key only if the user requires linkage.
4. **No example leakage.** When illustrating, use synthetic or fully de-identified snippets.
5. **Respect governance.** Flag if the analysis appears to need IRB/ethics approval or a data-use agreement; the suite's `ethics_review_agent` (deep-research) and EQUATOR ethics items apply.
6. **data_access_level = raw** for this skill: it is trusted to read raw data but its *handoffs* downstream are de-identified aggregates.

## On request
If the user asks to share or upload record-level data externally, decline and offer a de-identified aggregate or a local-only alternative.

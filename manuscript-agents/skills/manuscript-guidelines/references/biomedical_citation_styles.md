# Biomedical citation styles — reference

Default citation style for the manuscript-agents v2.0 fork is
**Vancouver**, with journal-specific overrides for the biomedical
journals the user is most likely to target.

Wu's existing `academic-paper/agents/formatter_agent.md` already
supports Vancouver natively (it is in the conversion table at
academic-paper/agents/formatter_agent.md, line 141 region) and can
convert to/from APA 7, Chicago, MLA 9, IEEE, and Vancouver. This
reference does not modify the formatter; it documents the mapping
from biomedical journal to citation-style choice so the user can
specify the right format-convert target.

## Default for biomedical manuscripts

**Vancouver** is the default. Rationale:

- Numbered references (superscript or in-text bracket) match almost all
  biomedical journals' conventions.
- Author abbreviation rules (Last FM) match NLM citation format that
  PubMed already produces.
- Numbered reference list orders by appearance in the manuscript, not
  alphabetically — easier to track during revision.

## Per-journal overrides

Most biomedical journals are Vancouver-derivatives with subtle
differences. Use the table below to select the target style when
running the formatter agent in `format-convert` mode.

| Journal | Closest formatter style | Notes |
|---------|--------------------------|-------|
| **Brain Stimulation** (Elsevier) | Vancouver | Author limit "et al." after 6; numbered references; DOIs required. Standard Vancouver. |
| **Neurosurgery** (Wolters Kluwer) | Vancouver | "et al." after 6 authors; DOIs in references; superscript numbers in text. Standard Vancouver. |
| **Journal of Neurosurgery** (AANS) | Vancouver | List all authors when ≤ 6, then et al.; DOIs required; PMIDs accepted. Vancouver-compatible. |
| **JAMA Neurology** (JAMA Network) | AMA (variant of Vancouver) | List all authors regardless of count; numbered superscripts; specific punctuation rules. Closest formatter target = Vancouver; then apply AMA-specific corrections (author list, journal abbreviation per Index Medicus). |
| **Movement Disorders** (Wiley) | Vancouver | Numbered; up to 7 authors then et al.; DOI required. |
| **Annals of Neurology** (ACNS / Wiley) | Vancouver | Up to 6 authors; specific abbreviations. Standard Vancouver. |
| **NeuroImage** (Elsevier) | Author-Date (Harvard / Elsevier) | NOT Vancouver. Closer to APA 7 or Elsevier Author-Date. Run formatter in APA 7 mode and then journal-style-specific tweaks. |
| **eLife** | Author-Date | NOT Vancouver. Closer to APA 7. |
| **PLoS journals** | Vancouver | Numbered references; minimal differences from canonical Vancouver. |
| **Nature Medicine / Nature Neuroscience** | Nature (variant) | Superscript numbered references; specific Nature reference style. Closest = Vancouver, then apply Nature-specific abbreviations and author-list rules. |
| **Brain (Oxford)** | Vancouver | List up to 6 authors; specific journal abbreviation conventions. Standard Vancouver. |

## How to apply

When the user invokes `academic-paper format-convert` mode:

1. **Default**: target style = Vancouver. Use this when no journal is
   yet selected, or when the journal is in the Vancouver column above.
2. **AMA target** (JAMA Neurology, etc.): target = Vancouver, then
   manually verify per-author full-list and journal abbreviation rules.
   The formatter does not currently produce AMA verbatim; this is a
   known limitation documented here rather than a bug.
3. **Author-date target** (NeuroImage, eLife): target = APA 7 (closest
   formatter-supported style), then apply journal-specific tweaks.
4. **Nature variants**: target = Vancouver as the base, then apply
   Nature-specific reference list formatting per the journal's
   instructions to authors.

## What this fork does NOT change

- The formatter agent's internal style implementations (apa7 LaTeX class,
  IEEE, Chicago, etc.) are unchanged.
- The formatter's bidirectional conversion table is unchanged.
- LaTeX class selection (apa7 / IEEE / etc.) is unchanged. Vancouver in
  LaTeX is implemented per Wu's existing approach (typically biblatex
  with `style=numeric-comp` or natbib).

## When the user wants AMA-perfect output

For now, the recommendation is:

1. Generate Vancouver from the formatter.
2. Manually apply AMA-specific corrections at the proof stage:
   - Convert "Last FM, Last GH, Last IJ. ..." (Vancouver up to 6) to the
     full author list (AMA).
   - Verify journal abbreviations match the AMA Manual of Style
     (Index Medicus abbreviations, no periods).
   - Verify punctuation matches AMA's specific rules.

A future phase MAY add an `ama` style to the formatter. That is out of
scope for v0.1 of the fork.

## When the user wants Author-Date (NeuroImage / eLife)

Generate APA 7 from the formatter, then apply journal-specific tweaks
(typically: minor punctuation, journal name abbreviation rules).

## See also

- `academic-paper/agents/formatter_agent.md` — citation-style conversion
  matrix and per-style implementation details.
- `academic-paper/references/anti_leakage_protocol.md` — every reference
  in the bibliography must be backed by a FactCard; the formatter does
  not invent references.

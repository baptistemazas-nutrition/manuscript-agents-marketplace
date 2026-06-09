# Manuscript Agents — plugin marketplace

A shared **Claude plugin marketplace** for `manuscript-agents`: an end-to-end suite of 8 skills that takes a researcher from question to published scientific paper. Hosting it as a marketplace (git repo) lets a team **install the same plugin and each improve it**, with version tracking and updates.

## What's inside

`manuscript-agents/` (the plugin, v2.5.0) — 8 skills:

| Skill | Role |
|---|---|
| `manuscript-statistics` | Autonomous statistical analysis of a dataset (CSV/Excel) with a bundled Python engine |
| `deep-research` | Question framing, systematic literature search, synthesis, meta-analysis |
| `manuscript-guidelines` | EQUATOR reporting checklists (CONSORT/STROBE/PRISMA/CARE/ARRIVE/TRIPOD/SRQR/SQUIRE) |
| `academic-paper` | Writing pipeline: outline, draft, abstract, style, plus discoverability/English/citation-style references |
| `manuscript-citations` | Source–claim citation coherence |
| `academic-paper-reviewer` | Simulated multi-perspective peer review |
| `academic-pipeline` | End-to-end orchestrator (research → write → integrity → review → revise → finalize) |
| `journal-submission` | Journal selection, cover letter, response to reviewers, submission checklist, open science, publication ethics |

## Add this marketplace in Claude Cowork

1. Open **Customize** (left sidebar) → **Plugins** tab.
2. In **Personal plugins**, click **“+”** → **“Add marketplace”** → **“Add from a repository”**.
3. Paste the GitHub repo (e.g. `your-org/manuscript-agents-marketplace` or the git URL).
4. Open the **Manuscript Agents** plugin and click **Install**.

To get later improvements: in the same Plugins screen, **update the marketplace**, then reinstall/upgrade the plugin.

> Claude Code CLI equivalent: `/plugin marketplace add your-org/manuscript-agents-marketplace`, then `/plugin`.

## Use it

Ask in natural language — the matching skill triggers. Examples:
- “analyse mes données” (CSV/Excel) → `manuscript-statistics`
- “lance le pipeline complet pour un article sur …” → `academic-pipeline`
- “où publier cet article / écris la lettre de soumission” → `journal-submission`

See `manuscript-agents/skills/journal-submission/references/researcher_workflow_map.md` for the full map.

## Improve it together

Each person can tweak their own installed copy, **and** share improvements back via pull request. See **[CONTRIBUTING.md](CONTRIBUTING.md)** — please read the *Validation rules* there before submitting (a few formatting rules keep the plugin installable).

## Provenance & license

Derived from **Academic Research Skills (ARS)**, licensed **CC BY-NC 4.0** — non-commercial use, with attribution. The `journal-submission` skill and the 360° references are additions in this fork.

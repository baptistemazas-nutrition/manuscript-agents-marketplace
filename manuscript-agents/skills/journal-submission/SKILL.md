---
name: journal-submission
description: "Guides a manuscript from finished draft to publication and beyond - the step most writing tools skip. Covers target-journal selection (scope/fit, impact, open-access, predatory-journal screening), formatting to author guidelines, the cover letter, suggested/excluded reviewers, the submission checklist (CRediT, conflicts, funding, ethics, data/code availability, ORCID, reporting checklist), point-by-point response to reviewers and rebuttals, revision strategy, appeals, proofs, and post-publication promotion. Triggers on: submit my paper, where should I publish, choose a journal, journal selection, target journal, cover letter, response to reviewers, rebuttal, reviewer response, revise and resubmit, R&R, suggested reviewers, predatory journal, open access, APC, data availability statement, ORCID, proofs, soumettre mon article, choisir une revue, lettre de soumission, reponse aux relecteurs, ou publier."
---

# Journal Submission & Publishing — From Final Draft to Published Paper

The blind spot most writing assistants ignore: getting a finished manuscript accepted and published. This skill manages the whole submission→publication→post-publication journey.

## When this triggers
After a draft exists (often from `academic-paper`) and the researcher asks where/how to publish, how to write the cover letter, how to answer reviewers, or how to handle revisions and proofs.

## Modes
| Mode | For | Produces |
|---|---|---|
| `select-journal` | "where should I publish this?" | Ranked shortlist of fit journals with rationale, scope match, OA/APC, speed, and a predatory-journal screen |
| `prepare-submission` | "get this ready to submit" | Author-guideline conformance pass + the full submission checklist + cover letter + suggested/excluded reviewers |
| `cover-letter` | just the letter | Tailored cover letter (editor, significance, fit, declarations) |
| `respond-reviewers` | "help me answer the reviewers" | Point-by-point response + revised-manuscript change map + rebuttal for unfair critiques |
| `appeal` | rejected unfairly | Reasoned, respectful appeal letter |
| `post-acceptance` | accepted | Proof-checking pass, license/OA choice, promotion plan (ORCID, preprint link, social, repository deposit) |

## Workflow
1. **Detect the stage** (pre-submission / under review / revision / accepted) and load the matching mode.
2. **Journal fit before everything** (`references/journal_selection.md`): match scope, audience, article type, and length; weigh impact vs. speed vs. open-access cost; **screen for predatory journals** (a hard gate). Never recommend a venue without the predatory screen.
3. **Conform to author guidelines**: structure, word/figure limits, reference style, required statements.
4. **Assemble the back matter** (`references/submission_checklist.md`): CRediT author contributions, conflicts of interest, funding, ethics/IRB, **data and code availability**, ORCID, and the design-appropriate reporting checklist (hand off to `manuscript-guidelines`).
5. **Cover letter** (`references/cover_letter.md`).
6. **Reviewer response** when revising (`references/response_to_reviewers.md`): answer every point, show the change and where it is, concede gracefully, and rebut unfair points with evidence — never dismissively.
7. **Post-acceptance** (`references/post_acceptance.md`): proofs, licensing/OA, preprint, promotion.

## IRON RULES
1. **Predatory-journal screen is mandatory** before recommending any venue (`references/journal_selection.md`). Flag pay-to-publish-with-no-real-review, fake metrics, and aggressive solicitation.
2. **Honesty in the cover letter and responses.** Never overstate novelty, fabricate fit, or misrepresent what changed. Every "we have revised X" must correspond to a real change.
3. **Answer every reviewer point** — none skipped — and locate each change in the revised manuscript.
4. **No authorship or citation manipulation.** No gift/ghost authorship, no coercive citation, no fake/suggested-reviewer fraud.
5. **Respect each journal's policies** on preprints, dual submission (never submit to two journals at once), and AI-use disclosure.

## Integration
- Consumes a draft from `academic-paper`; the reporting checklist from `manuscript-guidelines`; statistical reproducibility from `manuscript-statistics`.
- Hands a publication-ready package back to the user; revision requests route back to `academic-paper` (revision mode).

## References
- `references/journal_selection.md` — fit, metrics, OA/APC, speed, predatory screen
- `references/cover_letter.md` — structure + what editors look for
- `references/response_to_reviewers.md` — point-by-point craft, concession vs. rebuttal
- `references/submission_checklist.md` — the complete pre-submission back matter
- `references/open_science_and_reproducibility.md` — data/code availability, preprints, OSF, FAIR, licenses
- `references/publication_ethics_cope.md` — authorship, plagiarism, duplicate/salami, image integrity, conflicts (COPE)
- `references/post_acceptance.md` — proofs, licensing, promotion, corrections
- `references/researcher_workflow_map.md` — the end-to-end map of the whole suite (where every step lives)

## Templates
- `templates/cover_letter_template.md`
- `templates/response_to_reviewers_template.md`

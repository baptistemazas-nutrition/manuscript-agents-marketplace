# Clinical case report (CARE 2017) — manuscript template

A skeleton case-report template aligned 1:1 with the 13 CARE items.
Each section header includes (a) the CARE item number, (b) which card
types typically anchor content there, (c) example named tools / sources
where relevant. The author or `draft_writer_agent` fills the prose; the
anchoring requirements are explicit.

> **Anchoring vocabulary.** Every factual claim must trace to one of:
> FactCard (literature, `shared/fact_card_schema.yaml`),
> DataCard (own-experiment data, `shared/data_card_schema.yaml`), or
> MethodCard (own procedure, `shared/method_card_schema.yaml`).
> See `academic-paper/references/anti_leakage_protocol.md` (DataCard /
> MethodCard discipline section) for the IRON RULE on quantitative claims.

---

## Title (CARE Item 1)

`[Words "case report" + principal diagnosis or intervention]`

Anchors expected: none (titles do not require a card).

---

## Key Words (CARE Item 2)

2–5 keywords including "case report".

---

## Abstract (CARE Item 3)

Structured, four elements:

- **Introduction** — context, why this case matters.
- **Main symptoms / clinical findings** — the presenting picture.
- **Main diagnoses, interventions, outcomes** — what we did and the result.
- **Conclusions** — take-away.

Anchors expected: at least one DataCard for the headline outcome value
(e.g., Y-BOCS reduction percentage); FactCards for any literature cited.

---

## Introduction (CARE Item 4)

- Background of the case (why this case is being reported).
- Brief summary of relevant medical literature.

Anchors expected: FactCards for every cited paper. The
`citation_coherence_verifier_agent` (Phase F) grades each FactCard's
`use_intent` against the verbatim quote in the cited paper.

---

## Patient Information (CARE Item 5)

- De-identified demographics (age range, sex, ethnicity / occupation if
  relevant — never specific dates of birth, never PHI).
- Primary concerns and symptoms.
- Medical, family, and psychosocial history (relevant past interventions,
  outcomes).

Anchors expected: DataCards (`source_type: clinical_record`) for each
documented symptom, history element, or prior intervention. PHI MUST
NOT appear in the manuscript or the DataCard's `verbatim_anchor`.

---

## Clinical Findings (CARE Item 6)

Description of significant physical examination findings and important
clinical assessments. For DBS / neurosurgery cases, include:

- Pre-operative neurological exam findings.
- Pre-operative neuropsychological scores (with instrument names).
- Pre-operative imaging findings.

Anchors expected: DataCards (`source_type: patient_reported_outcome` for
PROs, `clinical_record` for exam findings, `imaging_quantification` for
quantitative imaging).

---

## Timeline (CARE Item 7)

Table or figure of relevant events with dates. For DBS cases:

| Event | Date (de-identified to month/year) |
|-------|-----------------------------------|
| First specialist consultation | YYYY-MM |
| MRI for surgical planning | YYYY-MM |
| Bilateral STN-DBS implantation | YYYY-MM |
| Initial programming session | YYYY-MM |
| 1-month follow-up | YYYY-MM |
| 6-month follow-up | YYYY-MM |
| 12-month follow-up | YYYY-MM |

Anchors expected: DataCards for each row's date AND outcome data.

---

## Diagnostic Assessment (CARE Item 8)

- Diagnostic methods (clinical exam, structured interview, lab, imaging,
  specific instruments).
- Diagnostic challenges (differential considered, exclusions reasoned).
- Diagnostic reasoning including alternatives.
- Prognostic characteristics where applicable.

Anchors expected: MethodCards for any diagnostic instrument (`tool_name:
"DSM-5 SCID"` or similar); DataCards for each diagnostic data point.

---

## Therapeutic Intervention (CARE Item 9)

- Type of intervention(s).
- Administration (dosage, strength, duration, frequency; for DBS:
  electrode model, implant target coordinates, programming parameters
  per contact).
- Changes in intervention(s) with rationale.

Anchors expected: **MethodCard for the surgical protocol** (with
tool_versions for: surgical planning software, atlas used for target
selection, intra-operative recording system if applicable).
**DataCards for each programming parameter change** (`source_type:
device_log`, with tool_version of the programmer software).

For DBS specifically, name explicitly: electrode manufacturer + model;
implantable pulse generator model; programmer software version.

---

## Follow-up and Outcomes (CARE Item 10)

- Clinician-assessed outcomes.
- Patient-assessed outcomes (PROs).
- Important follow-up diagnostic and other test results.
- Intervention adherence and tolerability (with how this was assessed).
- Adverse and unanticipated events (or explicit "no AEs").

Anchors expected: DataCards (`source_type: patient_reported_outcome` for
each PRO timepoint, `clinical_record` for clinician outcomes,
`imaging_quantification` for follow-up imaging). Include the assessment
instrument name in each DataCard's verbatim_anchor.

---

## Discussion (CARE Item 11)

- Strengths and limitations of this approach to the case.
- Discussion of related literature (with attention to evidence
  hierarchy: meta-analyses > RCTs > cohort > case reports > expert
  opinion).
- Rationale for conclusions (incl. assessment of cause and effect).
- Main "take-away" lessons.

Anchors expected: FactCards for every cited paper. Use_intent variety is
expected (some literature `provides_supporting_evidence`, some
`contrasts_with`, some `identifies_gap`). The
`citation_coherence_verifier_agent` cross_section mode at Stage 4.5
checks that papers cited multiple times across this section + others
(e.g., Introduction) are used consistently.

---

## Patient Perspective (CARE Item 12)

The patient's (or family's) perspective on the experience, when
applicable. Obtain consent for any quoted material.

Anchors expected: DataCard (`source_type: clinical_record` or `other`
with `source_type_other: "patient interview transcript"`) with the
verbatim quote and consent timestamp.

---

## Informed Consent (CARE Item 13)

Explicit statement that informed consent was obtained from the patient
(or legal guardian) for publication.

Anchors expected: DataCard (`source_type: protocol`, pointing to the
signed consent document with date).

---

## Acknowledgments / Funding / Conflicts of interest

Standard sections. No card anchors required.

---

## Tool / pipeline vocabulary used in this template

When DBS / connectomic content appears in this case report, the Methods
sections MUST name the specific tool versions used. Example vocabulary
(replace with actuals at write time):

- Surgical planning: e.g., StealthStation S8 v3.1, Brainlab Elements.
- Electrode reconstruction: Lead-DBS v3.0.1.
- Subcortical atlas: DISTAL atlas v2.0 (Ewert et al., 2018) — also a FactCard.
- Activation modeling: OSS-DBSv2 with McNeal axon model.
- Tractography pipeline: e.g., FSL 6.0, MRtrix3 3.0.4, ANTs 2.4.
- T1 / FreeSurfer pipeline: FreeSurfer 7.4.0 with `recon-all -all`.

Each named tool requires a MethodCard with the version recorded.

---

## See also

- `manuscript-guidelines/checklists/care_2017.md` — verifier checklist
  this template aligns with.
- `manuscript-guidelines/templates/DBS_connectomic_study.md` — when the
  case report includes substantial connectomic / tractographic content.
- `academic-paper/references/anti_leakage_protocol.md` — DataCard /
  MethodCard discipline section.

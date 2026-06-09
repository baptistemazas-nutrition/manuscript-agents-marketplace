# DBS connectomic study — manuscript template

Template for studies combining DBS clinical outcomes with connectomic
imaging analysis (tractography, structural connectivity, normative
connectomes, activation modeling). Composes with CARE (for case-report
flavor), STROBE (for cohort flavor), or stands alone for purely
methodological / connectomic-focused papers.

> **Anchoring discipline.** Methods sections in connectomic studies are
> dense with named tools and atlases. Every named entity needs a
> MethodCard (`shared/method_card_schema.yaml`) with `tool_versions[]`.
> The anti-leakage protocol's IRON RULE (clause 3) treats unannotated
> tool names as `[METHOD GAP — no protocol]`.

---

## Required tool / atlas / model vocabulary

Methods sections in this template typically name:

| Domain | Canonical names | Versioned |
|--------|-----------------|-----------|
| Electrode localization | Lead-DBS, PaCER, DiODe | always — Lead-DBS major versions differ materially |
| Subcortical atlases | DISTAL, CIT168, Ewert STN, Krauth STN, MNI PD25 | always — atlas versions are non-trivial |
| Cortical parcellations | Desikan-Killiany, Destrieux, Glasser HCP-MMP1 | always |
| Activation modeling | OSS-DBSv2 (McNeal axon, Howell-McIntyre axon), SimNIBS, COMSOL | always |
| Tractography | MRtrix3, FSL probtrackx2, DSI Studio, TrackVis, DIPY | always |
| Surface processing | FreeSurfer (recon-all), HCP minimal preprocessing pipelines | always |
| Volume registration | ANTs (SyN), FSL FLIRT/FNIRT, Greedy, NiftyReg | always |
| Functional preprocessing | fMRIPrep, AFNI afni_proc.py, FSL FEAT | always |
| Normative connectomes | HCP 1200 subjects (group average), PPMI, MGH adult diffusion | always |
| Statistical computing | R (with packages), Python (numpy/scipy/pandas/statsmodels), MATLAB | always |

**Each named entity in any Methods sentence requires a MethodCard
covering it.** A sentence "We localized electrodes with Lead-DBS using
the DISTAL atlas, then computed activations with OSS-DBSv2" requires
THREE MethodCards (or one MethodCard with three `tool_versions[]`
entries).

---

## Title

`[Anatomical target] [intervention type] for [condition]: a [study type]
analysis using [primary connectomic method]`

Examples: "Bilateral anterior STN-DBS for treatment-refractory OCD: a
case report with patient-specific connectomic analysis"; "Pallidal vs.
subthalamic DBS in Parkinson's disease: a probabilistic tractography
comparison".

---

## Abstract

Structured. Connectomic-specific elements that must be present:

- Imaging modality (3T / 7T MRI; sequence — MPRAGE, MP2RAGE, multi-shell
  diffusion).
- Connectomic method (e.g., normative connectome, patient-specific
  tractography, OSS-DBSv2 activation modeling).
- Atlas / parcellation used.
- Statistical approach.

Anchors: MethodCards for named tools; DataCards for any quantitative
result in the abstract (effect sizes, p-values, sample numbers).

---

## Introduction

Standard structure. For connectomic studies, the introduction MUST
situate against:

1. The clinical problem (target condition, intervention rationale).
2. The connectomic hypothesis (which tract / network is implicated;
   prior connectomic evidence).
3. The methodological landscape (atlas-based vs. patient-specific
   tractography; normative vs. own-cohort connectome).

Anchors: FactCards for every literature citation. Phase F's
cross_section verifier checks that papers cited here remain consistently
used in Discussion.

---

## Methods

### Patient(s) and ethics

Cohort or single-case description, IRB/ethics approval (with committee
name + approval number), consent.

Anchors: DataCard (clinical_record) for cohort characteristics; DataCard
(protocol, with verbatim_anchor of the consent document) for ethics.

### Imaging acquisition

For each MRI sequence:

- Scanner make / model / field strength.
- Sequence type (T1 MPRAGE / MP2RAGE / multi-shell DWI / etc.).
- Voxel size, TR / TE / flip angle.
- For DWI: number of directions, b-values, multi-shell or single-shell.

Anchors: MethodCard for the acquisition protocol (`tool_name:
"<scanner model>"`, `version: "<scanner software version>"`,
`configuration: "<sequence parameters>"`).

### Pre-operative planning and surgery

- Stereotactic frame or frameless system used.
- Trajectory planning software (e.g., Brainlab Elements, StealthStation).
- Microelectrode recording (if applicable).
- Final electrode model and lead.

Anchors: MethodCard with each named tool's version.

### Electrode localization

- Localization software (Lead-DBS version; the major version is critical
  — Lead-DBS v2 vs v3 differ in default atlas + registration pipeline).
- Atlas used (DISTAL / CIT168 / etc., with version).
- Manual vs. automated refinement.

Anchors: MethodCard with `tool_name: "Lead-DBS"`, `version: "3.0.1"`,
`configuration: "DISTAL atlas v2.0; manual refinement of contact 1 of
left hemisphere"`. Each electrode contact's coordinates is a DataCard
(`source_type: leaddbs_export`, `source_locator.coordinate: {x, y, z,
space: "MNI152 2009b"}`).

### Activation modeling

If patient-specific activation modeling was performed:

- Modeling tool (OSS-DBSv2 version) and axon model (McNeal vs. Howell-McIntyre).
- Tissue conductivity assumptions.
- Voltage / current settings simulated (matching the actual programming).

Anchors: MethodCard for OSS-DBSv2; DataCards (`source_type: pam_output`)
for each activation map. Each PAM output's DataCard.tool_version
includes the OSS-DBSv2 version AND the axon model.

### Tractography or connectivity analysis

- Pipeline (MRtrix3 + ACT, FSL probtrackx, DSI Studio, etc.).
- Source of streamlines (patient diffusion data vs. normative connectome
  reference). For normative: which dataset (HCP 1200, PPMI, MGH)?
- Region-of-interest definitions (which atlas, which masks).
- Filter / threshold parameters.

Anchors: MethodCard per pipeline. DataCards for any quantitative
connectivity measure (`source_type: leaddbs_export` or
`imaging_quantification`).

### Statistical analysis

Standard. Anchors: MethodCard for the analysis software (R, Python,
MATLAB) with version; DataCards for any reported test statistic.

---

## Results

Per-section anchoring per the analysis plan. Every quantitative claim is
a DataCard. Every effect size / p-value / confidence interval is a
DataCard. Tables and figures should each correspond to a defined set of
DataCards.

For figures showing tractograms, surface renderings, or activation maps:
the figure caption MUST name the rendering tool (Surf Ice, MRtrix3
mrview, custom Python with brain_visualization libraries) and the
parameters used (slice plane, opacity, threshold). MethodCard.

---

## Discussion

Standard structure. Phase F's cross_section verifier is most active in
this section: papers cited multiply across Introduction + Discussion are
checked for rhetorical-direction consistency. The
`source_claim_region` field on each FactCard is critical here for
disambiguating legitimate multi-use from selective heterogeneity
laundering.

---

## Limitations

Connectomic-study-specific limitations to address:

- Atlas vs. patient-specific differences (if normative connectome used).
- Registration accuracy (especially for subcortical structures).
- Activation model assumptions (axon orientation, tissue conductivity).
- Post-hoc programming changes within a follow-up window.

Each limitation should pair with the relevant MethodCard for full
reproducibility receipts.

---

## Funding / conflicts / data and code availability

Standard. The data and code availability section is particularly
important for connectomic studies — readers reproducing the analysis
need access to:

- Anonymized imaging data (if possible).
- Lead-DBS reconstructions (electrode coordinates, atlas alignment).
- Activation maps (PAM outputs).
- Analysis code with environment specifications (Conda / Docker / Apptainer).

---

## See also

- `manuscript-guidelines/checklists/care_2017.md` — when DBS connectomic
  case report.
- `manuscript-guidelines/checklists/strobe.md` — when DBS connectomic
  cohort.
- `manuscript-guidelines/checklists/tripod_ai.md` — when the study
  develops or validates a prediction model from connectomic features.
- `shared/method_card_schema.yaml` — required structure for tool
  declarations.
- `shared/data_card_schema.yaml` — required structure for own data.

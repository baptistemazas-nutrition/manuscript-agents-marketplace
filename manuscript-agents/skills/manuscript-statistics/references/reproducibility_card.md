# Reproducibility Card (schema)

A compact record that lets anyone re-run the analysis and get the same results.

```yaml
reproducibility_card:
  dataset:
    file: "<name>"          # not the raw data itself
    sha256: "<hash>"        # integrity of the input
    n_rows: <int>
    n_vars: <int>
  environment:
    python: "<x.y.z>"
    libraries: { pandas: "...", numpy: "...", scipy: "...", statsmodels: "...",
                 scikit-learn: "...", lifelines: "..." }
  seed: 42
  artifacts:
    script: "analysis.py"
    data_dictionary: "data_dictionary.csv"
    transformations_log: "transformations_log.md"
    sap: "sap.md"
    figures: ["fig1_*.png", "..."]
    tables: ["table1.csv", "..."]
  rerun: "bash bootstrap_env.sh && python analysis.py"
  notes: "exclusions, imputation, deviations from SAP (with dates)"
```

Every StatsResults handoff references a completed card. Aligns with the suite's Material Passport so the pipeline integrity gate can audit it.

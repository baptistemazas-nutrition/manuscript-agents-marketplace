# Reproducibility Card — {study}

- **Dataset**: {file} (sha256 {hash}); n = {rows} × {vars}
- **Environment**: Python {ver}; pandas {v}, numpy {v}, scipy {v}, statsmodels {v}, scikit-learn {v}, lifelines {v}
- **Seed**: {n}
- **Artifacts**: analysis.py · data_dictionary.csv · transformations_log.md · sap.md · versions.json · figures/ · tables/
- **Re-run**: `bash bootstrap_env.sh && python analysis.py`
- **Notes**: {exclusions, imputation, SAP deviations with dates}

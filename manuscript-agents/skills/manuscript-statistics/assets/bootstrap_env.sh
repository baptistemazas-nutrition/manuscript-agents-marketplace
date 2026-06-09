#!/usr/bin/env bash
# Manuscript Statistics — environment bootstrap (run once per session).
# pandas / numpy / matplotlib / seaborn / openpyxl are usually preinstalled.
set -e
pip3 install --break-system-packages --quiet \
  scipy statsmodels scikit-learn lifelines pingouin openpyxl statsmodels >/dev/null 2>&1 || \
pip install --quiet scipy statsmodels scikit-learn lifelines pingouin openpyxl
python3 - <<'PY'
import importlib
mods = ["pandas","numpy","scipy","statsmodels","sklearn","lifelines","pingouin","matplotlib","seaborn","openpyxl"]
print("Environment ready:")
for m in mods:
    try:
        x = importlib.import_module(m)
        print(f"  - {m} {getattr(x,'__version__','?')}")
    except Exception as e:
        print(f"  - {m} MISSING ({e})")
PY

# Python Stats Cookbook — driving `assets/stats_toolkit.py`

Bootstrap once: `bash assets/bootstrap_env.sh`. Then `import stats_toolkit as t; t.set_seed(42)`.

## Load & profile
```python
df = t.load_data("study.xlsx")      # csv/tsv/xlsx auto-detected
prof = t.profile(df)                 # type, missing%, summary per variable
```

## Table 1
```python
t.table_one(df, ["age","sex","bmi","weight_change"], group="arm")
```

## Right univariate test (auto-selected)
```python
t.auto_compare(df, outcome="weight_change", group="arm")            # continuous → t/Welch/MWU/ANOVA/KW
t.auto_compare(df, outcome="responder", group="arm")                # categorical → chi2/Fisher
t.auto_compare(df, outcome="pre_post", group="id", paired=True)     # paired
q, rej = t.p_adjust([0.01,0.04,0.20], method="fdr_bh")              # multiplicity
```

## Assumptions
```python
t.normality(df["weight_change"]); t.levene_equal_var(df,"weight_change","arm")
t.vif(df, ["age","bmi","sex"])
```

## Regression
```python
res, tidy = t.fit_model(df, "weight_change ~ C(arm) + age + C(sex)", family="gaussian")   # β, CI
res, tidy = t.fit_model(df, "responder ~ C(arm) + age",            family="binomial")     # OR, CI
res, tidy = t.fit_model(df, "exacerbations ~ C(arm) + age",        family="negbin")       # IRR, CI
```

## Survival
```python
t.km_logrank(df, "fu_months", "event", "arm")
cph, tidy, info = t.cox_model(df, "fu_months", "event", ["arm","age","sex"])   # HR, CI, PH check
```

## Machine learning (leakage-safe)
```python
ml = t.ml_classify(df, outcome="responder", features=["arm","age","sex","bmi"])
ml["cv_metrics"], ml["best_model"], ml["permutation_importance"]
```

## Figures
```python
t.plot_roc(y_true, y_score, "roc.png")
t.plot_forest(tidy, "OR/RR", "forest.png")
```

The toolkit is a convenience layer; for designs it does not cover (GEE, mixed models, multinomial/ordinal, competing risks, multiple imputation) call statsmodels / lifelines / scikit-learn directly following the relevant protocol file — keep preprocessing leakage-safe and every number traceable to output.

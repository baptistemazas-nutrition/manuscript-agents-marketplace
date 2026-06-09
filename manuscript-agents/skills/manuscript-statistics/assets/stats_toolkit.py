"""
stats_toolkit.py — reusable engine for the manuscript-statistics skill.

Design goals
------------
* One import, broad coverage: profiling, Table 1, assumption checks, the right
  univariate test, regression (OLS/logistic/Poisson/NB/ordinal), survival (KM/
  log-rank/Cox), and leakage-safe machine learning with calibration + importance.
* Every function returns plain Python/pandas objects so callers can render tables
  and trace every number back to an output.
* Heavy libraries are imported lazily so `import stats_toolkit` stays cheap and
  a missing optional dependency only fails the function that needs it.

Reproducibility: set_seed() once; record library versions with versions().
"""
from __future__ import annotations
import math, io
import numpy as np
import pandas as pd

RANDOM_SEED = 42

def set_seed(seed: int = RANDOM_SEED):
    global RANDOM_SEED
    RANDOM_SEED = seed
    np.random.seed(seed)
    return seed

def versions() -> dict:
    import sys, importlib
    out = {"python": sys.version.split()[0]}
    for m in ["pandas","numpy","scipy","statsmodels","sklearn","lifelines","pingouin"]:
        try:
            out[m] = importlib.import_module(m).__version__
        except Exception:
            out[m] = None
    return out

# --------------------------------------------------------------------------- #
# Loading & profiling
# --------------------------------------------------------------------------- #
def load_data(path: str, **kw) -> pd.DataFrame:
    p = str(path).lower()
    if p.endswith((".xlsx", ".xls")):
        return pd.read_excel(path, **kw)
    if p.endswith((".tsv", ".tab")):
        return pd.read_csv(path, sep="\t", **kw)
    # csv with separator sniffing
    try:
        return pd.read_csv(path, sep=None, engine="python", **kw)
    except Exception:
        return pd.read_csv(path, **kw)

def infer_kind(s: pd.Series) -> str:
    """continuous | binary | categorical | datetime | id"""
    if pd.api.types.is_datetime64_any_dtype(s):
        return "datetime"
    nun = s.nunique(dropna=True)
    if nun <= 1:
        return "constant"
    if nun == 2:
        return "binary"
    if pd.api.types.is_numeric_dtype(s):
        s_nonan = s.dropna()
        integer_like = bool((s_nonan % 1 == 0).all()) if len(s_nonan) else False
        # high-cardinality INTEGER columns that are ~unique per row -> likely an id
        if integer_like and nun > 20 and nun >= 0.95 * s.notna().sum():
            return "id"
        # small set of integer codes -> categorical-numeric
        if nun <= 10 and integer_like and float(np.nanmax(np.abs(s_nonan.values))) < 1e6:
            return "categorical-numeric"
        return "continuous"
    if nun > 0.95 * s.notna().sum() and nun > 20:
        return "id"
    return "categorical"

def profile(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    n = len(df)
    for c in df.columns:
        s = df[c]
        k = infer_kind(s)
        row = {"variable": c, "dtype": str(s.dtype), "kind": k,
               "n": int(s.notna().sum()), "missing": int(s.isna().sum()),
               "missing_pct": round(100 * s.isna().mean(), 1),
               "n_unique": int(s.nunique(dropna=True))}
        if pd.api.types.is_numeric_dtype(s) and k in ("continuous", "categorical-numeric", "binary"):
            row.update({"mean": round(float(s.mean()), 4) if s.notna().any() else None,
                        "sd": round(float(s.std()), 4) if s.notna().sum() > 1 else None,
                        "median": float(s.median()) if s.notna().any() else None,
                        "min": float(s.min()) if s.notna().any() else None,
                        "max": float(s.max()) if s.notna().any() else None})
        else:
            top = s.value_counts(dropna=True).head(3).to_dict()
            row["top_levels"] = "; ".join(f"{k2}={v2}" for k2, v2 in top.items())
        rows.append(row)
    return pd.DataFrame(rows)

# --------------------------------------------------------------------------- #
# Assumptions
# --------------------------------------------------------------------------- #
def normality(x) -> dict:
    from scipy import stats
    x = pd.Series(x).dropna().values
    n = len(x)
    if n < 3:
        return {"n": n, "test": None, "p": None, "normal": None}
    if n <= 5000:
        stat, p = stats.shapiro(x); test = "Shapiro-Wilk"
    else:
        stat, p = stats.normaltest(x); test = "D'Agostino-Pearson"
    return {"n": n, "test": test, "statistic": float(stat), "p": float(p), "normal": bool(p > 0.05)}

def levene_equal_var(df, outcome, group) -> dict:
    from scipy import stats
    groups = [g[outcome].dropna().values for _, g in df.groupby(group) if g[outcome].notna().sum() > 1]
    if len(groups) < 2:
        return {"test": "Levene", "p": None, "equal_var": None}
    stat, p = stats.levene(*groups, center="median")
    return {"test": "Levene", "statistic": float(stat), "p": float(p), "equal_var": bool(p > 0.05)}

def vif(df: pd.DataFrame, predictors: list) -> pd.DataFrame:
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    import statsmodels.api as sm
    X = pd.get_dummies(df[predictors].dropna(), drop_first=True).astype(float)
    X = sm.add_constant(X)
    out = [{"term": X.columns[i], "VIF": round(float(variance_inflation_factor(X.values, i)), 3)}
           for i in range(X.shape[1]) if X.columns[i] != "const"]
    return pd.DataFrame(out)

# --------------------------------------------------------------------------- #
# Effect sizes
# --------------------------------------------------------------------------- #
def cohen_d(a, b) -> float:
    a = pd.Series(a).dropna().values; b = pd.Series(b).dropna().values
    na, nb = len(a), len(b)
    sp = math.sqrt(((na - 1) * a.std(ddof=1) ** 2 + (nb - 1) * b.std(ddof=1) ** 2) / (na + nb - 2))
    return float((a.mean() - b.mean()) / sp) if sp else float("nan")

def hedges_g(a, b) -> float:
    a = pd.Series(a).dropna().values; b = pd.Series(b).dropna().values
    n = len(a) + len(b)
    return cohen_d(a, b) * (1 - 3 / (4 * n - 9))

def cramers_v(confusion: pd.DataFrame) -> float:
    from scipy import stats
    chi2 = stats.chi2_contingency(confusion)[0]
    n = confusion.values.sum()
    r, k = confusion.shape
    return float(math.sqrt((chi2 / n) / (min(r - 1, k - 1) or 1)))

# --------------------------------------------------------------------------- #
# Univariate auto-test (2+ groups, correct test for the data)
# --------------------------------------------------------------------------- #
def auto_compare(df: pd.DataFrame, outcome: str, group: str, paired: bool = False) -> dict:
    """Pick and run the appropriate bivariate test for outcome ~ group."""
    from scipy import stats
    d = df[[outcome, group]].dropna()
    ok = infer_kind(d[outcome])
    levels = list(pd.unique(d[group]))
    res = {"outcome": outcome, "group": group, "outcome_kind": ok,
           "n_groups": len(levels), "paired": paired}

    if ok == "continuous":
        arrs = [d.loc[d[group] == lv, outcome].astype(float).values for lv in levels]
        normal = all(normality(a).get("normal") for a in arrs if len(a) >= 3)
        if len(levels) == 2:
            a, b = arrs
            if paired:
                if normal:
                    stat, p = stats.ttest_rel(a, b); res["test"] = "Paired t-test"
                else:
                    stat, p = stats.wilcoxon(a, b); res["test"] = "Wilcoxon signed-rank"
            else:
                ev = levene_equal_var(d, outcome, group).get("equal_var", False)
                if normal:
                    stat, p = stats.ttest_ind(a, b, equal_var=bool(ev))
                    res["test"] = "Student t-test" if ev else "Welch t-test"
                else:
                    stat, p = stats.mannwhitneyu(a, b, alternative="two-sided")
                    res["test"] = "Mann-Whitney U"
            res["effect_size"] = {"cohen_d": round(cohen_d(a, b), 3), "hedges_g": round(hedges_g(a, b), 3)}
        else:
            if paired:
                stat, p = stats.friedmanchisquare(*arrs); res["test"] = "Friedman"
            elif normal:
                stat, p = stats.f_oneway(*arrs); res["test"] = "One-way ANOVA"
            else:
                stat, p = stats.kruskal(*arrs); res["test"] = "Kruskal-Wallis"
        res.update({"statistic": float(stat), "p": float(p)})
    else:
        ct = pd.crosstab(d[outcome], d[group])
        if ct.shape == (2, 2) and ct.values.min() < 5:
            _, p = stats.fisher_exact(ct.values); res["test"] = "Fisher exact"; stat = None
        else:
            chi2, p, dof, _ = stats.chi2_contingency(ct); res["test"] = "Chi-square"; stat = float(chi2)
        res.update({"statistic": stat, "p": float(p), "cramers_v": round(cramers_v(ct), 3),
                    "table": ct})
    return res

def p_adjust(pvals, method: str = "fdr_bh"):
    from statsmodels.stats.multitest import multipletests
    rej, q, _, _ = multipletests(pvals, method=method)
    return list(map(float, q)), list(map(bool, rej))

# --------------------------------------------------------------------------- #
# Table 1
# --------------------------------------------------------------------------- #
def table_one(df: pd.DataFrame, variables: list, group: str | None = None) -> pd.DataFrame:
    """Table 1. Format for a continuous row is decided ONCE on the overall
    distribution (mean +/- SD if ~normal, else median [IQR]) and applied to every
    cell in that row, per standard Table 1 convention."""
    rows = []
    def _is_cont(s):
        return infer_kind(s) == "continuous" and pd.api.types.is_numeric_dtype(s)
    def _cont(s, use_mean):
        s = s.dropna()
        if len(s) == 0:
            return "-"
        return (f"{s.mean():.2f} ± {s.std():.2f}" if use_mean
                else f"{s.median():.2f} [{s.quantile(.25):.2f}-{s.quantile(.75):.2f}]")
    def _cat(s):
        s = s.dropna()
        if len(s) == 0:
            return "-"
        vc = s.value_counts()
        return "; ".join(f"{i}: {v} ({100*v/len(s):.1f}%)" for i, v in vc.items())
    for v in variables:
        s_all = df[v]
        cont = _is_cont(s_all)
        use_mean = bool(normality(s_all).get("normal")) if cont else False
        row = {"variable": v,
               "overall": _cont(s_all, use_mean) if cont else _cat(s_all)}
        if group:
            for lv, g in df.groupby(group):
                row[f"{group}={lv}"] = _cont(g[v], use_mean) if cont else _cat(g[v])
            try:
                row["p"] = round(auto_compare(df, v, group)["p"], 4)
            except Exception:
                row["p"] = None
        rows.append(row)
    return pd.DataFrame(rows)

# --------------------------------------------------------------------------- #
# Regression (statsmodels formula API)
# --------------------------------------------------------------------------- #
def fit_model(df, formula, family="gaussian"):
    """family: gaussian|binomial|poisson|negbin -> returns fitted result + tidy table."""
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    fam = {"gaussian": lambda: None, "binomial": lambda: sm.families.Binomial(),
           "poisson": lambda: sm.families.Poisson(), "negbin": lambda: sm.families.NegativeBinomial()}
    import warnings as _w
    if family == "gaussian":
        res = smf.ols(formula, data=df).fit()
        tidy = pd.DataFrame({"term": res.params.index, "estimate": res.params.values,
                             "ci_low": res.conf_int()[0].values, "ci_high": res.conf_int()[1].values,
                             "p": res.pvalues.values})
    else:
        with _w.catch_warnings():
            _w.simplefilter('ignore')
            res = smf.glm(formula, data=df, family=fam[family]()).fit()
        coef = res.params; ci = res.conf_int()
        expo = family in ("binomial", "poisson", "negbin")
        tidy = pd.DataFrame({"term": coef.index,
                             ("OR/RR" if expo else "estimate"): (np.exp(coef.values) if expo else coef.values),
                             "ci_low": (np.exp(ci[0].values) if expo else ci[0].values),
                             "ci_high": (np.exp(ci[1].values) if expo else ci[1].values),
                             "p": res.pvalues.values})
    return res, tidy.round(4)

# --------------------------------------------------------------------------- #
# Survival
# --------------------------------------------------------------------------- #
def km_logrank(df, time, event, group):
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import multivariate_logrank_test
    d = df[[time, event, group]].dropna()
    curves = {}
    kmf = KaplanMeierFitter()
    for lv, g in d.groupby(group):
        kmf.fit(g[time], g[event], label=str(lv))
        curves[str(lv)] = {"median_survival": float(kmf.median_survival_time_)}
    lr = multivariate_logrank_test(d[time], d[group], d[event])
    return {"curves": curves, "logrank_p": float(lr.p_value), "logrank_stat": float(lr.test_statistic)}

def cox_model(df, time, event, covariates):
    from lifelines import CoxPHFitter
    d = df[[time, event] + covariates].dropna()
    d = pd.get_dummies(d, drop_first=True)
    cph = CoxPHFitter().fit(d, duration_col=time, event_col=event)
    tidy = cph.summary[["coef", "exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].copy()
    tidy.columns = ["coef", "HR", "HR_ci_low", "HR_ci_high", "p"]
    # proportional hazards check (quiet)
    ph_p = None
    try:
        import contextlib
        from lifelines.statistics import proportional_hazard_test
        with contextlib.redirect_stdout(io.StringIO()):
            zph = proportional_hazard_test(cph, d, time_transform="rank")
        ph_p = float(zph.summary["p"].min())
    except Exception:
        ph_p = None
    return cph, tidy.round(4), {"ph_global_min_p": ph_p, "ph_ok": (ph_p is None or ph_p > 0.05)}

# --------------------------------------------------------------------------- #
# Machine learning (leakage-safe, calibrated, interpretable)
# --------------------------------------------------------------------------- #
def ml_classify(df, outcome, features, model="auto", cv=5, seed=RANDOM_SEED):
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.model_selection import cross_val_predict, StratifiedKFold
    from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
    from sklearn.inspection import permutation_importance

    d = df[features + [outcome]].dropna()
    X, y = d[features], d[outcome]
    y = (y == sorted(y.unique())[-1]).astype(int) if y.nunique() == 2 else y
    num = [c for c in features if pd.api.types.is_numeric_dtype(d[c]) and infer_kind(d[c]) == "continuous"]
    cat = [c for c in features if c not in num]
    pre = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat)])
    models = {"logistic": LogisticRegression(max_iter=1000),
              "rf": RandomForestClassifier(n_estimators=400, random_state=seed),
              "gb": GradientBoostingClassifier(random_state=seed)}
    if model != "auto":
        models = {model: models[model]}
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
    out = {}; cv_proba = {}
    for name, clf in models.items():
        pipe = Pipeline([("pre", pre), ("clf", clf)])
        proba = cross_val_predict(pipe, X, y, cv=skf, method="predict_proba")[:, 1]
        cv_proba[name] = proba
        out[name] = {"roc_auc": round(float(roc_auc_score(y, proba)), 3),
                     "pr_auc": round(float(average_precision_score(y, proba)), 3),
                     "brier": round(float(brier_score_loss(y, proba)), 3)}
    best = max(out, key=lambda k: out[k]["roc_auc"])
    # permutation importance on the best model, fit on full data (report as exploratory)
    pipe = Pipeline([("pre", pre), ("clf", models[best])]).fit(X, y)
    perm = permutation_importance(pipe, X, y, n_repeats=10, random_state=seed, scoring="roc_auc")
    imp = pd.DataFrame({"feature": features, "importance": perm.importances_mean}).sort_values(
        "importance", ascending=False).round(4)
    # cv_proba_best + y_true let callers draw an HONEST (out-of-fold) ROC matching cv_metrics
    return {"cv_metrics": out, "best_model": best, "n": len(d),
            "permutation_importance": imp, "fitted_pipeline": pipe,
            "cv_proba": cv_proba[best], "y_true": y.to_numpy()}

# --------------------------------------------------------------------------- #
# Plots (saved to file; return path)
# --------------------------------------------------------------------------- #
def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt

def plot_roc(y_true, y_score, path="roc.png"):
    from sklearn.metrics import roc_curve, roc_auc_score
    plt = _mpl()
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.plot(fpr, tpr, label=f"AUC = {auc:.3f}"); ax.plot([0, 1], [0, 1], "--", color="grey")
    ax.set_xlabel("1 - Specificity"); ax.set_ylabel("Sensitivity"); ax.legend(loc="lower right")
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    return path

def plot_forest(tidy, estimate_col, path="forest.png", title="Adjusted estimates"):
    plt = _mpl()
    t = tidy[tidy["term"] != "Intercept"] if "term" in tidy else tidy
    fig, ax = plt.subplots(figsize=(6, 0.5 * len(t) + 1))
    y = range(len(t))
    ax.errorbar(t[estimate_col], y,
                xerr=[t[estimate_col] - t["ci_low"], t["ci_high"] - t[estimate_col]],
                fmt="o", capsize=3)
    ratio = estimate_col in ("OR/RR", "HR")
    ref = 1 if ratio else 0
    ax.axvline(ref, ls="--", color="grey")
    if ratio:
        ax.set_xscale("log")
        from matplotlib.ticker import ScalarFormatter
        ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_yticks(list(y)); ax.set_yticklabels(t["term"]); ax.set_xlabel(estimate_col); ax.set_title(title)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    return path

def plot_box(df, outcome, group, path="box.png", ylabel=None):
    plt = _mpl(); import numpy as _np
    d = df[[outcome, group]].dropna()
    levels = list(pd.unique(d[group]))
    data = [d.loc[d[group] == lv, outcome].astype(float).values for lv in levels]
    fig, ax = plt.subplots(figsize=(5, 4))
    parts = ax.violinplot(data, showmedians=True)
    ax.boxplot(data, widths=0.15, showfliers=False)
    ax.set_xticks(range(1, len(levels) + 1)); ax.set_xticklabels([str(l) for l in levels])
    ax.set_ylabel(ylabel or outcome); ax.set_xlabel(group)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    return path

def plot_km(df, time, event, group, path="km.png", xlabel="Time", ylabel="Survival probability"):
    from lifelines import KaplanMeierFitter
    plt = _mpl()
    d = df[[time, event, group]].dropna()
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    kmf = KaplanMeierFitter()
    for lv, g in d.groupby(group):
        kmf.fit(g[time], g[event], label=str(lv)); kmf.plot_survival_function(ax=ax, ci_show=True)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_ylim(0, 1.02); ax.legend(title=group)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    return path

if __name__ == "__main__":
    print("stats_toolkit loaded. versions:", versions())

# eda_calculator.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from statsmodels.stats.diagnostic import lilliefors
import statsmodels.api as sm
from scipy.stats import boxcox

os.makedirs("eda_outputs/plots", exist_ok=True)

# Load data
df = pd.read_csv("analysis_ready_data.csv")

# Rename long columns for display
rename_map = {col: col.replace("log_fiyat_per_m2", "log_fpm2")
                   .replace("boxcox_fiyat_per_m2", "boxcox_fpm2")
                   .replace("boxcox_metrekare", "boxcox_mt2")
                   .replace("log_metrekare", "log_mt2")
              for col in df.columns}
df.rename(columns=rename_map, inplace=True)

# Filter out 1% tails
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    q_low = df[col].quantile(0.01)
    q_high = df[col].quantile(0.99)
    df = df[(df[col] > q_low) & (df[col] < q_high)]

# Log & Box-Cox transforms
log_cols = []
boxcox_cols = []
for col in numeric_cols:
    if (df[col] > 0).all():
        df[f"log_{col}"] = np.log1p(df[col])
        log_cols.append(f"log_{col}")
        df[f"boxcox_{col}"] = boxcox(df[col])[0]
        boxcox_cols.append(f"boxcox_{col}")

# Summary statistics
def format_k(x):
    if pd.isna(x): return ""
    elif abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    elif abs(x) >= 1_000:
        return f"{x/1_000:.1f}K"
    else:
        return f"{x:.2f}"

summary_stats = df.describe().T.round(2)
summary_stats_formatted = summary_stats.applymap(format_k)
summary_stats_formatted.to_csv("eda_outputs/summary.csv")

# Normality tests
all_numeric = list(numeric_cols) + log_cols + boxcox_cols
norm_test_table = pd.DataFrame(columns=["Variable", "Test", "Statistic", "p-value", "Result"])

for column in all_numeric:
    try:
        stat_lillie, p_lillie = lilliefors(df[column].dropna())
        result = "Fail to reject H0 (normal)" if p_lillie > 0.05 else "Reject H0 (not normal)"
        norm_test_table = pd.concat([norm_test_table, pd.DataFrame.from_records([{
            "Variable": column, "Test": "KS-Lilliefors", "Statistic": round(stat_lillie, 3),
            "p-value": f"{p_lillie:.3e}", "Result": result
        }])])
    except: pass
    try:
        ad_test = stats.anderson(df[column].dropna(), dist='norm')
        crit_val = ad_test.critical_values[2]  # 5% level
        result = "Fail to reject H0 (normal)" if ad_test.statistic < crit_val else "Reject H0 (not normal)"
        norm_test_table = pd.concat([norm_test_table, pd.DataFrame.from_records([{
            "Variable": column, "Test": "Anderson-Darling", "Statistic": round(ad_test.statistic, 3),
            "p-value": f"< {crit_val:.3f}", "Result": result
        }])])
    except: pass

norm_test_table.to_csv("eda_outputs/normality_results.txt", index=False, sep='\t')

# Q-Q plots with R^2
qq_r2_scores = []
for column in all_numeric:
    try:
        osm, osr = sm.ProbPlot(df[column].dropna()).theoretical_quantiles, np.sort(df[column].dropna())
        r_squared = np.corrcoef(osm, osr)[0, 1] ** 2
        qq_r2_scores.append((column, r_squared))
        sm.qqplot(df[column].dropna(), line='s')
        plt.title(f"Q-Q Plot of {column}\nR^2 = {r_squared:.4f}")
        plt.savefig(f"eda_outputs/plots/qq_{column}.png")
        plt.close()
    except: pass

qq_r2_scores.sort(key=lambda x: x[1], reverse=True)
with open("eda_outputs/qq_r2_scores.txt", "w") as f:
    for var, r2 in qq_r2_scores:
        tag = "(visually normal)" if r2 >= 0.98 else "(possibly non-normal)"
        f.write(f"{var}: R^2 = {r2:.4f} {tag}\n")

# Correlation matrix
corr = df[all_numeric].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
plt.figure(figsize=(10, 8))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig("eda_outputs/plots/correlation_matrix.png")
plt.close()

# Plots
for column in all_numeric:
    try:
        sns.histplot(df[column], kde=True, bins='sturges')
        plt.title(f"Histogram of {column}")
        plt.savefig(f"eda_outputs/plots/hist_{column}.png")
        plt.close()

        sns.boxplot(x=df[column])
        plt.title(f"Boxplot of {column}")
        plt.savefig(f"eda_outputs/plots/box_{column}.png")
        plt.close()
    except: pass

for cat_col in ["kat", "kademe"]:
    if cat_col in df.columns:
        plt.figure(figsize=(10, 4))
        df[cat_col].astype(str).value_counts().sort_index().plot(kind="bar")
        plt.title(f"Histogram of {cat_col}")
        plt.xticks(rotation=30, ha='right', fontsize=8)
        plt.tight_layout()
        plt.savefig(f"eda_outputs/plots/hist_{cat_col}.png")
        plt.close()
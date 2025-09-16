#!/usr/bin/env python3
"""
week7_iris_analysis.py

Week 7: Iris dataset analysis (PLP - Python)
- Loads Iris via sklearn.datasets.load_iris()
- Explores, cleans (if needed), analyzes
- Produces 4 visualizations (line, bar, histogram, scatter)
- Saves cleaned CSV, plots/, and a text file containing terminal outputs:
    analysis_output.txt

Run:
    python week7_iris_analysis.py
"""

import os
import sys
from datetime import datetime

# --- Safe imports with friendly messages ---
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
except Exception as e:
    print("ERROR: Missing required packages. Install them in your environment:")
    print("    python -m pip install pandas numpy matplotlib scikit-learn")
    print("Then re-run this script.")
    raise

# --- configuration ---
BASE_DIR = os.getcwd()
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

OUTPUT_TXT = os.path.join(BASE_DIR, "analysis_output.txt")
CLEANED_CSV = os.path.join(BASE_DIR, "week7_iris_clean.csv")

# --- helper to write terminal output to both screen and a file (tee) ---
class Tee:
    def __init__(self, filename):
        self.file = open(filename, "w", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, s):
        self.stdout.write(s)
        self.file.write(s)

    def flush(self):
        self.stdout.flush()
        self.file.flush()

    def close(self):
        self.file.close()

# --- data functions ---
def load_dataset():
    """Load Iris dataset and convert to pandas DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    # normalize column names to simpler forms
    df.columns = [c.replace(" (cm)", "").replace(" ", "_") for c in df.columns]
    df["species_id"] = iris.target
    df["species"] = pd.Categorical([iris.target_names[i] for i in iris.target])
    return df

def feature_engineer(df):
    """Add some derived features (sepal_area, petal_area) to be slightly unique."""
    # columns expected: sepal_length, sepal_width, petal_length, petal_width
    # original column names in sklearn: 'sepal length (cm)' etc. we cleaned names above.
    if {"sepal_length", "sepal_width", "petal_length", "petal_width"}.issubset(df.columns):
        df["sepal_area"] = (df["sepal_length"] * df["sepal_width"]).round(3)
        df["petal_area"] = (df["petal_length"] * df["petal_width"]).round(3)
    return df

def explore_and_clean(df):
    """Print exploration info and perform simple cleaning if missing values exist."""
    print("=== Data Head (first 5 rows) ===")
    print(df.head().to_string(index=False))
    print("\n=== Data Info ===")
    df.info()
    print("\n=== Missing Values per Column ===")
    print(df.isnull().sum())

    # simple cleaning strategy
    df_clean = df.copy()
    missing_total = df_clean.isnull().sum().sum()
    if missing_total > 0:
        print(f"\nFound {missing_total} missing values. Applying median imputation for numeric columns.")
        num_cols = df_clean.select_dtypes(include=[np.number]).columns
        for c in num_cols:
            if df_clean[c].isnull().any():
                median_val = df_clean[c].median()
                df_clean[c].fillna(median_val, inplace=True)
                print(f" - Filled missing in '{c}' with median {median_val}")
    else:
        print("\nNo missing values found. No imputation needed.")

    # ensure types: species as category
    df_clean["species"] = df_clean["species"].astype("category")
    return df_clean

def analyze(df):
    """Perform basic analysis and groupings; return findings."""
    print("\n=== Descriptive Statistics (numeric) ===")
    print(df.describe().round(3))

    # Groupings: mean petal_length and sepal_length per species
    group_metrics = df.groupby("species").agg(
        mean_sepal_length=("sepal_length", "mean"),
        mean_petal_length=("petal_length", "mean"),
        mean_sepal_area=("sepal_area", "mean") if "sepal_area" in df.columns else ("sepal_length", "mean"),
    ).round(3)
    print("\n=== Grouped Means by Species ===")
    print(group_metrics)

    # additional grouping: median and std for units of area
    if "petal_area" in df.columns:
        area_stats = df.groupby("species")["petal_area"].agg(["mean", "median", "std"]).round(3)
        print("\n=== Petal Area stats by Species ===")
        print(area_stats)

    # correlations
    print("\n=== Correlation matrix (numeric) ===")
    corr = df.select_dtypes(include=[np.number]).corr().round(3)
    print(corr)

    # Findings (data-driven)
    findings = []
    # species with largest mean sepal length
    try:
        s_max = group_metrics["mean_sepal_length"].idxmax()
        findings.append(f"Species with largest mean sepal length: {s_max} ({group_metrics['mean_sepal_length'].max():.3f} cm)")
    except Exception:
        pass

    # strongest positive correlation among numeric features (excluding self-correlation)
    corr_unstack = corr.unstack().sort_values(ascending=False)
    # get top pair excluding identical pairs
    for (a, b), val in corr_unstack.items():
        if a != b:
            top_pair = (a, b, val)
            break
    findings.append(f"Strongest positive correlation: {top_pair[0]} vs {top_pair[1]} = {top_pair[2]:.3f}")

    return findings, corr

# --- plotting functions (4 required visuals) ---
def plot_line_cumulative_mean(df):
    """Line chart: cumulative mean of sepal_length across sample order.
       Explanation: Iris has no time index; to satisfy 'trend' requirement we display a cumulative mean across samples.
    """
    series = df["sepal_length"].expanding().mean()
    plt.figure(figsize=(8, 4.5))
    plt.plot(series.index, series.values, marker="o", linewidth=1, markersize=3, label="Cumulative mean sepal_length")
    plt.title("Cumulative Mean of Sepal Length (sample order) — trend proxy")
    plt.xlabel("Sample index (ordered)")
    plt.ylabel("Cumulative mean sepal length (cm)")
    plt.grid(alpha=0.3)
    plt.legend()
    out = os.path.join(PLOTS_DIR, "line_cumulative_sepal_length.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_bar_avg_petal_length(df):
    """Bar chart: average petal length per species, annotated."""
    means = df.groupby("species")["petal_length"].mean().sort_values(ascending=False)
    plt.figure(figsize=(6, 4))
    ax = means.plot(kind="bar")
    plt.title("Average Petal Length by Species")
    plt.xlabel("Species")
    plt.ylabel("Mean petal length (cm)")
    # annotate bars
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center", va="bottom", fontsize=9, rotation=0)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "bar_avg_petal_length_by_species.png")
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_histogram_sepal_length(df):
    """Histogram of sepal length distribution."""
    plt.figure(figsize=(6, 4))
    plt.hist(df["sepal_length"], bins=12, edgecolor="black", alpha=0.75)
    mean_val = df["sepal_length"].mean()
    plt.axvline(mean_val, color="red", linestyle="--", linewidth=1, label=f"Mean = {mean_val:.2f}")
    plt.title("Distribution of Sepal Length")
    plt.xlabel("Sepal length (cm)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "hist_sepal_length.png")
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_scatter_sepal_vs_petal(df):
    """Scatter plot: sepal length vs petal length, colored by species."""
    colors = {"setosa": "C0", "versicolor": "C1", "virginica": "C2"}
    plt.figure(figsize=(6.5, 5))
    for species, g in df.groupby("species"):
        plt.scatter(g["sepal_length"], g["petal_length"], label=str(species), alpha=0.75, s=40, edgecolors="k", color=colors.get(str(species), None))
    plt.title("Sepal Length vs Petal Length (colored by species)")
    plt.xlabel("Sepal length (cm)")
    plt.ylabel("Petal length (cm)")
    plt.legend(title="Species")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "scatter_sepal_vs_petal.png")
    plt.savefig(out, dpi=150)
    plt.close()
    return out

# --- main orchestration ---
def main():
    tee = Tee(OUTPUT_TXT)
    sys.stdout = tee  # redirect prints to file + console

    try:
        start_time = datetime.now()
        print(f"Week 7 — Iris analysis started at {start_time.isoformat()}\n")
        df = load_dataset()
        df = feature_engineer(df)
        df_clean = explore_and_clean(df)

        # Save cleaned CSV for submission
        df_clean.to_csv(CLEANED_CSV, index=False)
        print(f"\nCleaned dataset saved to: {CLEANED_CSV}")

        findings, corr = analyze(df_clean)

        # Create plots
        plots = []
        plots.append(plot_line_cumulative_mean(df_clean))
        plots.append(plot_bar_avg_petal_length(df_clean))
        plots.append(plot_histogram_sepal_length(df_clean))
        plots.append(plot_scatter_sepal_vs_petal(df_clean))

        print("\nPlots saved to:")
        for p in plots:
            print(" -", p)

        # Print findings
        print("\n=== Findings / Observations ===")
        for f in findings:
            print(" -", f)

        end_time = datetime.now()
        print(f"\nCompleted at {end_time.isoformat()} (duration: {end_time - start_time})")

    except Exception as e:
        print(f"\nERROR: An exception occurred during processing: {e}")
    finally:
        # restore stdout and close file
        sys.stdout = tee.stdout
        tee.close()

        # final console-only summary
        print("\nExecution finished. Terminal output was saved to:", OUTPUT_TXT)
        print("Generated files:")
        print(" -", CLEANED_CSV)
        for fname in sorted(os.listdir(PLOTS_DIR)):
            print(" -", os.path.join(PLOTS_DIR, fname))
        print("\nNotes:")
        print(" - The line chart uses a cumulative mean across samples as a 'trend' proxy (Iris has no time column).")

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = "students_clean.csv"
OUTDIR = Path("figures")
OUTDIR.mkdir(exist_ok=True)

df = pd.read_csv(CSV_PATH)

if not {"total","average"}.issubset(df.columns):
    df["total"] = df[["math","science","english"]].sum(axis=1)
    df["average"] = df[["math","science","english"]].mean(axis=1)

avg_per_subject = df[["math","science","english"]].mean()
plt.figure()
avg_per_subject.plot(kind="bar")
plt.title("Average Scores per Subject")
plt.ylabel("Average score")
plt.tight_layout()
plt.savefig(OUTDIR / "bar_avg_per_subject.png")
plt.close()

plt.figure()
df["grade"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Grade Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUTDIR / "pie_grade_distribution.png")
plt.close()

plt.figure()
df["math"].plot(kind="hist", bins=15)
plt.title("Math Score Distribution")
plt.xlabel("Math score")
plt.tight_layout()
plt.savefig(OUTDIR / "hist_math_scores.png")
plt.close()

if "rank" not in df.columns:
    df = df.assign(rank=df["average"].rank(ascending=False, method="first").astype(int))

trend = df.sort_values("rank")
plt.figure()
plt.plot(trend["rank"], trend["average"])
plt.title("Performance Trend by Rank (1 = best)")
plt.xlabel("Rank")
plt.ylabel("Average score")
plt.tight_layout()
plt.savefig(OUTDIR / "line_trend_by_rank.png")
plt.close()

plt.figure()
plt.scatter(df["math"], df["science"])
plt.title("Math vs Science")
plt.xlabel("Math")
plt.ylabel("Science")
plt.tight_layout()
plt.savefig(OUTDIR / "scatter_math_vs_science.png")
plt.close()

num_cols = df.select_dtypes(include=[np.number])
corr = num_cols.corr()

plt.figure()
plt.imshow(corr, interpolation="nearest")
plt.title("Correlation Matrix")
plt.xticks(range(len(num_cols.columns)), num_cols.columns, rotation=45, ha="right")
plt.yticks(range(len(num_cols.columns)), num_cols.columns)
plt.colorbar()
plt.tight_layout()
plt.savefig(OUTDIR / "heatmap_correlation.png")
plt.close()

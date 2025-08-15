#!/usr/bin/env python3

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

CLEAN_CSV = Path("students_clean.csv")
RAW_CSV   = Path("students.csv")
OUTDIR    = Path("figures")
OUTDIR.mkdir(exist_ok=True)

if CLEAN_CSV.exists():
    df = pd.read_csv(CLEAN_CSV)
    print(f"Loaded: {CLEAN_CSV}")
elif RAW_CSV.exists():
    df = pd.read_csv(RAW_CSV)
    print(f"Loaded: {RAW_CSV}")
else:
    sys.exit("❌ Neither students_clean.csv nor students.csv found in current folder.")

if df["pass_fail"].dtype == object:
    df["pass_fail"] = (
        df["pass_fail"].astype(str).str.strip().str.lower().map({"pass": 1, "fail": 0})
    )

df = df.dropna(subset=["pass_fail"]).copy()
df["pass_fail"] = df["pass_fail"].astype(int)

candidates = ["math", "science", "english", "hours_studied", "attendance", "participation"]
features = [c for c in candidates if c in df.columns]
if not features:
    sys.exit("❌ No usable feature columns. Expected at least one of: " + ", ".join(candidates))

X = df[features].copy()
y = df["pass_fail"].copy()

X = X.fillna(X.median(numeric_only=True))

unique_classes = sorted(y.unique().tolist())
if len(unique_classes) < 2:
    print("⚠️ Only one class present in target. Classification metrics may be trivial.")
    stratify_arg = None
else:
    class_counts = y.value_counts()
    if (class_counts < 2).any():
        stratify_arg = None
        print("⚠️ Not enough samples per class to stratify; proceeding without stratify.")
    else:
        stratify_arg = y

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=stratify_arg
    )
except ValueError:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    print("⚠️ Fallback split without stratify due to small dataset.")

print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

train_n = len(X_train)
safe_k = max(1, min(5, train_n))
if safe_k % 2 == 0 and safe_k > 1:
    safe_k -= 1
print("Using k for k-NN:", safe_k)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    f"k-NN (k={safe_k})": KNeighborsClassifier(n_neighbors=safe_k),
}

def save_confmat(name: str, cm: np.ndarray) -> None:
    fig, ax = plt.subplots()
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title(f"{name} — Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["fail", "pass"]); ax.set_yticklabels(["fail", "pass"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center")
    fig.colorbar(im)
    fig.tight_layout()
    safe = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "")
    out = OUTDIR / f"cm_{safe}.png"
    plt.savefig(out)
    plt.close()
    print(f"💾 Saved confusion matrix → {out}")

results = []

for name, model in models.items():
    if name.startswith("Decision Tree"):
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
    else:
        model.fit(X_train_s, y_train)
        preds = model.predict(X_test_s)

    acc = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds, labels=[0, 1])
    results.append((name, acc))

    print(f"\n=== {name} ===")
    print("Features:", features)
    print("Accuracy:", round(acc, 4))
    print("Confusion matrix (rows=true [0,1]; cols=pred [0,1]):\n", cm)
    try:
        print("Classification report:\n",
              classification_report(y_test, preds, target_names=["fail", "pass"]))
    except Exception as e:
        print(f"(classification_report skipped: {e})")

    save_confmat(name, cm)

print("\n=== Model Comparison (Accuracy) ===")
for name, acc in sorted(results, key=lambda x: x[1], reverse=True):
    print(f"{name:20s} : {acc:.4f}")
print("\n✅ Done.")

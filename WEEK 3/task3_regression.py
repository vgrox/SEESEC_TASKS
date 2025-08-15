import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

CSV_PATH = "students_clean.csv"
OUTDIR = Path("figures")
OUTDIR.mkdir(exist_ok=True)

df = pd.read_csv(CSV_PATH)

if not {"average"}.issubset(df.columns):
    df["total"] = df[["math","science","english"]].sum(axis=1)
    df["average"] = df[["math","science","english"]].mean(axis=1)

pref_feats = [c for c in ["hours_studied", "attendance", "participation"] if c in df.columns]
if len(pref_feats) == 0:
    if "hours_studied" not in df.columns:
        raise ValueError("hours_studied column not found. Add it to your CSV for Task 3.")
    pref_feats = ["hours_studied"]

X = df[pref_feats].copy()
y = df["average"].copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

linreg = LinearRegression()
linreg.fit(X_train_s, y_train)

y_pred = linreg.predict(X_test_s)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("Features used:", pref_feats)
print({"MAE": round(mae, 3), "MSE": round(mse, 3), "RMSE": round(rmse, 3)})

plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Average")
plt.ylabel("Predicted Average")
plt.title("Linear Regression: Actual vs Predicted")
plt.tight_layout()
plt.savefig(OUTDIR / "reg_actual_vs_predicted.png")
plt.close()

if X.shape[1] == 1:
    x_col = pref_feats[0]
    x_all = df[x_col].to_numpy().reshape(-1, 1)
    x_min, x_max = x_all.min(), x_all.max()
    grid = np.linspace(x_min, x_max, 100).reshape(-1, 1)

    grid_s = (grid - scaler.mean_[0]) / scaler.scale_[0]

    y_line = linreg.predict(grid_s)

    plt.figure()
    plt.scatter(X_train[x_col], y_train, alpha=0.7)
    plt.plot(grid, y_line)
    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel("Average")
    plt.title(f"Regression Line: {x_col} vs Average")
    plt.tight_layout()
    plt.savefig(OUTDIR / "reg_line_single_feature.png")
    plt.close()

joblib.dump(linreg, "linreg_model.joblib")
joblib.dump(scaler, "scaler.joblib")
print("Saved linreg_model.joblib and scaler.joblib")

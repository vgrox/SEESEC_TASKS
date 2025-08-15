import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from pathlib import Path

# Synthetic training data: [hours_studied, attendance_percent, assignments_submitted] -> score
# We'll craft a simple relationship with some noise so the model is realistic.
rng = np.random.default_rng(42)
n = 200

hours = rng.uniform(0, 12, size=n)                 # 0-12 hours/day
attendance = rng.uniform(50, 100, size=n)          # 50-100%
assignments = rng.integers(0, 10, size=n)          # 0-9 assignments

# True underlying relationship (totally made up but plausible)
# score out of 100
score = 5*hours + 0.5*attendance + 2*assignments + rng.normal(0, 5, size=n)

X = np.column_stack([hours, attendance, assignments])
y = score

model = LinearRegression()
model.fit(X, y)

outdir = Path(__file__).parent
joblib.dump(model, outdir / "model.joblib")

# Save feature order for clarity
FEATURES = ["hours_studied", "attendance_percent", "assignments_submitted"]
(outdir / "feature_order.json").write_text(__import__("json").dumps(FEATURES, indent=2))

print("Trained model saved to", outdir / "model.joblib")
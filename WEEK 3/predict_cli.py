import sys, json, joblib, pandas as pd

# Load trained artifacts
linreg = joblib.load("linreg_model.joblib")
scaler = joblib.load("scaler.joblib")

# Read JSON from stdin
payload = json.loads(sys.stdin.read())

# Figure out which features the scaler expects (scikit-learn >=1.0)
expected = list(getattr(scaler, "feature_names_in_", []))
if not expected:
    # Fallback if feature names are unavailable; most likely you trained on hours_studied only
    expected = ["hours_studied"]

# Build input in the exact expected order; ignore any extra keys
row = []
missing = []
for feat in expected:
    val = payload.get(feat, None)
    if val is None:
        missing.append(feat)
    row.append(val)

if missing:
    raise SystemExit(f"Missing required fields: {missing}. Please include them in the JSON.")

X = pd.DataFrame([row], columns=expected)

# Transform & predict
X_s = scaler.transform(X)
pred = linreg.predict(X_s)[0]
print(round(float(pred), 2))

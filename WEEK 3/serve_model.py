from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, pandas as pd

app = Flask(__name__)
CORS(app)

linreg = joblib.load("linreg_model.joblib")
scaler = joblib.load("scaler.joblib")

# Auto-detect features the scaler/model were trained on
EXPECTED = list(getattr(scaler, "feature_names_in_", [])) or ["hours_studied"]

@app.get("/health")
def health():
    return jsonify(status="ok", expected_features=EXPECTED)

@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    # Build row in the exact expected order; ignore extras
    missing = [f for f in EXPECTED if f not in data]
    if missing:
        return jsonify(error=f"Missing required fields: {missing}", expected=EXPECTED), 400

    X = pd.DataFrame([[data[f] for f in EXPECTED]], columns=EXPECTED)
    Xs = scaler.transform(X)
    y = float(linreg.predict(Xs)[0])
    return jsonify(predicted_average=round(y, 2), used_features=EXPECTED)

if __name__ == "__main__":
    app.run(debug=True)

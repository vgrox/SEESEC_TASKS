from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import json
from pathlib import Path

app = Flask(__name__)

# --- Load model on startup ---
MODEL_DIR = Path(__file__).parent / "model"
MODEL_PATH = MODEL_DIR / "model.joblib"
FEATURE_PATH = MODEL_DIR / "feature_order.json"

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
else:
    model = None

if FEATURE_PATH.exists():
    FEATURE_ORDER = json.loads(FEATURE_PATH.read_text())
else:
    FEATURE_ORDER = ["hours_studied", "attendance_percent", "assignments_submitted"]

def _extract_inputs(data):
    """Validate & coerce inputs; returns (payload, errors).
    payload is dict {feature: float} in FEATURE_ORDER.
    """
    errors = {}
    payload = {}
    for key in FEATURE_ORDER:
        if key not in data or data[key] in (None, ""):
            errors[key] = "This field is required."
            continue
        try:
            # hours & attendance can be float; assignments int-like but we'll cast to float for the model
            payload[key] = float(data[key])
        except (TypeError, ValueError):
            errors[key] = "Must be a number."
    return payload, errors

@app.route("/")
def home():
    return render_template("index.html", feature_order=FEATURE_ORDER)

@app.route("/health")
def health():
    return {"status": "ok", "model_loaded": bool(model)}

@app.route("/predict", methods=["POST"])  # accepts JSON or form
def predict():
    global model
    if model is None:
        return jsonify({"error": "Model not found. Please train it first."}), 500

    if request.is_json:
        data = request.get_json(silent=True) or {}
        payload, errors = _extract_inputs(data)
        if errors:
            return jsonify({"errors": errors}), 400
        X = np.array([[payload[k] for k in FEATURE_ORDER]], dtype=float)
        y_pred = float(model.predict(X)[0])
        # Map to rough grade just for fun
        grade = (
            "A" if y_pred >= 90 else
            "B" if y_pred >= 80 else
            "C" if y_pred >= 70 else
            "D" if y_pred >= 60 else
            "F"
        )
        return jsonify({"prediction": round(y_pred, 2), "grade": grade, "inputs": payload})
    else:
        # Form submission
        form_data = {k: request.form.get(k) for k in FEATURE_ORDER}
        payload, errors = _extract_inputs(form_data)
        if errors:
            # Re-render form with errors
            return render_template("index.html", feature_order=FEATURE_ORDER, errors=errors, values=form_data), 400

        X = np.array([[payload[k] for k in FEATURE_ORDER]], dtype=float)
        y_pred = float(model.predict(X)[0])
        grade = (
            "A" if y_pred >= 90 else
            "B" if y_pred >= 80 else
            "C" if y_pred >= 70 else
            "D" if y_pred >= 60 else
            "F"
        )
        return render_template("result.html", score=round(y_pred, 2), grade=grade, inputs=payload)

if __name__ == "__main__":
    # For local dev only
    app.run(host="127.0.0.1", port=5000, debug=True)
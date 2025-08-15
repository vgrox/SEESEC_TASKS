# Week 4 – Student Performance Prediction API (Flask)

This mini‑project serves a simple ML model behind a Flask API and a basic HTML form.

## Quickstart

```bash
# from this folder
python3 -m venv .venv
source .venv/bin/activate        # On macOS / Linux
pip install -r requirements.txt

# Create a demo model (if you don't already have one):
python model/train_model.py

# Run the app:
python app.py
# Open http://127.0.0.1:5000 in your browser
```

## API

### `POST /predict` (JSON)

Body:
```json
{
  "hours_studied": 5,
  "attendance_percent": 90,
  "assignments_submitted": 6
}
```

Response:
```json
{
  "prediction": 87.42,
  "grade": "B",
  "inputs": {...}
}
```

### `POST /predict` (Form)

Submit via the homepage form. The result is rendered on `result.html`.

## Files

```
Week4/student_api/
├── app.py
├── model/
│   ├── model.joblib          # created by train_model.py
│   ├── feature_order.json    # feature order reference
│   └── train_model.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/
├── requirements.txt
└── README.md
```

## Testing with curl

```bash
curl -X POST http://127.0.0.1:5000/predict \  -H "Content-Type: application/json" \  -d '{"hours_studied": 5, "attendance_percent": 92, "assignments_submitted": 7}'
```

## Postman

- Create a `POST` request to `http://127.0.0.1:5000/predict`
- Body → Raw → JSON
- Paste the same JSON as above and send.

## Notes

- Input validation is included for both JSON and form.
- If you already have a trained model, replace `model/model.joblib` and update `feature_order.json` if your feature order differs.
# Student API Backend

This is a RESTful API for managing student records built using Flask and SQLite.

## Features
- Add, update, delete, and search student records
- Modular code structure
- CORS enabled for frontend integration

## Endpoints
- `GET /students`
- `POST /students`
- `PUT /students/<roll_number>`
- `DELETE /students/<roll_number>`
- `GET /students/search?name=...&grade=...`

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Initialize DB:
   ```python
   from db import initialize_db
   initialize_db()
   ```

3. Run server:
   ```
   python app.py
   ```

## Test with Postman
Import endpoints and test with JSON payloads.


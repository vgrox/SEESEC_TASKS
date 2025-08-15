from flask import Blueprint, request, jsonify
from db import get_db_connection
import sqlite3

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "API is working"})

@bp.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data.get('roll_number') or not data.get('name') or not data.get('grade'):
        return jsonify({'error': 'Missing data'}), 400
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO students (roll_number, name, grade) VALUES (?, ?, ?)',
                     (data['roll_number'], data['name'], data['grade']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Student added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Student with that roll number already exists'}), 400

@bp.route('/students/<int:roll_number>', methods=['PUT'])
def update_student(roll_number):
    data = request.get_json()
    if 'grade' not in data:
        return jsonify({'error': 'Grade is required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.execute('UPDATE students SET grade = ? WHERE roll_number = ?',
                              (data['grade'], roll_number))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify({'message': 'Student grade updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/students/<int:roll_number>', methods=['DELETE'])
def delete_student(roll_number):
    try:
        conn = get_db_connection()
        cursor = conn.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/students/search', methods=['GET'])
def search_students():
    name = request.args.get('name')
    grade = request.args.get('grade')
    conn = get_db_connection()
    query = 'SELECT * FROM students WHERE 1=1'
    params = []

    if name:
        query += ' AND name LIKE ?'
        params.append(f'%{name}%')
    if grade:
        query += ' AND grade = ?'
        params.append(grade)

    students = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

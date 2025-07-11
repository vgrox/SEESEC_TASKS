import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    grade TEXT NOT NULL
)
''')
conn.commit()
print("Table 'students' created successfully (or already exists).\n")

for i in range(3):
    print(f"Enter details for student {i+1}:")
    name = input("Name: ")
    roll_number = input("Roll Number: ")
    grade = input("Grade: ")
    try:
        cursor.execute("INSERT INTO students (name, roll_number, grade) VALUES (?, ?, ?)", (name, roll_number, grade))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}. Please ensure roll number is unique.")
        break
    print()

print("Students in the table:")
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

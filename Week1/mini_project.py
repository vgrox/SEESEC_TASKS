import sqlite3
import csv
import os

def connect_db():
    return sqlite3.connect('school.db')

def create_table():
    with connect_db() as conn:
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

def display_all_students():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, roll_number, grade FROM students')
        records = cursor.fetchall()
        if not records:
            print("\nNo student records found.\n")
        else:
            print("\nAll Student Records:")
            print(f"{'ID':<5}{'Name':<20}{'Roll Number':<15}{'Grade':<10}")
            print('-'*50)
            for row in records:
                print(f"{row[0]:<5}{row[1]:<20}{row[2]:<15}{row[3]:<10}")
            print()

def validate_name(name):
    return name.isalpha() and len(name) >= 2

def validate_roll_number(roll_number):
    return roll_number.isalnum() and len(roll_number) >= 2

def validate_grade(grade):
    return grade.upper() in ['A', 'B', 'C', 'D', 'E', 'F']

def add_student():
    print("\nAdd New Student Record:")
    while True:
        name = input("Enter student name: ").strip()
        if not validate_name(name):
            print("Invalid name. Name should be alphabetic and at least 2 characters.")
            continue
        break
    while True:
        roll_number = input("Enter roll number: ").strip()
        if not validate_roll_number(roll_number):
            print("Invalid roll number. Should be alphanumeric and at least 2 characters.")
            continue
        break
    while True:
        grade = input("Enter grade (A-F): ").strip().upper()
        if not validate_grade(grade):
            print("Invalid grade. Should be one of A, B, C, D, E, F.")
            continue
        break
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (name, roll_number, grade) VALUES (?, ?, ?)', (name, roll_number, grade))
            conn.commit()
        print("Student record added successfully!\n")
    except sqlite3.IntegrityError:
        print("Error: Roll number already exists.\n")

def search_and_update_student():
    print("\nSearch and Update Student Record:")
    roll_number = input("Enter roll number to search: ").strip()
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, roll_number, grade FROM students WHERE roll_number = ?', (roll_number,))
        record = cursor.fetchone()
        if not record:
            print("No student found with that roll number.\n")
            return
        print(f"Found: ID={record[0]}, Name={record[1]}, Roll Number={record[2]}, Grade={record[3]}")
        print("Enter new details (leave blank to keep current value):")
        new_name = input(f"New name [{record[1]}]: ").strip()
        if new_name:
            if not validate_name(new_name):
                print("Invalid name. Update cancelled.\n")
                return
        else:
            new_name = record[1]
        new_grade = input(f"New grade [{record[3]}] (A-F): ").strip().upper()
        if new_grade:
            if not validate_grade(new_grade):
                print("Invalid grade. Update cancelled.\n")
                return
        else:
            new_grade = record[3]
        cursor.execute('UPDATE students SET name = ?, grade = ? WHERE roll_number = ?', (new_name, new_grade, roll_number))
        conn.commit()
        print("Student record updated successfully!\n")

def delete_student():
    print("\nDelete Student Record:")
    roll_number = input("Enter roll number to delete: ").strip()
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM students WHERE roll_number = ?', (roll_number,))
        if not cursor.fetchone():
            print("No student found with that roll number.\n")
            return
        cursor.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
        conn.commit()
        print("Student record deleted successfully!\n")

def save_to_csv():
    filename = 'students.csv'
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, roll_number, grade FROM students')
        records = cursor.fetchall()
        if not records:
            print("No records to save.\n")
            return
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Name', 'Roll Number', 'Grade'])
            writer.writerows(records)
        print(f"Records saved to {filename} in {os.getcwd()}\n")

def main_menu():
    while True:
        print("="*40)
        print("  Welcome to School Report Card Manager  ")
        print("="*40)
        print("Main Menu:")
        print("1) Load and display all student records")
        print("2) Add new student record")
        print("3) Search and update student details")
        print("4) Delete student record by roll number")
        print("5) Save table as .csv file")
        print("6) Exit")
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            display_all_students()
            print("Task completed. Returning to main menu.\n")
        elif choice == '2':
            add_student()
            print("Task completed. Returning to main menu.\n")
        elif choice == '3':
            search_and_update_student()
            print("Task completed. Returning to main menu.\n")
        elif choice == '4':
            delete_student()
            print("Task completed. Returning to main menu.\n")
        elif choice == '5':
            save_to_csv()
            print("Task completed. Returning to main menu.\n")
        elif choice == '6':
            print("Thank you for using the School Report Card Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.\n")

if __name__ == "__main__":
    create_table()
    main_menu()

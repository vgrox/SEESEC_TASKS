import csv
import os
from typing import List, Dict, Optional

def read_csv_file(filename: str = "students.csv") -> List[Dict]:
    students = []
    
    try:
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found!")
            return students
            
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    student = process_student_row(row, row_num)
                    if student:
                        students.append(student)
                except Exception as e:
                    print(f"Warning: Error processing row {row_num}: {e}")
                    continue
                    
        print(f"Successfully read {len(students)} student records from '{filename}'")
        return students
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return students
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'")
        return students
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}'. Please check file encoding.")
        return students
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        return students


def process_student_row(row: Dict[str, str], row_num: int) -> Optional[Dict]:
    try:
        student_id = row.get('Student_ID', '').strip()
        name = row.get('Name', '').strip()
        
        if not student_id or not name:
            print(f"Warning: Row {row_num}: Missing Student_ID or Name")
            return None
        
        marks = []
        subject_names = []
        
        for key, value in row.items():
            if key.lower().endswith('_marks') or key.lower().endswith('_mark'):
                subject_name = key.replace('_marks', '').replace('_mark', '').replace('_', ' ').title()
                subject_names.append(subject_name)
                
                try:
                    mark = float(value.strip()) if value.strip() else 0.0
                    if mark < 0 or mark > 100:
                        print(f"Warning: Row {row_num}, {subject_name}: Mark {mark} is out of range (0-100)")
                        mark = 0.0
                    marks.append(mark)
                except ValueError:
                    print(f"Warning: Row {row_num}, {subject_name}: Invalid mark '{value}', setting to 0")
                    marks.append(0.0)
        
        if not marks:
            print(f"Warning: Row {row_num}: No valid marks found")
            return None
        
        total_marks = sum(marks)
        average_marks = total_marks / len(marks)
        
        student_data = {
            'student_id': student_id,
            'name': name,
            'marks': marks,
            'subject_names': subject_names,
            'total_marks': total_marks,
            'average_marks': round(average_marks, 2),
            'num_subjects': len(marks)
        }
        
        return student_data
        
    except Exception as e:
        print(f"Error processing row {row_num}: {e}")
        return None


def calculate_total_and_average(students: List[Dict]) -> None:
    if not students:
        print("No student data available for analysis.")
        return
    
    print("\n" + "="*60)
    print("STUDENT MARKS ANALYSIS")
    print("="*60)
    
    for student in students:
        print(f"\nStudent ID: {student['student_id']}")
        print(f"Name: {student['name']}")
        print(f"Subjects: {', '.join(student['subject_names'])}")
        print(f"Marks: {student['marks']}")
        print(f"Total Marks: {student['total_marks']}")
        print(f"Average Marks: {student['average_marks']}%")
        print("-" * 40)


def find_top_scorer(students: List[Dict]) -> Optional[Dict]:
    if not students:
        print("No students to find top scorer.")
        return None
    
    top_scorer = max(students, key=lambda x: x['average_marks'])
    
    print(f"\n🏆 TOP SCORER 🏆")
    print(f"Name: {top_scorer['name']}")
    print(f"Student ID: {top_scorer['student_id']}")
    print(f"Average Marks: {top_scorer['average_marks']}%")
    print(f"Total Marks: {top_scorer['total_marks']}")
    
    return top_scorer


def display_class_statistics(students: List[Dict]) -> None:
    if not students:
        print("No student data available for class statistics.")
        return
    
    averages = [student['average_marks'] for student in students]
    totals = [student['total_marks'] for student in students]
    
    class_avg = sum(averages) / len(averages)
    class_total_avg = sum(totals) / len(totals)
    
    print(f"\n📊 CLASS STATISTICS 📊")
    print(f"Total Students: {len(students)}")
    print(f"Class Average: {round(class_avg, 2)}%")
    print(f"Average Total Marks: {round(class_total_avg, 2)}")
    print(f"Highest Average: {max(averages)}%")
    print(f"Lowest Average: {min(averages)}%")


def export_results(students: List[Dict], top_scorer: Optional[Dict], output_filename: str = "student_analysis.txt") -> None:
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("STUDENT MARKS ANALYSIS REPORT\n")
            file.write("=" * 50 + "\n\n")
            
            for student in students:
                file.write(f"Student ID: {student['student_id']}\n")
                file.write(f"Name: {student['name']}\n")
                file.write(f"Total Marks: {student['total_marks']}\n")
                file.write(f"Average Marks: {student['average_marks']}%\n")
                file.write("-" * 30 + "\n")
            
            if top_scorer:
                file.write(f"\nTOP SCORER:\n")
                file.write(f"Name: {top_scorer['name']}\n")
                file.write(f"Average: {top_scorer['average_marks']}%\n")
        
        print(f"\n✅ Analysis exported to '{output_filename}'")
        
    except Exception as e:
        print(f"Error exporting results: {e}")


def main():
    print("🎓 STUDENT CSV READER AND ANALYZER 🎓")
    print("=" * 50)
    
    students = read_csv_file('students.csv')
    
    if students:
        calculate_total_and_average(students)
        
        top_scorer = find_top_scorer(students)
        
        display_class_statistics(students)
        
        export_results(students, top_scorer)
        
        print(f"\n✅ Analysis completed successfully!")
    else:
        print("❌ Failed to read CSV file. Please check the file and try again.")


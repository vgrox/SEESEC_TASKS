import csv

student_id = input("Enter student ID: ")
student_name = input("Enter student name: ")
marks = []
for i in range(1, 4):
    mark = input(f"Enter marks for subject {i}: ")
    marks.append(mark)

row = [student_id, student_name] + marks

with open('students.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(row)

print("Data written successfully to students.csv.")

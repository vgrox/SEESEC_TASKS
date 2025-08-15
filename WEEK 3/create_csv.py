import pandas as pd

data = {
    "name": ["Rohan", "Raman", "Arnav", "Aryan", "Rishi"],
    "math": [85, 78, 60, 92, 55],
    "science": [90, 82, 58, 95, 50],
    "english": [88, 80, 65, 94, 52],
    "grade": ["A", "B", "C", "A", "D"],
    "hours_studied": [15, 12, 8, 20, 5],
    "pass_fail": ["Pass", "Pass", "Fail", "Pass", "Fail"]
}

df = pd.DataFrame(data)
df.to_csv("students.csv", index=False)

print("students.csv created successfully!")
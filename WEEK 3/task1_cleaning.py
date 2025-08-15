import pandas as pd
import numpy as np

df = pd.read_csv("students.csv")
print("\nHEAD:")
print(df.head(10))
print("\nINFO:")
print(df.info())
print("\nDESCRIBE (numeric):")
print(df.describe())

num_cols = df.select_dtypes(include=[np.number]).columns
cat_cols = df.select_dtypes(exclude=[np.number]).columns

df[num_cols] = df[num_cols].fillna(df[num_cols].median())
for c in cat_cols:
    df[c] = df[c].fillna(df[c].mode().iloc[0])

print("\nNULLS AFTER FILL:")
print(df.isna().sum())

df["total"] = df[["math","science","english"]].sum(axis=1)

df["average"] = df[["math","science","english"]].mean(axis=1)

def to_grade(x):
    if x >= 85: return "A"
    if x >= 70: return "B"
    if x >= 55: return "C"
    if x >= 40: return "D"
    return "F"

if "grade" not in df.columns:
    df["grade"] = df["average"].apply(to_grade)

print("\nPREVIEW WITH DERIVED COLUMNS:")
print(df.head())

df.to_csv("students_clean.csv", index=False)
print("\nSaved -> students_clean.csv")

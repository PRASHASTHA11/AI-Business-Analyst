import pandas as pd

file_path = "data/sales_data.xlsx"

df = pd.read_excel(file_path)

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
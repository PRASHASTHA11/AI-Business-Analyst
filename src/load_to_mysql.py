import pandas as pd
import mysql.connector

# Read Excel
df = pd.read_excel("data/sales_data.xlsx")

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Student@123",
    database="ai_business_analyst"
)

cursor = connection.cursor()

# Insert data
query = """
INSERT INTO sales (
    Order_ID,
    Order_Date,
    Customer_ID,
    Customer_Name,
    Region,
    Category,
    Sub_Category,
    Product_Name,
    Sales,
    Quantity,
    Discount,
    Profit
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    values = tuple(row)
    cursor.execute(query, values)

connection.commit()

print("Excel data successfully loaded into MySQL!")

cursor.close()
connection.close()
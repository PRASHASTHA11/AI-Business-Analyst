import pandas as pd

df = pd.read_excel("data/sales_data.xlsx")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.month

monthly_sales = df.groupby("Month")["Sales"].sum()

march_sales = monthly_sales[3]
april_sales = monthly_sales[4]

sales_change = march_sales - april_sales
sales_change_percentage = (sales_change / march_sales) * 100

print("March Sales:", march_sales)
print("April Sales:", april_sales)
print("Sales Decrease:", sales_change)
print("Sales Decrease %:", round(sales_change_percentage, 2))
regional_sales = df.groupby(["Region", "Month"])["Sales"].sum().unstack()

regional_sales["Change"] = (
    regional_sales[4] - regional_sales[3]
)

print("\nRegional Sales:")
print(regional_sales)
product_sales = df.groupby(["Product_Name", "Month"])["Sales"].sum().unstack(fill_value=0)

product_sales["Change"] = (
    product_sales[4] - product_sales[3]
)

print("\nProduct Sales Changes:")
print(product_sales.sort_values("Change"))
biggest_decline = product_sales["Change"].idxmin()
decline_amount = product_sales["Change"].min()

print("\nBiggest Product Decline:")
print(biggest_decline, ":", decline_amount)
march_customers = set(df[df["Month"] == 3]["Customer_Name"])
april_customers = set(df[df["Month"] == 4]["Customer_Name"])

missing_customers = march_customers - april_customers

print("\nCustomers who purchased in March but not April:")
print(missing_customers)
lost_customer_sales = df[
    (df["Month"] == 3) &
    (df["Customer_Name"].isin(missing_customers))
]["Sales"].sum()

print("\nSales from customers who didn't return in April:")
print(lost_customer_sales)
monthly_profit = df.groupby("Month")["Profit"].sum()

march_profit = monthly_profit[3]
april_profit = monthly_profit[4]

profit_change = march_profit - april_profit
profit_change_percentage = (profit_change / march_profit) * 100

print("\nProfit Analysis:")
print("March Profit:", march_profit)
print("April Profit:", april_profit)
print("Profit Decrease:", profit_change)
print("Profit Decrease %:", round(profit_change_percentage, 2))
march_margin = (march_profit / march_sales) * 100
april_margin = (april_profit / april_sales) * 100

print("\nProfit Margin:")
print("March Profit Margin:", round(march_margin, 2), "%")
print("April Profit Margin:", round(april_margin, 2), "%")
march_margin = (march_profit / march_sales) * 100
april_margin = (april_profit / april_sales) * 100

print("\nProfit Margin:")
print("March Profit Margin:", round(march_margin, 2), "%")
print("April Profit Margin:", round(april_margin, 2), "%")
loss_orders = df[
    (df["Month"] == 4) &
    (df["Profit"] < 0)
]

print("\nLoss-making April Orders:")
print(
    loss_orders[
        ["Order_ID", "Product_Name", "Sales", "Discount", "Profit"]
    ]
)
total_loss = loss_orders["Profit"].sum()

print("\nTotal Loss from April Orders:")
print(total_loss)
discount_profit = df.groupby("Discount").agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum")
)

discount_profit["profit_margin"] = (
    discount_profit["total_profit"]
    / discount_profit["total_sales"]
    * 100
).round(2)

print("\nDiscount vs Profit:")
print(discount_profit)
print("\n========== BUSINESS INSIGHT ==========")

print(
    f"Sales decreased by ₹{sales_change:,.0f} "
    f"({sales_change_percentage:.2f}%) from March to April."
)

print(
    f"Profit decreased by ₹{profit_change:,.0f} "
    f"({profit_change_percentage:.2f}%)."
)

print(
    f"Profit margin changed from {march_margin:.2f}% "
    f"to {april_margin:.2f}%."
)

print(
    f"The biggest product-level decline was "
    f"{biggest_decline}, with a decrease of ₹{abs(decline_amount):,.0f}."
)

print(
    f"Customers who purchased in March but not April "
    f"accounted for ₹{lost_customer_sales:,.0f} in March sales."
)

print(
    f"April loss-making orders resulted in a total loss "
    f"of ₹{abs(total_loss):,.0f}."
)
import matplotlib.pyplot as plt

monthly_sales = df.groupby("Month")["Sales"].sum()

plt.bar(
    ["March", "April"],
    monthly_sales.values
)

plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.show()
# Regional Sales Change

regional_sales = df.groupby(["Region", "Month"])["Sales"].sum().unstack(fill_value=0)

regional_sales["Change"] = (
    regional_sales[4] - regional_sales[3]
)

regional_sales["Change"].plot(
    kind="bar",
    title="Regional Sales Change: March to April"
)

plt.xlabel("Region")
plt.ylabel("Sales Change")

plt.axhline(0)
plt.show()
# Product Sales Change

product_sales = df.groupby(
    ["Product_Name", "Month"]
)["Sales"].sum().unstack(fill_value=0)

product_sales["Change"] = (
    product_sales[4] - product_sales[3]
)

product_sales["Change"].sort_values().plot(
    kind="bar",
    title="Product Sales Change: March to April"
)

plt.xlabel("Product")
plt.ylabel("Sales Change")

plt.axhline(0)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
print("\n========== BUSINESS ANALYST REPORT ==========")

# 1. Overall sales
print(
    f"\n1. SALES PERFORMANCE"
    f"\nSales decreased from ₹{march_sales:,.0f} "
    f"to ₹{april_sales:,.0f}."
)

print(
    f"Overall decline: ₹{sales_change:,.0f} "
    f"({sales_change_percentage:.2f}%)."
)


# 2. Region causing the largest decline
largest_region_decline = regional_sales["Change"].idxmin()
largest_region_amount = regional_sales["Change"].min()

print(
    f"\n2. REGIONAL DRIVER"
    f"\n{largest_region_decline} had the largest sales decline "
    f"of ₹{abs(largest_region_amount):,.0f}."
)


# 3. Product causing the largest decline
largest_product_decline = product_sales["Change"].idxmin()
largest_product_amount = product_sales["Change"].min()

print(
    f"\n3. PRODUCT DRIVER"
    f"\n{largest_product_decline} had the largest "
    f"product-level decline of ₹{abs(largest_product_amount):,.0f}."
)


# 4. Profit
print(
    f"\n4. PROFITABILITY"
    f"\nProfit decreased from ₹{march_profit:,.0f} "
    f"to ₹{april_profit:,.0f}."
)

print(
    f"Profit margin changed from "
    f"{march_margin:.2f}% to {april_margin:.2f}%."
)


# 5. Loss-making orders
print(
    f"\n5. LOSS-MAKING ORDERS"
    f"\nApril loss-making orders resulted in "
    f"₹{abs(total_loss):,.0f} total loss."
)


print("\n==============================================")
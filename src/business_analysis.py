
import pandas as pd
import mysql.connector
import streamlit as st


def analyze_sales():

    # 1. Connect to MySQL
    connection = mysql.connector.connect(
    **st.secrets["mysql"]
    )
    try:
        # 2. Fetch data from MySQL
        df = pd.read_sql(
            "SELECT * FROM sales",
            connection
        )

    finally:
        connection.close()

    # 3. Prepare data
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month

    # 4. Monthly sales analysis
    monthly_sales = df.groupby("Month")["Sales"].sum()

    march_sales = monthly_sales.get(3, 0)
    april_sales = monthly_sales.get(4, 0)

    sales_decline = march_sales - april_sales

    sales_decline_percentage = (
        sales_decline / march_sales * 100
        if march_sales != 0 else 0
    )

    # 5. Regional analysis
    regional_sales = (
        df.groupby(["Region", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    regional_sales["Change"] = (
        regional_sales[4] - regional_sales[3]
    )

    largest_region = regional_sales["Change"].idxmin()

    largest_region_decline = abs(
        regional_sales["Change"].min()
    )

    # 6. Product analysis
    product_sales = (
        df.groupby(["Product_Name", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    product_sales["Change"] = (
        product_sales[4] - product_sales[3]
    )

    largest_product = product_sales["Change"].idxmin()

    largest_product_decline = abs(
        product_sales["Change"].min()
    )

    # 7. Profit analysis
    monthly_profit = df.groupby("Month")["Profit"].sum()

    march_profit = monthly_profit.get(3, 0)
    april_profit = monthly_profit.get(4, 0)

    profit_decline = march_profit - april_profit

    # 8. Return results
    return {
        "march_sales": march_sales,
        "april_sales": april_sales,
        "sales_decline": sales_decline,
        "sales_decline_percentage": sales_decline_percentage,

        "largest_region": largest_region,
        "largest_region_decline": largest_region_decline,

        "largest_product": largest_product,
        "largest_product_decline": largest_product_decline,

        "march_profit": march_profit,
        "april_profit": april_profit,
        "profit_decline": profit_decline
    }


# 9. Test the function
if __name__ == "__main__":

    result = analyze_sales()

    print("\n========== MYSQL BUSINESS ANALYSIS ==========")

    print("March Sales:", result["march_sales"])
    print("April Sales:", result["april_sales"])

    print("Sales Decline:", result["sales_decline"])

    print(
        "Sales Decline Percentage:",
        round(result["sales_decline_percentage"], 2), "%"
    )

    print(
        "Largest Regional Decline:",
        result["largest_region"]
    )

    print(
        "Largest Product Decline:",
        result["largest_product"]
    )

    print("Profit Decline:", result["profit_decline"])

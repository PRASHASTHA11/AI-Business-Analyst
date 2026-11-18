
import pandas as pd


def detect_business_changes(df):

    df = df.copy()

    # Prepare data
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month

    march = df[df["Month"] == 3]
    april = df[df["Month"] == 4]

    # 1. Overall sales comparison
    march_sales = march["Sales"].sum()
    april_sales = april["Sales"].sum()

    sales_change = april_sales - march_sales

    sales_change_percentage = (
        sales_change / march_sales * 100
        if march_sales != 0 else 0
    )

    # 2. Regional sales comparison
    regional = (
        df.groupby(["Region", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    regional["Change"] = regional[4] - regional[3]

    regional["Change_Percentage"] = (
        regional["Change"] / regional[3].replace(0, pd.NA) * 100
    )

    largest_region_decline = regional["Change"].idxmin()
    largest_region_increase = regional["Change"].idxmax()

    # 3. Product sales comparison
    product = (
        df.groupby(["Product_Name", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    product["Change"] = product[4] - product[3]

    largest_product_decline = product["Change"].idxmin()
    largest_product_increase = product["Change"].idxmax()

    # 4. Category sales comparison
    category = (
        df.groupby(["Category", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    category["Change"] = category[4] - category[3]

    # 5. Customers who purchased in March but not April
    march_customers = set(march["Customer_ID"].dropna())
    april_customers = set(april["Customer_ID"].dropna())

    inactive_customers = march_customers - april_customers

    # 6. Products with increased sales
    improved_products = (
        product[product["Change"] > 0]
        .sort_values("Change", ascending=False)
    )

    # 7. Products with decreased sales
    declining_products = (
        product[product["Change"] < 0]
        .sort_values("Change")
    )

    return {
        "march_sales": march_sales,
        "april_sales": april_sales,
        "sales_change": sales_change,
        "sales_change_percentage": sales_change_percentage,

        "regional": regional,
        "largest_region_decline": largest_region_decline,
        "largest_region_increase": largest_region_increase,

        "product": product,
        "largest_product_decline": largest_product_decline,
        "largest_product_increase": largest_product_increase,

        "category": category,
        "inactive_customers": sorted(inactive_customers),

        "improved_products": improved_products,
        "declining_products": declining_products
    }

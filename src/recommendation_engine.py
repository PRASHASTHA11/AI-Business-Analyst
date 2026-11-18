
import pandas as pd


def generate_recommendations(df):

    recommendations = []

    # Prepare dates and month information
    df = df.copy()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month

    # 1. Find the region with the largest sales decline
    regional_sales = (
        df.groupby(["Region", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    regional_sales["Change"] = (
        regional_sales[4] - regional_sales[3]
    )

    worst_region = regional_sales["Change"].idxmin()
    region_decline = abs(regional_sales["Change"].min())

    recommendations.append(
        f"Focus on the {worst_region} region. "
        f"Its sales declined by ₹{region_decline:,.0f} "
        f"from March to April. Investigate local demand "
        f"and sales performance."
    )

    # 2. Find the product with the largest sales decline
    product_sales = (
        df.groupby(["Product_Name", "Month"])["Sales"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=[3, 4], fill_value=0)
    )

    product_sales["Change"] = (
        product_sales[4] - product_sales[3]
    )

    worst_product = product_sales["Change"].idxmin()
    product_decline = abs(product_sales["Change"].min())

    recommendations.append(
        f"Review demand for {worst_product}. "
        f"Its sales declined by ₹{product_decline:,.0f}. "
        f"Check product demand, pricing and availability."
    )

    # 3. Find customers who did not return in April
    march_customers = set(
        df[df["Month"] == 3]["Customer_ID"]
    )

    april_customers = set(
        df[df["Month"] == 4]["Customer_ID"]
    )

    lost_customers = march_customers - april_customers

    if lost_customers:

        recommendations.append(
            f"{len(lost_customers)} customers who purchased "
            f"in March did not purchase in April. "
            f"Consider targeted customer follow-ups."
        )

    # 4. Identify loss-making April orders
    loss_orders = df[
        (df["Month"] == 4) &
        (df["Profit"] < 0)
    ]

    if not loss_orders.empty:

        total_loss = abs(loss_orders["Profit"].sum())

        recommendations.append(
            f"Review {len(loss_orders)} loss-making April orders. "
            f"Together, they generated a loss of "
            f"₹{total_loss:,.0f}. Check discounts and costs."
        )

    return recommendations

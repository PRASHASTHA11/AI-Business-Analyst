
import pandas as pd


def simulate_business_scenario(
    df,
    sales_growth_pct=0,
    discount_reduction_pct=0
):

    df = df.copy()

    # Prepare dates
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month

    # Use April as the baseline
    april = df[df["Month"] == 4]

    if april.empty:
        raise ValueError("No April data available for simulation.")

    # Actual April performance
    actual_sales = april["Sales"].sum()
    actual_profit = april["Profit"].sum()

    # Calculate actual profit margin
    profit_margin = (
        actual_profit / actual_sales * 100
        if actual_sales != 0 else 0
    )

    # Apply expected sales growth
    projected_sales = (
        actual_sales * (1 + sales_growth_pct / 100)
    )

    # Estimate profit from sales growth
    estimated_profit = (
        projected_sales * profit_margin / 100
    )

    # Estimate the impact of reducing discounts
    discount_impact = (
        actual_sales * discount_reduction_pct / 100
    )

    projected_profit = estimated_profit + discount_impact

    # Calculate changes
    additional_sales = projected_sales - actual_sales
    additional_profit = projected_profit - actual_profit

    return {
        "actual_sales": actual_sales,
        "actual_profit": actual_profit,
        "profit_margin": profit_margin,
        "projected_sales": projected_sales,
        "projected_profit": projected_profit,
        "additional_sales": additional_sales,
        "additional_profit": additional_profit,
        "discount_impact": discount_impact
    }


import streamlit as st
import sys
import os
import pandas as pd
import mysql.connector

# Add src folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src")
    )
)

from business_analysis import analyze_sales
from recommendation_engine import generate_recommendations
from change_detection import detect_business_changes
from what_if_simulator import simulate_business_scenario
from report_export import create_excel_report, create_pdf_report


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("AI Business Analyst Assistant")
st.write("Analyze sales performance and identify important business trends.")


# LOAD DATA FROM MYSQL
@st.cache_data(ttl=60)
def load_sales_data():

    connection = mysql.connector.connect(
        **st.secrets["mysql"]
    )

    try:
        df = pd.read_sql("SELECT * FROM sales", connection)
    finally:
        connection.close()

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month

    return df


try:
    df = load_sales_data()

except Exception as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()


# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
months = ["All", "March", "April"]

selected_region = st.sidebar.selectbox("Select Region", regions)
selected_category = st.sidebar.selectbox("Select Category", categories)
selected_month = st.sidebar.selectbox("Select Month", months)


# APPLY FILTERS
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_month == "March":
    filtered_df = filtered_df[filtered_df["Month"] == 3]
elif selected_month == "April":
    filtered_df = filtered_df[filtered_df["Month"] == 4]


if selected_month == "March":
    months_to_show = [3]
elif selected_month == "April":
    months_to_show = [4]
else:
    months_to_show = [3, 4]

month_names = {3: "March", 4: "April"}


# SALES PERFORMANCE DASHBOARD
st.subheader("Sales Performance Dashboard")

if filtered_df.empty:
    st.warning("No data available for the selected filters.")

else:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order_ID"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("Total Profit", f"₹{total_profit:,.0f}")
    col3.metric("Total Orders", total_orders)

    st.subheader("Monthly Sales")

    monthly_sales = (
        filtered_df.groupby("Month")["Sales"]
        .sum()
        .reindex(months_to_show, fill_value=0)
    )

    monthly_sales.index = [
        month_names[month] for month in months_to_show
    ]

    st.bar_chart(monthly_sales)

    st.subheader("Monthly Profit")

    monthly_profit = (
        filtered_df.groupby("Month")["Profit"]
        .sum()
        .reindex(months_to_show, fill_value=0)
    )

    monthly_profit.index = [
        month_names[month] for month in months_to_show
    ]

    st.bar_chart(monthly_profit)

    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

    st.subheader("Sales by Region")

    regional_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(regional_sales)


# PREPARE REPORT DATA
changes = None
scenario = None


# AUTOMATIC BUSINESS CHANGE DETECTION
st.divider()
st.header("Automatic Business Change Detection")

st.write(
    "Automatically identify important changes between March and April."
)

try:
    changes = detect_business_changes(df)

    st.subheader("Overall Sales Comparison")

    col1, col2, col3 = st.columns(3)

    col1.metric("March Sales", f"₹{changes['march_sales']:,.0f}")
    col2.metric("April Sales", f"₹{changes['april_sales']:,.0f}")

    col3.metric(
        "Sales Change",
        f"₹{changes['sales_change']:,.0f}",
        delta=f"{changes['sales_change_percentage']:.2f}%"
    )

    st.subheader("Regional Sales Changes")

    regional_table = changes["regional"][[3, 4, "Change"]].copy()
    regional_table.columns = ["March Sales", "April Sales", "Sales Change"]

    st.dataframe(
        regional_table.style.format("₹{:,.0f}"),
        use_container_width=True
    )

    st.write(
        f"**Largest regional decline:** "
        f"{changes['largest_region_decline']}"
    )

    st.subheader("Category Sales Changes")

    category_table = changes["category"][[3, 4, "Change"]].copy()
    category_table.columns = ["March Sales", "April Sales", "Sales Change"]

    st.dataframe(
        category_table.style.format("₹{:,.0f}"),
        use_container_width=True
    )

    st.subheader("Product Performance Changes")

    tab1, tab2 = st.tabs(["Declining Products", "Improving Products"])

    with tab1:
        declining = changes["declining_products"][
            [3, 4, "Change"]
        ].head(5).copy()

        declining.columns = ["March Sales", "April Sales", "Sales Change"]

        st.dataframe(
            declining.style.format("₹{:,.0f}"),
            use_container_width=True
        )

    with tab2:
        improving = changes["improved_products"][
            [3, 4, "Change"]
        ].head(5).copy()

        improving.columns = ["March Sales", "April Sales", "Sales Change"]

        st.dataframe(
            improving.style.format("₹{:,.0f}"),
            use_container_width=True
        )

    st.subheader("Customer Activity Changes")

    inactive_customers = changes["inactive_customers"]

    if inactive_customers:
        st.write(
            f"**{len(inactive_customers)} customers** purchased in March "
            "but did not purchase in April:"
        )
        st.write(", ".join(map(str, inactive_customers)))
    else:
        st.success("All March customers also purchased in April.")

    # BUSINESS CHANGE SUMMARY
    st.divider()
    st.header("Business Change Summary")

    regional_decline = changes["regional"]["Change"].min()
    category_decline = changes["category"]["Change"].min()
    product_decline = changes["product"]["Change"].min()

    biggest_region = changes["regional"]["Change"].idxmin()
    biggest_category = changes["category"]["Change"].idxmin()
    biggest_product = changes["product"]["Change"].idxmin()

    st.write(
        f"Between March and April, sales decreased by "
        f"₹{abs(changes['sales_change']):,.0f} "
        f"({abs(changes['sales_change_percentage']):.2f}%)."
    )

    st.write(
        f"**Regional change:** {biggest_region} recorded the largest "
        f"regional decline of ₹{abs(regional_decline):,.0f}."
    )

    st.write(
        f"**Category change:** {biggest_category} recorded the largest "
        f"category decline of ₹{abs(category_decline):,.0f}."
    )

    st.write(
        f"**Product change:** {biggest_product} recorded the largest "
        f"product decline of ₹{abs(product_decline):,.0f}."
    )

    st.write(
        f"**Customer activity:** {len(inactive_customers)} customers "
        "who purchased in March did not purchase in April."
    )

    st.info(
        "These findings describe observed changes. Further investigation "
        "is needed to establish their causes."
    )

except Exception as e:
    st.error(f"Business change detection error: {e}")


# WHAT-IF BUSINESS SIMULATOR
st.divider()
st.header("What-If Business Simulator")

st.write(
    "Explore how different sales growth and discount scenarios "
    "could affect April's revenue and profit."
)

sales_growth = st.slider(
    "Expected sales growth (%)",
    min_value=0,
    max_value=30,
    value=10,
    step=1
)

discount_reduction = st.slider(
    "Discount reduction (percentage points)",
    min_value=0,
    max_value=10,
    value=2,
    step=1
)

try:
    scenario = simulate_business_scenario(
        df,
        sales_growth_pct=sales_growth,
        discount_reduction_pct=discount_reduction
    )

    st.subheader("Scenario Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Actual April Revenue",
        f"₹{scenario['actual_sales']:,.0f}"
    )

    col2.metric(
        "Simulated Revenue",
        f"₹{scenario['projected_sales']:,.0f}",
        delta=f"₹{scenario['additional_sales']:,.0f}"
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "Actual April Profit",
        f"₹{scenario['actual_profit']:,.0f}"
    )

    col4.metric(
        "Simulated Profit",
        f"₹{scenario['projected_profit']:,.0f}",
        delta=f"₹{scenario['additional_profit']:,.0f}"
    )

    st.subheader("Actual vs Simulated Performance")

    comparison = pd.DataFrame({
        "Actual": [
            scenario["actual_sales"],
            scenario["actual_profit"]
        ],
        "Simulated": [
            scenario["projected_sales"],
            scenario["projected_profit"]
        ]
    }, index=["Revenue", "Profit"])

    st.bar_chart(comparison)

    st.subheader("Scenario Explanation")

    st.write(
        f"With an assumed sales growth of {sales_growth}% "
        f"and a discount reduction of {discount_reduction} "
        "percentage points:"
    )

    st.write(
        f"- Estimated additional revenue: "
        f"₹{scenario['additional_sales']:,.0f}"
    )

    st.write(
        f"- Estimated additional profit: "
        f"₹{scenario['additional_profit']:,.0f}"
    )

    st.caption(
        "This is a simplified scenario calculation, not a forecast. "
        "It assumes April's profit margin remains constant and that "
        "each percentage-point discount reduction improves profit "
        "by 1% of baseline revenue, without changing sales volume."
    )

except Exception as e:
    st.error(f"Simulator error: {e}")


# BUSINESS QUESTION INPUT
st.divider()
st.subheader("Ask Your Business Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Why did sales decrease from March to April?"
)

if st.button("Analyze Sales"):

    if not question.strip():
        st.warning("Please enter a business question.")

    else:
        try:
            result = analyze_sales()
            question_lower = question.lower().strip()

            sales_words = ["sales", "revenue", "turnover"]

            decline_words = [
                "decrease", "decreased", "drop", "dropped",
                "decline", "declined", "fall", "fell",
                "down", "lower"
            ]

            profit_words = ["profit", "profitability", "margin"]
            region_words = ["region", "regional", "area"]
            product_words = ["product", "item", "product-wise"]

            st.subheader("Business Answer")

            if (
                any(word in question_lower for word in sales_words)
                and any(word in question_lower for word in decline_words)
            ):
                st.write(
                    f"Sales decreased from ₹{result['march_sales']:,.0f} "
                    f"in March to ₹{result['april_sales']:,.0f} in April."
                )

                st.write(
                    f"That is a decline of ₹{result['sales_decline']:,.0f} "
                    f"({result['sales_decline_percentage']:.2f}%)."
                )

                st.write(
                    f"The region with the largest decline was "
                    f"**{result['largest_region']}**, with a decline of "
                    f"₹{result['largest_region_decline']:,.0f}."
                )

            elif any(word in question_lower for word in profit_words):
                st.write(
                    f"Profit was ₹{result['march_profit']:,.0f} in March "
                    f"and ₹{result['april_profit']:,.0f} in April."
                )

                st.write(
                    f"Profit decreased by ₹{result['profit_decline']:,.0f}."
                )

            elif any(word in question_lower for word in region_words):
                st.write(
                    f"{result['largest_region']} had the largest regional "
                    f"sales decline of ₹{result['largest_region_decline']:,.0f}."
                )

            elif any(word in question_lower for word in product_words):
                st.write(
                    f"{result['largest_product']} had the largest "
                    f"product-level decline of "
                    f"₹{result['largest_product_decline']:,.0f}."
                )

            else:
                st.info(
                    "I can currently answer questions about sales "
                    "declines, profit, regions, and products."
                )

            st.subheader("Key Findings")

            st.write(
                f"**Regional driver:** {result['largest_region']} "
                f"declined by ₹{result['largest_region_decline']:,.0f}."
            )

            st.write(
                f"**Product driver:** {result['largest_product']} "
                f"declined by ₹{result['largest_product_decline']:,.0f}."
            )

            st.write(
                f"**Profit:** decreased by "
                f"₹{result['profit_decline']:,.0f}."
            )

            st.subheader("Business Recommendations")

            recommendations = generate_recommendations(df)

            for i, recommendation in enumerate(recommendations, start=1):
                st.write(f"**{i}.** {recommendation}")

            st.caption(
                "Recommendations use the complete March–April dataset, "
                "not just the selected dashboard filters."
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# EXPORT BUSINESS REPORTS
st.divider()
st.header("Export Business Reports")

st.write(
    "Download your sales analysis and What-If scenario as Excel or PDF reports."
)

if changes is not None and scenario is not None:

    try:
        excel_data = create_excel_report(df, changes, scenario)
        pdf_data = create_pdf_report(df, changes, scenario)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Excel Report",
                data=excel_data,
                file_name="AI_Business_Analysis_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with col2:
            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name="AI_Business_Analysis_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Could not generate reports: {e}")

else:
    st.warning(
        "Reports are unavailable because the business analysis "
        "or simulator could not be completed."
    )

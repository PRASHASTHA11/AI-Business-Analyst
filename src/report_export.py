
import pandas as pd
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def create_excel_report(df, changes, scenario):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # Complete sales data
        df.to_excel(
            writer,
            sheet_name="Sales Data",
            index=False
        )

        # Regional comparison
        regional = changes["regional"].copy()
        regional.to_excel(
            writer,
            sheet_name="Regional Analysis"
        )

        # Category comparison
        category = changes["category"].copy()
        category.to_excel(
            writer,
            sheet_name="Category Analysis"
        )

        # Product comparison
        product = changes["product"].copy()
        product.to_excel(
            writer,
            sheet_name="Product Analysis"
        )

        # What-if scenario
        scenario_df = pd.DataFrame({
            "Metric": [
                "Actual April Revenue",
                "Simulated Revenue",
                "Actual April Profit",
                "Simulated Profit",
                "Additional Revenue",
                "Additional Profit"
            ],
            "Value": [
                scenario["actual_sales"],
                scenario["projected_sales"],
                scenario["actual_profit"],
                scenario["projected_profit"],
                scenario["additional_sales"],
                scenario["additional_profit"]
            ]
        })

        scenario_df.to_excel(
            writer,
            sheet_name="What-If Analysis",
            index=False
        )

    output.seek(0)

    return output.getvalue()


def create_pdf_report(df, changes, scenario):

    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()
    story = []

    # TITLE
    story.append(
        Paragraph(
            "AI Business Analyst - Business Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 15))

    # OVERALL SUMMARY
    story.append(
        Paragraph("1. Overall Sales Performance", styles["Heading2"])
    )

    summary_data = [
        ["Metric", "Value"],
        ["March Sales", f"Rs. {changes['march_sales']:,.0f}"],
        ["April Sales", f"Rs. {changes['april_sales']:,.0f}"],
        [
            "Sales Change",
            f"Rs. {changes['sales_change']:,.0f}"
        ],
        [
            "Sales Change Percentage",
            f"{changes['sales_change_percentage']:.2f}%"
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[220, 220]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 18))

    # REGIONAL ANALYSIS
    story.append(
        Paragraph("2. Regional Sales Changes", styles["Heading2"])
    )

    regional_data = [
        ["Region", "March Sales", "April Sales", "Change"]
    ]

    for region, row in changes["regional"].iterrows():

        regional_data.append([
            str(region),
            f"Rs. {row[3]:,.0f}",
            f"Rs. {row[4]:,.0f}",
            f"Rs. {row['Change']:,.0f}"
        ])

    regional_table = Table(regional_data)

    regional_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    story.append(regional_table)
    story.append(Spacer(1, 18))

    # CATEGORY ANALYSIS
    story.append(
        Paragraph("3. Category Sales Changes", styles["Heading2"])
    )

    category_data = [
        ["Category", "March Sales", "April Sales", "Change"]
    ]

    for category, row in changes["category"].iterrows():

        category_data.append([
            str(category),
            f"Rs. {row[3]:,.0f}",
            f"Rs. {row[4]:,.0f}",
            f"Rs. {row['Change']:,.0f}"
        ])

    category_table = Table(category_data)

    category_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    story.append(category_table)
    story.append(Spacer(1, 18))

    # PRODUCT ANALYSIS
    story.append(
        Paragraph("4. Product Performance", styles["Heading2"])
    )

    product_data = [
        ["Product", "March Sales", "April Sales", "Change"]
    ]

    for product, row in changes["product"].iterrows():

        product_data.append([
            str(product),
            f"Rs. {row[3]:,.0f}",
            f"Rs. {row[4]:,.0f}",
            f"Rs. {row['Change']:,.0f}"
        ])

    product_table = Table(
        product_data,
        repeatRows=1
    )

    product_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 5)
    ]))

    story.append(product_table)
    story.append(Spacer(1, 18))

    # WHAT-IF ANALYSIS
    story.append(
        Paragraph("5. What-If Scenario", styles["Heading2"])
    )

    scenario_data = [
        ["Metric", "Actual", "Simulated"],
        [
            "Revenue",
            f"Rs. {scenario['actual_sales']:,.0f}",
            f"Rs. {scenario['projected_sales']:,.0f}"
        ],
        [
            "Profit",
            f"Rs. {scenario['actual_profit']:,.0f}",
            f"Rs. {scenario['projected_profit']:,.0f}"
        ]
    ]

    scenario_table = Table(scenario_data)

    scenario_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(scenario_table)
    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            "Note: What-if results are illustrative scenarios based on "
            "simplified assumptions, not guaranteed forecasts.",
            styles["Normal"]
        )
    )

    document.build(story)

    output.seek(0)

    return output.getvalue()

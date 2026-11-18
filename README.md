# AI Business Analyst Assistant

An interactive business analytics application that analyzes sales data, identifies business trends, detects performance changes, and generates actionable recommendations.

## Project Overview

The AI Business Analyst Assistant helps users understand business performance through data analysis and interactive visualizations.

Users can explore sales performance, identify declining regions and products, simulate business scenarios, and export reports.

## Features

- **Interactive Dashboard:** Filter sales data by region, category, and month.
- **Business Change Detection:** Identify changes in sales across regions, categories, products, and customers.
- **Business Recommendations:** Generate recommendations based on observed sales trends.
- **What-If Simulator:** Explore how sales growth and discount changes could affect revenue and profit.
- **Business Question Analysis:** Ask predefined business questions about sales, profit, regions, and products.
- **Report Export:** Download business reports in Excel and PDF formats.

## Technologies Used

- Python
- Pandas
- MySQL
- Streamlit
- Matplotlib
- ReportLab
- OpenPyXL

## Project Structure

```text
AI-Business-Analyst/
│
├── app/
│   └── app.py
│
├── data/
│   └── sales_data.xlsx
│
├── src/
│   ├── analysis.py
│   ├── business_analysis.py
│   ├── change_detection.py
│   ├── recommendation_engine.py
│   ├── what_if_simulator.py
│   ├── report_export.py
│   ├── load_data.py
│   └── load_to_mysql.py
│
└── README.md
```

## How to Run the Project

1. Clone or download this repository.
2. Install the required Python libraries.
3. Configure your local MySQL database.
4. Configure database credentials using Streamlit secrets.
5. Run the application:

```bash
streamlit run app/app.py
```

## Database

The project uses MySQL to store and retrieve sales records.

Database name: `ai_business_analyst`

Table name: `sales`

## Business Use Case

The application compares March and April sales performance and identifies areas that require further investigation.

It can help answer questions such as:

- Why did sales decrease?
- Which region experienced the largest decline?
- Which products performed poorly?
- How could changes in sales growth and discounts affect profit?

## Future Enhancements

- Natural-language-to-SQL functionality.
- LLM-powered business insights.
- Forecasting future sales.
- More advanced customer segmentation.
- Interactive business report generation.

## Note

The current application uses programmed business rules and calculations. It does not yet use an external LLM API. What-If results are illustrative scenarios, not guaranteed forecasts.
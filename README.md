
# Olist E-commerce Analytics

## Project Overview

This project analyzes Brazilian e-commerce data from Olist to understand sales performance, product category trends, delivery performance, customer satisfaction, and payment behavior.

The project combines SQL, Python, statistical analysis, and Power BI to transform raw data into meaningful business insights.

## Business Objectives

- Analyze monthly sales trends and identify high-performing periods.
- Identify product categories generating the highest sales.
- Evaluate delivery performance and late delivery rates.
- Investigate the relationship between delivery delays and customer review scores.
- Understand customer payment method preferences.

## Tools and Technologies

- **SQL:** MySQL 8.0
- **Python:** Pandas, SQLAlchemy, SciPy
- **Data Visualization:** Power BI
- **Development Tools:** VS Code, Git, GitHub
- **Database:** MySQL

## Dataset

Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The analysis uses multiple related datasets, including orders, order items, payments, reviews, customers, sellers, products, and product category translations.

The geolocation dataset was not imported into MySQL for this analysis.

## Project Structure

```text
olist-ecommerce-analytics/
├── data/                  # Raw CSV files (not tracked by Git)
├── python/                # Python analysis and data-loading scripts
├── sql/                   # SQL queries for business analysis
├── powerbi/               # Power BI report and data exports
├── .gitignore
└── README.md
```

## Analysis Performed

### 1. Sales Performance
- Calculated total product sales, freight revenue, and order counts.
- Analyzed monthly sales trends.
- Identified the highest-performing month.

### 2. Product Category Analysis
- Ranked product categories by sales.
- Compared sales, order counts, and items sold.
- Exported category-level results for Power BI.

### 3. Delivery Performance
- Calculated average delivery duration.
- Identified late deliveries and calculated the late delivery rate.
- Compared review scores between late and on-time or early deliveries.

### 4. Statistical Analysis
- Used the Mann–Whitney U test in Python to compare customer review score distributions between late and on-time or early deliveries.
- Evaluated whether the observed difference was statistically significant.

### 5. Payment Analysis
- Compared payment methods by order count, payment value, and average payment record value.
- Examined installment patterns.

### 6. Power BI Dashboard
The report contains two pages:

- **Sales Dashboard:** Total product sales, total orders, monthly sales trend, and top 10 product categories by sales.
- **Business Insights:** Key findings from the SQL and Python analyses.

## Key Findings

- Total product sales were approximately **R$13.59 million** across orders with item records.
- The analysis included **98,666 distinct orders with item records**.
- November 2017 recorded the highest monthly product sales, at approximately **R$1.01 million**.
- Health and beauty was the highest-selling product category, generating approximately **R$1.26 million** in product sales.
- The late delivery rate was approximately **8.11%** among eligible delivered orders.
- On-time or early deliveries had an average review score of **4.29**, compared with **2.57** for late deliveries.

The review score difference indicates an association between delivery timeliness and customer satisfaction. It does not, by itself, establish causation.

## Skills Demonstrated

- SQL querying, aggregation, joins, and date-based analysis
- Data cleaning and data quality inspection
- Python data analysis and database integration
- Statistical hypothesis testing
- ETL and data export workflows
- Power BI dashboard development
- Business insight communication

## Future Improvements

- Add customer and seller geographic analysis.
- Develop more detailed customer segmentation.
- Analyze repeat purchases and customer retention.
- Improve dashboard interactivity with slicers and additional KPIs.

## Author

Jayalakshmi M

Computer Science and Engineering Graduate | Aspiring Data Analyst

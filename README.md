# Olist E-commerce Analytics

## Project Overview

This project analyzes Brazilian e-commerce data from Olist to understand sales performance, product category trends, delivery performance, customer satisfaction, payment behavior, and low-review prediction.

The project combines SQL, Python, statistical analysis, machine learning, and Power BI to transform raw data into meaningful business insights.

## Business Objectives

- Analyze monthly sales trends and identify high-performing periods.
- Identify product categories generating the highest sales.
- Evaluate delivery performance and late delivery rates.
- Investigate the relationship between delivery delays and customer review scores.
- Understand customer payment method preferences.
- Build machine learning models to classify orders associated with low customer reviews.

## Tools and Technologies

- **SQL:** MySQL 8.0
- **Python:** Pandas, SQLAlchemy, SciPy, Scikit-learn
- **Machine Learning:** Logistic Regression, Random Forest, classification metrics, feature importance
- **Data Visualization:** Power BI
- **Statistical Analysis:** Mann–Whitney U test
- **Development Tools:** VS Code, Git, GitHub
- **Database:** MySQL

## Dataset

Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The analysis uses multiple related datasets, including orders, order items, payments, reviews, customers, sellers, products, and product category translations.

The geolocation dataset was not imported into MySQL for this analysis.

## Project Structure

```text
olist-ecommerce-analytics/
├── data/                   # Raw CSV files (not tracked by Git)
├── python/                 # Python analysis and ML scripts
├── sql/                    # SQL queries for business analysis
├── powerbi/                # Power BI report and local data exports
├── .gitignore
└── README.md
```

## Analysis Performed

### 1. Sales Performance

- Calculated total product sales, freight value, and order counts.
- Analyzed monthly sales trends.
- Identified the highest-performing month.
- Exported monthly sales results for Power BI visualization.

### 2. Product Category Analysis

- Ranked product categories by sales.
- Compared sales, order counts, and items sold.
- Identified the highest-revenue product categories.
- Exported category-level results for Power BI.

### 3. Delivery Performance

- Calculated average delivery duration.
- Identified late deliveries and calculated the late delivery rate.
- Compared review scores between late and on-time or early deliveries.

### 4. Statistical Analysis

- Used the Mann–Whitney U test in Python to compare customer review score distributions between late and on-time or early deliveries.
- Evaluated whether the observed difference was statistically significant.
- Interpreted the results as an association rather than evidence of causation.

### 5. Payment Analysis

- Compared payment methods by order count and total payment value.
- Examined average payment record values and installment patterns.
- Identified credit cards as the dominant payment method by total payment value.

### 6. Predictive Analytics: Low Review Classification

Developed machine learning models to classify orders associated with low customer reviews (1–2 stars) using order and delivery characteristics.

**Dataset preparation**
- Prepared a dataset containing 95,823 orders with complete review, delivery, payment, and order-value information.
- Defined `low_review` as 1 when an order's average review score was 2 or below, and 0 otherwise.
- Identified low-review orders as 12.77% of the prepared dataset.
- Used delivery duration, delay days, total product price, freight cost, and payment type as model features.
- Split the dataset into 80% training data and 20% testing data using stratified sampling.

**Models developed**
- Logistic Regression
- Random Forest Classifier

Class weighting was used to address the imbalance between low-review and other orders.

**Model performance**

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 0.8024 | 0.8621 |
| Precision | 0.3163 | 0.4492 |
| Recall | 0.4716 | 0.3527 |
| F1-score | 0.3787 | 0.3951 |
| ROC-AUC | 0.7130 | 0.6927 |

Random Forest achieved higher accuracy, precision, and F1-score, while Logistic Regression achieved higher recall and ROC-AUC. Neither model detected every low-review order, highlighting the challenge of identifying negative customer feedback in an imbalanced dataset.

**Feature importance**

Random Forest feature importance analysis identified the following leading predictive features:

| Feature | Importance |
|---|---:|
| Delivery duration | 32.55% |
| Total freight cost | 26.85% |
| Total product price | 26.72% |
| Delay days | 12.31% |
| Payment type | 1.57% |

Delivery duration was the most influential feature in the trained Random Forest model, followed by freight cost and total product price. Feature importance indicates predictive contribution within the model and does not establish causation.

**Limitations**

- The model uses actual delivery information and is intended for post-delivery review-risk analysis, not pre-delivery prediction.
- Model performance is affected by the imbalance between low-review and other orders.
- Further validation would be necessary before real-world deployment.

### 7. Power BI Dashboard

The Power BI report contains two pages:

- **Sales Dashboard:** Total product sales, order count, monthly sales trend, and top 10 product categories by sales.
- **Business Insights:** Key findings from SQL and Python analyses, including sales performance, delivery performance, and customer review patterns.

## Key Findings

- Total product sales were approximately **R$13.59 million** across orders with item records.
- The analysis included **98,666 distinct orders with item records**.
- November 2017 recorded the highest monthly product sales, at approximately **R$1.01 million**.
- Health and beauty was the highest-selling product category, generating approximately **R$1.26 million** in product sales.
- The late delivery rate was approximately **8.11%** among eligible delivered orders.
- On-time or early deliveries had an average review score of **4.29**, compared with **2.57** for late deliveries.
- Credit cards accounted for approximately **78.3% of total payment value**.
- The low-review classification dataset contained **95,823 orders**, with **12.77%** classified as low-review orders.
- Random Forest achieved an F1-score of **0.3951** and ROC-AUC of **0.6927** for low-review classification.

The review score difference indicates an association between delivery timeliness and customer satisfaction. It does not, by itself, establish causation.

## Skills Demonstrated

- SQL querying, aggregation, joins, and date-based analysis
- Data cleaning and data quality inspection
- Python data analysis and database integration
- Statistical hypothesis testing
- Machine learning model development and evaluation
- Classification metrics and feature importance analysis
- ETL and data export workflows
- Power BI dashboard development
- Business insight communication
- Git and GitHub version control

## Future Improvements

- Add customer and seller geographic analysis.
- Develop more detailed customer segmentation.
- Analyze repeat purchases and customer retention.
- Improve dashboard interactivity with slicers and additional KPIs.
- Experiment with feature engineering and classification thresholds to improve low-review detection.
- Validate model performance on additional data before considering real-world use.

## Author

**Jayalakshmi M**

Computer Science and Engineering Graduate | Aspiring Data Analyst
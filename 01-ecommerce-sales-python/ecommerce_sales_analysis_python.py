# -*- coding: utf-8 -*-
"""ecommerce_sales_analysis

# E-Commerce Sales & Customer Experience Analysis

## Project Overview

This project analyzes 5,000 synthetic e-commerce transactions using Python
to identify business insights related to sales performance, delivery
performance, customer satisfaction, discount effectiveness, and seasonality.

## Business Problems

1. Which product categories and regions are driving revenue?
2. Does delivery performance affect customer satisfaction?
3. Are discounts being used effectively?

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Google Colab

## Key Analysis

### Sales Performance
Analyzed revenue by product category, region, and category-region combinations.

### Delivery & Customer Satisfaction
Analyzed delivery duration, regional delivery performance, and the
relationship between delivery time and customer ratings.

### Discount Effectiveness
Analyzed discount levels and their relationship with average revenue per order.

### Seasonality
Compared quarterly revenue and discount behavior.

## Key Findings

- Electronics generated the highest revenue.
- West was the highest-revenue region.
- Delivery time showed only a weak relationship with customer ratings.
- Higher discount levels were associated with lower average revenue per order.
- Q2 generated the highest quarterly revenue.

## Business Recommendations

- Prioritize high-performing product categories.
- Investigate lower-performing categories.
- Monitor unusually long delivery times.
- Use targeted discount strategies.
- Validate business assumptions using actual data.

## Dataset

The dataset is synthetic and was created for analytical practice and portfolio
purposes.

# E-Commerce Sales & Customer Experience Analysis


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("ecommerce_sales_analysis.csv")

df.head()

"""# 1. Data Understanding

Before performing business analysis, we first understand the structure,
size, data types, and quality of the dataset.
"""

df.shape

df.info()

df.describe()

"""# 2. Data Quality Check

We will check for missing values and duplicate records before performing
the business analysis.
"""

print("Missing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("Duplicate order IDs:", df['order_id'].duplicated().sum())

df['order_date'] = pd.to_datetime(df['order_date'])

print(df['order_date'].dtype)

print("First order date:", df['order_date'].min())
print("Last order date:", df['order_date'].max())
#Because this is synthetic data, we shouldn't treat that period as a literal real-world company history.

df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['quarter'] = df['order_date'].dt.quarter

df.head()

"""# 3. Key Business KPIs

Before investigating individual business problems, we establish a baseline
using key sales, operational, and customer-experience KPIs.
"""

total_revenue = df['revenue'].sum()
total_orders = df['order_id'].nunique()
average_order_value = df['revenue'].mean()
average_delivery_days = df['delivery_days'].mean()
average_rating = df['customer_rating'].mean()

print("Total Revenue:", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Average Order Value:", round(average_order_value, 2))
print("Average Delivery Days:", round(average_delivery_days, 2))
print("Average Customer Rating:", round(average_rating, 2))

"""# 4. Business Problem 1 – Sales & Revenue Performance

## Business Question

Which product categories and regions are driving revenue?

## Objective

Identify high-performing product categories and regions to help the business
prioritize inventory, marketing, and sales efforts.
"""

category_revenue = (
    df.groupby('product_category')['revenue']
    .sum()
    .sort_values(ascending=False)
)

category_revenue

plt.figure(figsize=(8,5))

category_revenue.plot(kind='bar')

plt.title('Revenue by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Revenue')
plt.xticks(rotation=0)

plt.show()

region_revenue = (
    df.groupby('region')['revenue']
    .sum()
    .sort_values(ascending=False)
)

region_revenue

plt.figure(figsize=(8,5))

region_revenue.plot(kind='bar')

plt.title('Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Total Revenue')
plt.xticks(rotation=0)

plt.show()

category_region = pd.pivot_table(
    df,
    values='revenue',
    index='product_category',
    columns='region',
    aggfunc='sum'
)

category_region

category_region.plot(
    kind='bar',
    figsize=(10,6)
)

plt.title('Revenue by Product Category and Region')
plt.xlabel('Product Category')
plt.ylabel('Revenue')
plt.xticks(rotation=0)
plt.legend(title='Region')

plt.show()

category_region_rank = (
    df.groupby(['product_category', 'region'])['revenue']
    .sum()
    .sort_values(ascending=False)
)

category_region_rank.head(10)

"""## Business Findings – Problem 1

- Electronics is the highest-revenue product category.
- Beauty generates the lowest total revenue.
- West is the highest-revenue region.
- Electronics in the South region is the strongest category-region combination.

## Business Recommendation

The company should maintain strong inventory availability for Electronics
and continue supporting high-performing regions.

Lower-performing categories such as Beauty should be investigated further
to determine whether product demand, pricing, or promotional strategies
can be improved.

# 5. Business Problem 2 – Delivery Performance & Customer Satisfaction

## Business Question

Does delivery performance affect customer satisfaction?

## Objective

Determine whether longer delivery times are associated with lower customer
ratings and identify potential areas for operational improvement.
"""

delivery_region = (
    df.groupby('region')
    .agg(
        average_delivery_days=('delivery_days', 'mean'),
        average_rating=('customer_rating', 'mean')
    )
    .sort_values('average_delivery_days', ascending=False)
)

delivery_region

delivery_rating_corr = df['delivery_days'].corr(df['customer_rating'])

print("Correlation between delivery days and customer rating:",
      round(delivery_rating_corr, 3))

delivery_analysis = (
    df.groupby(
        pd.cut(
            df['delivery_days'],
            bins=[0, 3, 5, 7, 9, 12]
        ),
        observed=True
    )
    .agg(
        orders=('order_id', 'count'),
        average_rating=('customer_rating', 'mean'),
        total_revenue=('revenue', 'sum')
    )
)

delivery_analysis

plt.figure(figsize=(9,5))

delivery_analysis['average_rating'].plot(kind='bar')

plt.title('Average Customer Rating by Delivery Duration')
plt.xlabel('Delivery Days')
plt.ylabel('Average Customer Rating')
plt.xticks(rotation=0)

plt.show()

"""## Business Findings – Problem 2

- Average delivery time is approximately 6.1 days.
- Regional differences in delivery time are relatively small.
- The correlation between delivery time and customer rating is very weak.
- Orders taking 10–12 days have somewhat lower average ratings than orders
  delivered within 4–5 days.

## Business Recommendation

Delivery time should still be monitored, particularly for unusually long
delivery durations. However, the analysis suggests that delivery time alone
is unlikely to explain customer satisfaction.

The business should investigate other factors such as product experience,
pricing, product quality, or customer service if improving ratings is a priority.

# 6. Business Problem 3 – Discount Effectiveness

## Business Question

Are higher discounts associated with stronger revenue performance?

## Objective

Understand how order-level discounts relate to revenue and determine whether
the business should use broad or targeted discount strategies.
"""

print("Average discount:",
      round(df['discount'].mean() * 100, 2), "%")

print("Minimum discount:",
      round(df['discount'].min() * 100, 2), "%")

print("Maximum discount:",
      round(df['discount'].max() * 100, 2), "%")

discount_analysis = (
    df.groupby(
        pd.cut(
            df['discount'],
            bins=[-0.001, 0.10, 0.20, 0.30, 0.40]
        ),
        observed=True
    )
    .agg(
        orders=('order_id', 'count'),
        average_revenue=('revenue', 'mean'),
        total_revenue=('revenue', 'sum'),
        average_rating=('customer_rating', 'mean')
    )
)

discount_analysis

plt.figure(figsize=(9,5))

discount_analysis['average_revenue'].plot(kind='bar')

plt.title('Average Revenue by Discount Level')
plt.xlabel('Discount Level')
plt.ylabel('Average Revenue per Order')
plt.xticks(rotation=0)

plt.show()

discount_rating_corr = df['discount'].corr(df['customer_rating'])

print(
    "Correlation between discount and customer rating:",
    round(discount_rating_corr, 3)
)

"""## Business Findings – Problem 3

- The average order discount is approximately 18%.
- Orders with lower discounts have higher average revenue.
- Orders with discounts above 30% have the lowest average revenue per order.
- Discount level does not show a meaningful relationship with customer rating.

## Business Recommendation

The company should avoid applying high discounts broadly across all orders.

Instead, discounts should be targeted toward selected products, customer
segments, or campaigns where additional demand is needed.

The business should also monitor revenue performance at different discount
levels before increasing promotional discounts.

> Note: The dataset does not contain cost or profit information. Therefore,
> discount effectiveness is evaluated using revenue performance rather than
> profitability.

# 7. Seasonality Analysis

The dataset description suggests increased transaction activity and discounting
during Q4. We will verify the pattern using the available data.
"""

quarter_analysis = (
    df.groupby('quarter')
    .agg(
        orders=('order_id', 'count'),
        total_revenue=('revenue', 'sum'),
        average_discount=('discount', 'mean'),
        average_rating=('customer_rating', 'mean')
    )
)

quarter_analysis

plt.figure(figsize=(8,5))

quarter_analysis['total_revenue'].plot(kind='bar')

plt.title('Revenue by Quarter')
plt.xlabel('Quarter')
plt.ylabel('Total Revenue')
plt.xticks(rotation=0)

plt.show()

"""# 8. Overall Key Findings

### Sales Performance

- Electronics is the highest-revenue product category.
- Beauty generates the lowest total revenue.
- West is the highest-revenue region.
- Electronics in the South region is the strongest category-region combination.

### Delivery & Customer Satisfaction

- Average delivery time is approximately 6.1 days.
- The relationship between delivery time and customer rating is very weak.
- Very long delivery durations show somewhat lower average ratings.
- Delivery time alone does not appear to explain customer satisfaction.

### Discount Effectiveness

- Average discount is approximately 18%.
- Higher discount levels are associated with lower average revenue per order.
- High discounts should therefore be used selectively.
- Profitability cannot be evaluated because cost/profit data is unavailable.

### Seasonality

- Q2 has the highest quarterly revenue in this dataset.
- Q4 does not show the highest revenue despite the dataset's stated seasonal assumption.

# 9. Business Recommendations

### 1. Prioritize High-Performing Categories

Electronics generates the highest revenue and should receive strong attention
from inventory and marketing teams.

### 2. Investigate Low-Performing Categories

Beauty generates the lowest revenue. The business should investigate whether
pricing, product demand, product assortment, or promotions can improve its
performance.

### 3. Monitor Long Delivery Times

Although delivery time has only a weak relationship with ratings, unusually
long deliveries are associated with somewhat lower satisfaction. Orders with
long delivery durations should therefore be monitored.

### 4. Use Targeted Discounts

Higher discounts are associated with lower average revenue per order.
Instead of applying large discounts broadly, the company should use targeted
promotions where additional demand is required.

### 5. Validate Business Assumptions Using Data

The dataset description suggests Q4 seasonality, but the analysis shows that
Q2 generated the highest quarterly revenue. Business assumptions should
therefore be validated with actual performance data.

# 10. Conclusion

This analysis examined 5,000 e-commerce orders to understand sales performance,
regional performance, delivery operations, customer satisfaction, discount
behavior, and quarterly trends.

The analysis found that Electronics is the strongest revenue-generating
category, while West is the strongest region by total revenue.

Delivery time showed only a very weak relationship with customer ratings,
suggesting that customer satisfaction is likely influenced by factors beyond
delivery duration alone.

Higher discount levels were associated with lower average revenue per order,
indicating that broad high-discount strategies should be used carefully.

Overall, the analysis demonstrates how Python can be used to transform raw
transaction data into business insights and actionable recommendations.
"""

summary = pd.DataFrame({
    'KPI': [
        'Total Revenue',
        'Total Orders',
        'Average Order Value',
        'Average Delivery Days',
        'Average Customer Rating'
    ],
    'Value': [
        round(df['revenue'].sum(), 2),
        df['order_id'].nunique(),
        round(df['revenue'].mean(), 2),
        round(df['delivery_days'].mean(), 2),
        round(df['customer_rating'].mean(), 2)
    ]
})

summary
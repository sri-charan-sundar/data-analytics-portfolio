
--Is the business growing profitably?

-- Check the overall sales, profit, orders, and average order value
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(net_sales), 2) AS average_order_value
FROM ecommerce_sales
WHERE order_status = 'Completed';

-- Compare revenue, profit, and orders across each year
SELECT
    strftime('%Y', order_date) AS year,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM ecommerce_sales
WHERE order_status = 'Completed'
GROUP BY year
ORDER BY year;

-- Check whether the company's profit margin is improving or declining
SELECT
    strftime('%Y', order_date) AS year,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) * 100.0 / SUM(net_sales), 2) AS profit_margin
FROM ecommerce_sales
WHERE order_status = 'Completed'
GROUP BY year
ORDER BY year;

-- Check monthly revenue and profit to identify sales trends
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM ecommerce_sales
WHERE order_status = 'Completed'
GROUP BY month
ORDER BY month;

--Which products are driving revenue and profit?

-- Compare sales, units sold, and profit across product categories
SELECT
    p.product_category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.net_sales), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit
FROM order_items oi
JOIN product p
    ON oi.product_id = p.product_id
GROUP BY p.product_category
ORDER BY total_revenue DESC;

-- Find the top 10 products generating the highest revenue
SELECT
    p.product_name,
    p.product_category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.net_sales), 2) AS total_revenue
FROM order_items oi
JOIN product p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_name,
    p.product_category
ORDER BY total_revenue DESC
LIMIT 10;

-- Find the top 10 products generating the highest profit
SELECT
    p.product_name,
    p.product_category,
    ROUND(SUM(oi.net_sales), 2) AS total_revenue,
    ROUND(SUM(oi.profit), 2) AS total_profit
FROM order_items oi
JOIN product p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_name,
    p.product_category
ORDER BY total_profit DESC
LIMIT 10;

--Are delivery issues affecting customer satisfaction?

-- Compare the number of orders by delivery status
SELECT
    delivery_status,
    COUNT(*) AS total_orders
FROM ecommerce_sales
GROUP BY delivery_status
ORDER BY total_orders DESC;

-- Compare average customer ratings for different delivery statuses
SELECT
    delivery_status,
    COUNT(*) AS total_orders,
    ROUND(AVG(customer_rating), 2) AS average_rating
FROM ecommerce_sales
WHERE customer_rating IS NOT NULL
GROUP BY delivery_status
ORDER BY average_rating DESC;

-- Compare actual delivery days with expected delivery days
SELECT
    delivery_status,
    ROUND(AVG(delivery_days), 2) AS average_delivery_days,
    ROUND(AVG(estimated_delivery_days), 2) AS average_expected_days,
    COUNT(*) AS total_orders
FROM ecommerce_sales
WHERE delivery_days IS NOT NULL
  AND estimated_delivery_days IS NOT NULL
GROUP BY delivery_status
ORDER BY average_delivery_days;

-- Compare customer review sentiment across delivery statuses
SELECT
    delivery_status,
    review_sentiment,
    COUNT(*) AS total_reviews
FROM ecommerce_sales
WHERE review_sentiment IS NOT NULL
GROUP BY
    delivery_status,
    review_sentiment
ORDER BY
    delivery_status,
    total_reviews DESC;
# Write your MySQL query statement below
SELECT
    ROUND(
        AVG(order_date = customer_pref_delivery_date) * 100,
        2
    ) AS immediate_percentage
FROM (
    SELECT
        customer_id,
        order_date,
        customer_pref_delivery_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS order_rank
    FROM Delivery
) ranked_orders
WHERE order_rank = 1;
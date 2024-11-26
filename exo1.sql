SELECT
    c.id,
    c.name,
    SUM(oi.quantity * oi.price) AS total_amount
FROM
    customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY
    c.id,
    c.name
ORDER BY
    total_amount DESC;


---
SELECT
    c.id,
    c.name
FROM
    customers c
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            orders o
        WHERE
            o.customer_id = c.id
    );

---
SELECT
    p.id,
    p.name,
    SUM(oi.quantity) AS total_quantity_sold
FROM
    products p
    JOIN order_items oi ON p.id = oi.product_id
GROUP BY
    p.id, p.name
ORDER BY
    total_quantity_sold DESC
LIMIT 5;
---
WITH customer_orders AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date
    FROM
        orders
)
SELECT
    customer_id,
    AVG(EXTRACT(EPOCH FROM (order_date - previous_order_date))/86400) AS avg_days_between_orders
FROM
    customer_orders
WHERE
    previous_order_date IS NOT NULL
GROUP BY
    customer_id;
---
WITH total_per_customer AS (
    SELECT
        customer_id,
        SUM(total_amount) AS total_spent
    FROM
        orders
    GROUP BY
        customer_id
),
average_spent AS (
    SELECT
        AVG(total_spent) AS avg_spent
    FROM
        total_per_customer
)
SELECT
    c.id,
    c.name,
    t.total_spent
FROM
    customers c
    JOIN total_per_customer t ON c.id = t.customer_id,
    average_spent a
WHERE
    t.total_spent > a.avg_spent;

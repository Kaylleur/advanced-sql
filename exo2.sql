SELECT
    p.id,
    p.name,
    p.category_id,
    p.stock_quantity,
    RANK() OVER (PARTITION BY p.category_id ORDER BY p.stock_quantity DESC) AS stock_rank
FROM
    products p
ORDER BY
    p.category_id,
    stock_rank;

---
SELECT
    p.id,
    p.name,
    p.stock_quantity
FROM
    products p
WHERE
    p.stock_quantity < (
        SELECT
            AVG(stock_quantity)
        FROM
            products
    );
---
SELECT
    p.id,
    p.name,
    MAX(o.order_date) AS last_order_date
FROM
    products p
    JOIN order_items oi ON p.id = oi.product_id
    JOIN orders o ON oi.order_id = o.id
GROUP BY
    p.id, p.name;
---

---Optimisation :

-- Index sur products(category_id) : Optimise la partition pour le classement par stock.
-- Index sur order_items(product_id) et orders(order_date) : Améliore les jointures et les agrégations pour les dates de commande.
-- Index sur products(stock_quantity) : Accélère la recherche de produits sous le stock moyen.

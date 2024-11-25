insert into customers (id, name, email, created_at)
values (1001, 'Foo Bar', 'foo.bar@gmail.com', DEFAULT);

select * from customers c
left join orders o on c.id = o.customer_id
where o.id is null;

select * from orders o
right join customers c on c.id = o.customer_id
where o.id is null;

select count(*) as nb_orders, c.id from customers c
left join orders o on c.id = o.customer_id
group by c.id
having count(*) > 10
order by count(*) desc;

alter table customers add column phone varchar(20);

create table toto (id serial primary key, name varchar(50));
drop table toto;

SELECT
  (select max(id) from customers) as maxIdCustomers,
  (select max(id) from orders) as maxIdOrders;


WITH avg_order_amount AS (
    SELECT AVG(total_amount) AS avg_amount FROM orders
)
SELECT id, total_amount
FROM orders
WHERE total_amount > (SELECT avg_amount FROM avg_order_amount);

-- exo 1
WITH product_order_count AS (
    SELECT
        p.id,
        p.name,
        p.category,
        COUNT(oi.id) AS order_count
    FROM
        products p
    JOIN
        order_items oi ON p.id = oi.product_id
    GROUP BY
        p.id, p.name, p.category
),
max_order_count AS (
    SELECT
        category,
        MAX(order_count) AS max_count
    FROM
        product_order_count
    GROUP BY
        category
)
SELECT
    poc.category,
    poc.name,
    poc.order_count
FROM
    product_order_count poc
JOIN
    max_order_count moc ON poc.category = moc.category AND poc.order_count = moc.max_count;

-- exo 2
SELECT
    c.name,
    o.id AS order_id,
    o.total_amount,
    customer_totals.total_spent
FROM
    customers c
JOIN
    orders o ON c.id = o.customer_id
JOIN
    (
        SELECT
            customer_id,
            SUM(total_amount) AS total_spent
        FROM
            orders
        GROUP BY
            customer_id
    ) AS customer_totals ON c.id = customer_totals.customer_id
WHERE
    o.total_amount >= 0.5 * customer_totals.total_spent;


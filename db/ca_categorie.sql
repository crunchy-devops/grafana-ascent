SELECT
    p.category,
    SUM(p.price * oi.quantity) as value
FROM order_items oi
         JOIN products p ON oi.product_id = p.id
         JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
GROUP BY p.category;

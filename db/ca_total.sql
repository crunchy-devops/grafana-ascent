SELECT
    SUM(p.price * oi.quantity) as total_ca
FROM order_items oi
         JOIN products p ON oi.product_id = p.id
         JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'; -- On ne compte que les ventes réussies
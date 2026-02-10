SELECT
    SUM(p.price * oi.quantity) as total_ca
FROM order_items oi
         JOIN products p ON oi.product_id = p.id
         JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'; -- On ne compte que les ventes réussies


--
SELECT
    $__timeGroupAlias(o.order_date, '15m') ,
    SUM(p.price * oi.quantity) as total_ca
FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
  AND $__timeFilter(o.order_date) -- On ne compte que les ventes réussies
GROUP BY 1
ORDER BY 1;


--
SELECT
    $__timeGroupAlias(o.order_date, $__interval) ,
    SUM(p.price * oi.quantity) as total_ca
FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
  AND $__timeFilter(o.order_date) -- On ne compte que les ventes réussies
GROUP BY 1
ORDER BY 1;
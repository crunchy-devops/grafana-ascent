SELECT
    p.category,
    SUM(p.price * oi.quantity) as value
FROM order_items oi
         JOIN products p ON oi.product_id = p.id
         JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
GROUP BY p.category;


-- # pour le dashboard
SELECT
    $__timeGroupAlias(o.order_date, $__interval) ,
    p.category AS "metric", -- Alias interne a Grafana
    SUM(p.price * oi.quantity) as partiel_ca
FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
  AND $__timeFilter(o.order_date) -- On ne compte que les ventes réussies
  AND (p.category IN ($category) OR 'all' IN ($category))
GROUP BY 1,2
ORDER BY 1;

-- dans display name,  mettre ${__field.labels.category}

-- Add Nombre de Commandes
SELECT
    $__timeGroupAlias(o.order_date, $__interval) ,
     p.category AS "metric",
    SUM(p.price * oi.quantity) as total_ca,
    COUNT(DISTINCT o.id) as "Nombre de Commandes"
FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
  AND $__timeFilter(o.order_date)
  AND (p.category IN ($category) OR 'all' IN ($category))
GROUP BY 1,2
ORDER BY 1;

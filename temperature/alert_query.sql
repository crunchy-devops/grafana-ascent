SELECT
    time,
    value
FROM temperatures
WHERE $__timeFilter(time)
ORDER BY time DESC
LIMIT 1

SELECT
    CASE
        -- Check if all values in the last 4 minutes are < 0
        WHEN (
            SELECT count(*)
            FROM temperatures
            WHERE time >= NOW() - INTERVAL '4 minutes' AND value >= 0
        ) = 0 AND (
            SELECT count(*)
            FROM temperatures
            WHERE time >= NOW() - INTERVAL '4 minutes'
        ) > 0 THEN 2
        -- Check if all values in the last 2 minutes are < 0
        WHEN (
            SELECT count(*)
            FROM temperatures
            WHERE time >= NOW() - INTERVAL '2 minutes' AND value >= 0
        ) = 0 AND (
            SELECT count(*)
            FROM temperatures
            WHERE time >= NOW() - INTERVAL '2 minutes'
        ) > 0 THEN 1
        ELSE 0
    END AS alert_level

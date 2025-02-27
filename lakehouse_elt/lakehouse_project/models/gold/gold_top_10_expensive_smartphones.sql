--  Mostar os 10 smartphones mais caros

WITH expensive_smartphones AS (
    SELECT
        brand,
        model,
        price,
        ram_capacity,
        rom_capacity,
        rating_value
    FROM {{ ref('silver_smartphone') }}
    ORDER BY price DESC
    LIMIT 10
)

SELECT *
FROM expensive_smartphones
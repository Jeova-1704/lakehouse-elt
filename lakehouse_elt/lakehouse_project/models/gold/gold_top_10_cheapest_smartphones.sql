-- seleciona os 10 smartphones mais baratos 

WITH expensive_smartphones AS (
    SELECT
        brand,
        model,
        price,
        ram_capacity,
        rom_capacity,
        rating_value
    FROM {{ ref('silver_smartphone') }}
    ORDER BY price ASC
    LIMIT 10
)

SELECT *
FROM expensive_smartphones
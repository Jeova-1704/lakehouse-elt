--  Comparar preços e avaliações entre as marcas.



WITH brand_comparison AS (
    SELECT 
        brand,
        ROUND(AVG(price), 2) AS avg_price,
        ROUND(AVG(rating_value), 2) AS avg_rating,
        COUNT(*) AS total_products
    FROM {{ ref('silver_smartphone') }}
    GROUP BY brand
    ORDER BY avg_price DESC
)

SELECT * FROM brand_comparison
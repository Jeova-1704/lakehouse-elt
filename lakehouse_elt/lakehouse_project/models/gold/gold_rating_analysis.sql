-- Descobrir quais marcas e modelos possuem as melhores e piores avaliações.


WITH rating_analysis AS (
    SELECT 
        brand,
        model,
        ROUND(AVG(rating_value), 2) AS avg_rating,
        COUNT(*) AS total_products
    FROM {{ ref('silver_smartphone') }}
    GROUP BY brand, model
    ORDER BY avg_rating DESC
)

SELECT * FROM rating_analysis

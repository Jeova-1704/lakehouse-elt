-- identificar estatisticas de preço por marca e modelo, incluindo média, mínimo e máximo.


WITH price_analysis AS (
    SELECT 
        brand,
        model,
        COUNT(*) AS total_products,
        ROUND(AVG(price), 2) AS avg_price,
        MIN(price) AS min_price,
        MAX(price) AS max_price
    FROM {{ ref('silver_smartphone') }}
    GROUP BY brand, model
)

SELECT * FROM price_analysis

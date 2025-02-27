--  Analisar como os preços mudam ao longo do tempo.


WITH price_trend AS (
    SELECT 
        brand,
        model,
        extracted_date,
        ROUND(AVG(price), 2) AS avg_price
    FROM {{ ref('silver_smartphone') }}
    GROUP BY brand, model, extracted_date
    ORDER BY extracted_date DESC
)

SELECT * FROM price_trend
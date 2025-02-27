--  Criar segmentos de mercado para identificar categorias de preço.


WITH price_segments AS (
    SELECT 
        brand,
        model,
        price,
        CASE 
            WHEN price < 1000 THEN 'Econômico'
            WHEN price BETWEEN 1000 AND 3000 THEN 'Intermediário'
            ELSE 'Premium'
        END AS price_segment
    FROM {{ ref('silver_smartphone') }}
)

SELECT * FROM price_segments
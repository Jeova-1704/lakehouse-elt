{{ config(
    materialized='incremental',
    unique_key='id'
) }}

WITH bronze AS (
    SELECT * FROM public.bronze_amazon_products
),

transformed AS (
    SELECT 
        id,

        CASE 
            WHEN product_name ILIKE '%iphone%' THEN 'Apple'
            WHEN product_name ILIKE '%samsung%' THEN 'Samsung'
            WHEN product_name ILIKE '%motorola%' OR product_name ILIKE '%moto%' THEN 'Motorola'
            WHEN product_name ILIKE '%xiaomi%' OR product_name ILIKE '%redmi%' OR product_name ILIKE '%poco%' THEN 'Xiaomi'
            WHEN product_name ILIKE '%realme%' THEN 'Realme'
            WHEN product_name ILIKE '%infinix%' THEN 'Infinix'
            ELSE 'Outros'
        END AS brand,

        -- Extraindo apenas o modelo do celular
        REGEXP_SUBSTR(
            REGEXP_REPLACE(
                product_name, 
                '.*?(iphone|samsung|motorola|moto|xiaomi|redmi|poco|realme|infinix)\s+', 
                '', 
                'i'
            ), 
            '([a-zA-Z]*\s?[0-9]+[a-zA-Z]*)'
        ) AS model,

        -- Extraindo apenas o número da RAM antes de "GB RAM" e convertendo para inteiro
        ABS(CAST(REGEXP_SUBSTR(product_name, '([0-9]+)(?=GB RAM)') AS INTEGER)) AS ram_capacity,

        -- Extraindo apenas o número da ROM antes de "GB" e convertendo para inteiro
        ABS(CAST(REGEXP_SUBSTR(product_name, '(^|[^0-9])(32|64|128|256|512)(?=GB)') AS INTEGER)) AS rom_capacity,

        -- Convertendo preço para NUMERIC
        CAST(
            NULLIF(
                REPLACE(
                    REPLACE(
                        REPLACE(TRIM(price_whole), 'R$', ''), 
                        '.', ''
                    ), 
                    ',', '.' 
                ), 
                ''
            ) AS NUMERIC
        ) AS price,

        -- Convertendo rating_value para NUMERIC
        CAST(
            NULLIF(
                REPLACE(
                    SPLIT_PART(rating_value, ' ', 1), 
                    ',', '.'
                ), 
                ''
            ) AS NUMERIC
        ) AS rating_value,

        extracted_at::TIMESTAMP AS extracted_date

    FROM bronze
)

SELECT *
FROM transformed
WHERE 
    brand IS NOT NULL 
    AND model IS NOT NULL 
    AND ram_capacity IS NOT NULL 
    AND rom_capacity IS NOT NULL 
    AND price IS NOT NULL 
    AND rating_value IS NOT NULL 
    AND extracted_date IS NOT NULL

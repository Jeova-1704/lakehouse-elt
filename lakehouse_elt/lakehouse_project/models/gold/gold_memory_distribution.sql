-- Analisar quais configurações de RAM e ROM são mais comuns no mercado.


WITH memory_distribution AS (
    SELECT 
        brand,
        ram_capacity,
        rom_capacity,
        COUNT(*) AS total_products,
        ROUND(AVG(price), 2) AS avg_price
    FROM {{ ref('silver_smartphone') }}
    GROUP BY brand, ram_capacity, rom_capacity
    ORDER BY total_products DESC
)

SELECT * FROM memory_distribution
import scrapy


class AmazonProductItem(scrapy.Item):
    """Define os campos que serão extraídos pela spider"""

    product_name = scrapy.Field()  # Nome do produto
    price_whole = scrapy.Field()  # Preço formatado
    rating_value = scrapy.Field()  # Avaliação do produto
    extracted_at = scrapy.Field()  # Data e hora da extração


#

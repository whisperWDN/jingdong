# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    collection = 'products'
    name = scrapy.Field()
    price = scrapy.Field()
    shop = scrapy.Field()
    link = scrapy.Field()
    pass

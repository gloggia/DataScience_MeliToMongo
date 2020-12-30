# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MelispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    descripcion = scrapy.Field()
    titulo = scrapy.Field()
    precio = scrapy.Field()
    rooms = scrapy.Field()
    baths = scrapy.Field()

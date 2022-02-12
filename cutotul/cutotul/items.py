# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from price_parser import Price


def get_price(price_raw):
    price_object = Price.fromstring(price_raw)
    return price_object.amount_float


def get_currency(price_raw):
    price_object = Price.fromstring(price_raw)
    return price_object.currency


class CutotulItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field(output_processor=TakeFirst())
    product_price = scrapy.Field(output_processor=TakeFirst())
    product_model = scrapy.Field(output_processor=TakeFirst())
    product_price_list = scrapy.Field(output_processor=TakeFirst())
    product_condition = scrapy.Field(output_processor=TakeFirst())

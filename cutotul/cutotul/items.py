# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class CutotulItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field(output_processor=TakeFirst())
    product_price = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    product_model = scrapy.Field(output_processor=TakeFirst())

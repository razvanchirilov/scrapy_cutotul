import os
import scrapy
from scrapy.loader import ItemLoader
from ..items import CutotulItem


class CutotulSpiderLoader(scrapy.Spider):
    name = 'cutotul_spider_loader'
    start_urls = ['https://cutotul.ro/39-karcher-aspiratoare-profesionale']

    def __init__(self):
        self.model = ""

    def start_requests(self):
        yield scrapy.Request('https://cutotul.ro/39-karcher-aspiratoare-profesionale', callback=self.parse)

    def parse(self, response):
        products = response.css("div.columns-container")
        for product in products:
            # get details link
            details_link = product.xpath("//a[@class='lnk_view btn btn-default']/@href").get()

            # get details
            yield response.follow(url=details_link, callback=self.parse_details)
            product_name_xpath = "//span[@class='grid-name']/text()"
            product_price_xpath = "//span[@class='price product-price']/text()"
            product_model_xpath = "".join(self.model)

            # loader
            loader = ItemLoader(item=CutotulItem(), selector=product, response=response)
            loader.add_xpath("product_name", product_name_xpath)
            loader.add_xpath("product_price", product_price_xpath)
            loader.add_value("product_model", product_model_xpath)
            yield loader.load_item()

        # nav to next page
        # Get the next response for x items from the next page - persist until no more #

        next_page = response.xpath("//li[@class='pagination_next']//@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_details(self, response):
        # set variable to response for model
        self.model = response.css("span.editable::text").get()




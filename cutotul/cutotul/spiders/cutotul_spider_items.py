import scrapy
from scrapy.loader import ItemLoader
from ..items import CutotulItem


class CutotulSpider(scrapy.Spider):
    name = 'cutotul_spider_items'
    start_urls = ['https://cutotul.ro/39-karcher-aspiratoare-profesionale?id_category=39&n=370']

    def parse(self, response):
        products = response.xpath("//ul[@class='product_list grid row']/li")
        for product in products:

            product_name_xpath = ".//span[@class='grid-name']/text()"
            product_price_xpath = ".//span[@class='price product-price']/text()"
            product_model_xpath = ".//span[@class='list-desc']/text()"

            product_price = []
            for data in product.xpath(product_price_xpath).getall():
                product_price.append(data.strip())

            product_model = []
            snip = slice(-12, -1)
            for data in product.xpath(product_model_xpath).getall():
                product_model.append(data[snip])

            item = CutotulItem()
            item['product_name'] = product.xpath(product_name_xpath).get()
            item['product_price'] = "".join(product_price)
            item['product_model'] = "".join(product_model)

            yield item




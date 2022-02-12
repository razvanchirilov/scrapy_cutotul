import os
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from ..items import CutotulItem, get_price


class CutotulSpiderLoader(scrapy.Spider):
    name = 'cutotul_spider_loader'
    start_urls = ['https://cutotul.ro/39-karcher-aspiratoare-profesionale']
    custom_settings = {"FEEDS": {"rezultate_12.02.csv": {"format": "csv"}}, 'CONCURRENT_REQUESTS': 5}

    def __init__(self):
        self.model = ""
        self.condition = ""

    def start_requests(self):
        yield scrapy.Request('https://cutotul.ro/39-karcher-aspiratoare-profesionale', callback=self.parse)

    async def parse(self, response):
        # products = response.css("div.columns-container")
        products = response.css('div.product-container')
        for product in products:
            # get details link
            details_link = product.xpath(".//a[@class='lnk_view btn btn-default']/@href").get()

            # get details
            req = response.follow(url=details_link)
            resp = await self.crawler.engine.download(req, self)
            if not None:
                self.model = resp.css("span[itemprop='sku']").css("::text").get()

            if not None:
                self.condition = resp.xpath(".//span[text()='Nou' or text()='Resigilat']/text()").get()

            product_name_xpath = ".//span[@class='grid-name']/text()"
            product_price_xpath = ".//span[@class='price product-price']/text()"
            price_raw = product.xpath(product_price_xpath).get()
            price = get_price(price_raw)
            currency = product.xpath(product_price_xpath).get()
            product_model_xpath = "".join(self.model)
            product_condition = "".join(self.condition)

            product_list_price_xpath = resp.xpath("/html/body/script/text()").re(r'getKarcherPriceNou.*;')

            product_price_list = []
            for string in product_list_price_xpath:
                search_string = string
                regex = "\\d{1,}"
                result_search = re.findall(regex, search_string)
                product_price_list.append(result_search[0])

            # loader
            loader = ItemLoader(item=CutotulItem(), selector=product, response=response)
            loader.add_xpath("product_name", product_name_xpath)
            loader.add_value("product_price", price)
            loader.add_value("product_model", product_model_xpath)
            loader.add_value("product_price_list", product_price_list)
            loader.add_value("product_condition", product_condition)
            yield loader.load_item()

        # nav to next page
        # Get the next response for x items from the next page - persist until no more #

        next_page = response.xpath("//li[@class='pagination_next']//@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)


# main driver #
if __name__ == "__main__":
    # Create Instance called 'ct' as in "c"u "t"otul
    ct = CrawlerProcess()
    ct.crawl(CutotulSpiderLoader)
    ct.start()

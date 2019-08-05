# from scrapy.spider import BaseSpider
# from scrapy.selector import HtmlXPathSelector
# from scrapy.item import Item
import scrapy
from quotesbot.items import Product

class Bikeoutlet(scrapy.Spider):
    name = "bikeoutlet"
    allowed_domains = ["bikeoutlet.cz"]
    start_urls = ["https://www.bikeoutlet.cz/bikeoutlet.php?disp=akce"]

    def parse(self, response):
            hxs = HtmlXPathSelector(response)
            listitem = hxs.select('//div[@id="item_list.item_list_akce"]')
            products = []
            for item in listitem:
                    prod = Product()
                    prod['id'] = item.select('//div[@id="ceny"]/text()').extract()
                    products.append(prod)
            return products
	
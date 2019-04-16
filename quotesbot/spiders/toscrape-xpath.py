# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="item_list"]'):
            yield {
                'code': quote.xpath('./div[@class="ceny"]/text()').extract_first(),
                'desc': quote.xpath('./div[@class="item_list_desc1"]/text()').extract_first(),
                'stock': quote.xpath('.//div[@class="item_list_stav"]/img[@class="tool"]/src()').extract()
            }

        next_page_url = response.xpath('//li[@class="page"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
	id = scrapy.Field()
	name = scrapy.Field()
	desc = scrapy.Field()
	price = scrapy.Field()
	regprice = scrapy.Field()
	img = scrapy.Field()

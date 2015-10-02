# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FeedItem(scrapy.Item):
	headline = scrapy.Field()
	body = scrapy.Field()
	tags = scrapy.Field()
	img = scrapy.Field()

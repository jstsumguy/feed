import scrapy
import os
import re
import scraper.config as config

''' Spider for fox rss feed '''
class FoxRSSSpider(scrapy.Spider):

    name = "fox"
    allowed_domains = ["feeds.foxnews.com"]
    start_urls = config.FOX_FEED

    def parse(self, response):
        for elm in response.xpath("//item"):
            obj = FeedItem()
            obj['title'] = elm.xpath('title/text()').extract()[0]
            obj['link'] = elm.xpath('link/text()').extract()
            obj['category'] = elm.xpath('category/text()').extract()
            print obj['category'][]

            # remove non-ascii chars
            desc_raw = elm.xpath('description/text()').extract()
            obj['description'] = re.sub('<[^>]+>', '', desc_raw[0])

            yield obj
            
            #_append('fox.feed.txt', obj)

''' spider for cnn rss feed '''
# class CNNRSSSpider(scrapy.Spider):

#     name = 'cnn'
#     allowed_domains = ["rss.cnn.com"]
#     start_urls = config.CNN_FEED

#     def parse(self, response):
#         pass

''' spider for bloomberg rss feed '''
# class BLBSpider(scrapy.Spider):

#     name = 'blb'
#     allowed_domains = ["rss.cnn.com"]
#     start_urls = config.CNN_FEED

#     def parse(self, response):
#         pass

''' spider for vice rss feed '''
# class VCESpider(scrapy.Spider):

#     name = 'vice'
#     allowed_domains = ["rss.cnn.com"]
#     start_urls = config.CNN_FEED

#     def parse(self, response):
#         pass


def _append(filename, item):
    if os.path.isfile(filename):
        try:
            with open(filename, 'a') as f:
                f.write(item['title'])
                f.write(item['description'].encode('ascii', 'ignore'))
                f.write('\n\n\n\n')
        except Exception as ex:
            pass
    else:
        try:
            with open(filename, 'w') as f:
                f.write(item['title'])
                f.write(item['description'].encode('ascii', 'ignore'))
                f.write('\n\n\n\n')
        except Exception as ex:
            pass




            






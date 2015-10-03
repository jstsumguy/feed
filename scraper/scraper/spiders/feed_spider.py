import scrapy
import os
from datetime import datetime
from pymongo import MongoClient
import re
import sys

''' Defines entry urls for spiders '''
CNN_FEED = ['http://rss.cnn.com/rss/cnn_topstories.rss']
FOX_FEED = ['http://feeds.foxnews.com/foxnews/latest']

''' Spider for fox rss feed '''
class FoxRSSSpider(scrapy.Spider):

    name = "fox"
    allowed_domains = ["feeds.foxnews.com"]
    start_urls = FOX_FEED

    def parse(self, response):

        client = DBConnection()
        for elm in response.xpath("//item"):
            obj = {}
            obj['headline'] = elm.xpath('title/text()').extract()[0]
            obj['link_to'] = elm.xpath('link/text()').extract()
            obj['post_date'] = datetime.now()
            obj['categories'] = elm.xpath('category/text()').extract()
            obj['raw'] = elm.xpath('/text()').extract()
            obj['description'] = []

            if not client.update_feed(obj):
                print 'Could not sync with db'
        client.disconnect()

class DBConnection:

    def __init__(self):
        self.client = None

    def get_client(self):
        connection_str = 'mongodb://guest:password@ds063833.mongolab.com:63833/news-feed-scraper'
        if not self.client:
            try:
                self.client = MongoClient(connection_str)
            except Exception as ex:
                print str(ex)
                sys.exit("Could not establish connection")
        return self.client

    def disconnect(self):
        if self.client is not None:
            self.client.close()

    def update_feed(self, data):

        client = self.get_client()
        db = client['news-feed-scraper']

        feed = { "headline": data['headline'], 
                "description": data['description'], 
                "categories": data['categories'], 
                "link_to": data['link_to'], 
                "post_date": data['post_date'], 
                "raw": data['raw'] }
        try:
            feeds = db.feed
            feed_id = feeds.insert_one(feed).inserted_id
            return True

        except Exception as ex:
            print 'Mongodb Exception: ' + str(ex) + ' \n\n'
        return False

''' Append to file system '''
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

if __name__ == '__main__':
    main()




            






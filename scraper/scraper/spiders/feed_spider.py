import scrapy
import os
from datetime import datetime
from pymongo import MongoClient
import re
import sys

''' Defines entry urls for spiders '''
RSS_FEEDS = ['http://feeds.foxnews.com/foxnews/latest', 'http://feeds.foxnews.com/foxnews/tech', 'http://feeds.foxnews.com/foxnews/entertainment', 'http://feeds.foxnews.com/foxnews/politics', 'http://feeds.foxnews.com/foxnews/world', 'http://feeds.foxnews.com/foxnews/science', 'http://feeds.foxnews.com/foxnews/most-popular']
MAX_ROW_COUNT = 100

''' Spider for rss feeds '''
class RSSSpider(scrapy.Spider):

    name = "feed"
    allowed_domains = ["feeds.foxnews.com"]
    start_urls = RSS_FEEDS

    def __init__(self, *args, **kwargs):
        super(RSSSpider, self).__init__(*args, **kwargs)
        self.connection = DBConnection()
        self.connection.clear_feed()
        
    def parse(self, response):
        for elm in response.xpath("//item"):
            obj = {}
            obj['headline'] = elm.xpath('title/text()').extract()[0]
            obj['link_to'] = elm.xpath('link/text()').extract()
            obj['post_date'] = datetime.now()
            obj['categories'] = elm.xpath('category/text()').extract()
            obj['description'] = elm.xpath('description/text()').extract()

            if not self.connection.update_feed(obj):
                print 'Could not sync data with db'
        self.connection.disconnect()

class DBConnection:

    def __init__(self):
        self.client = None

    def get_client(self):
        connection_str = 'mongodb://<your_username>:<your_password>@your_database_uri'
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

    def clear_feed(self):
        client = self.get_client()
        db = client['news-feed-scraper']
        db.feed.remove(None)

    def update_feed(self, data):

        client = self.get_client()
        db = client['news-feed-scraper']

        feed = { "headline": data['headline'], 
                "description": data['description'], 
                "categories": data['categories'], 
                "link_to": data['link_to'], 
                "post_date": data['post_date']
                }
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





            






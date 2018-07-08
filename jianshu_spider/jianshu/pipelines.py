# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
from scrapy.exceptions import DropItem

class ItemContentPipeline(object):
    def process_item(self, item, spider):
        if item['wordage'] or item['content']:
            wordage_digits = re.search('(\d+)',item['wordage']).group(1)
            item['wordage'] = wordage_digits
            #content去除换行
            content_list = item['content']
            content_new = ''
            for content in content_list:
                content_new += re.sub('\n|\t|\s', '', content)
            item['content'] = content_new
            return item
        else:
            raise DropItem


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri,27017)
        self.db = self.client.get_database(self.mongo_db)



    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))

    def close_spider(self,spider):
        self.client.close()
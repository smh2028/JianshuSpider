# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ArticleItem(scrapy.Item):
    title = Field()
    author = Field()
    publish_time = Field()
    wordage = Field()
    views_count = Field()
    comments_count = Field()
    likes_count = Field()
    content = Field()

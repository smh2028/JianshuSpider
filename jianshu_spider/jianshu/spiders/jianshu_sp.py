# -*- coding: utf-8 -*-
import sys
import os
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
ffpath = os.path.abspath(os.path.join(fpath,".."))
print(ffpath)
sys.path.append(ffpath)

import scrapy
from scrapy.http import Request
import json
from scrapy import cmdline
from scrapy.http.response import urljoin
from jianshu.items import ArticleItem
import re
import random
from time import sleep

class JianshuSpSpider(scrapy.Spider):
    name = 'jianshu_sp'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['http://www.jianshu.com/']
    start_articles_url = 'https://www.jianshu.com/'

    def start_requests(self):
        yield Request(self.start_articles_url,callback=self.parse_jianshu_home)

    def random_delay(self):
        delay = random.random() * 0.5
        sleep(delay)

    def parse_jianshu_home(self, response):
        '''
        解析简书首页
        '''
        articles = response.xpath('//ul[@class="note-list"]/li')
        print('parse start page','-'*100)
        for article in articles:
            #./和不加任何符号，效果相同，都表示当前节点
            title = article.xpath('./div[@class="content"]/a[@class="title"]/text()').extract_first()
            brief = article.xpath('./div/p[@class="abstract"]/text()').extract_first()
            author = article.xpath('./div[@class="meta"]/a[@class="nickname"]/text()').extract_first()
            link = article.xpath('./div[@class="content"]/a[@class="title"]/@href').extract_first()
            article_url = urljoin(self.start_articles_url,link)
            # self.random_delay()
            yield Request(url=article_url,callback=self.parse_article)

    def parse_article(self,response):
        '''
        解析文章页
        '''
        item = ArticleItem()
        article = response.xpath('//div[@class="article"]')
        item['title'] = article.xpath('./h1/text()').extract_first()
        item['author'] = article.xpath('./div[@class="author"]/div/span/a/text()').extract_first()
        article_info = article.xpath('./div[@class="author"]/div[@class="info"]/div[@class="meta"]')
        result_dict = response.xpath('//script[@data-name="page-data"]/text()').extract_first()
        json_dict = json.loads(result_dict)
        item['publish_time'] = article_info.xpath('./span/text()').extract_first()
        # wordage_full = article_info.xpath('./span/text()')[1].extract()
        # item['wordage'] = re.search('(\d+)',wordage_full).group(1)
        item['wordage'] = article_info.xpath('./span/text()')[1].extract()
        # item['views_count'] = article_info.xpath('./span[@class="views_count"]/text()').extract_first()
        # item['comments_count'] = article_info.xpath('./span[@class="comments_count"]/text()').extract_first()
        # item['likes_count'] = article_info.xpath('./span[@class="likes_count"]/text()').extract_first()
        item['views_count'] = json_dict.get('note').get('views_count')
        item['comments_count'] = json_dict.get('note').get('comments_count')
        item['likes_count'] = json_dict.get('note').get('likes_count')
        #content是列表
        contens_list = article.xpath('./div[@class="show-content"]/div[@class="show-content-free"]/p/text()').extract()
        item['content'] = contens_list
        yield item
        #根据页面底端推荐列表，生成新的请求
        hrefs = response.xpath('//div[@class="note-bottom"]//a[@class="title"]/@href').extract()
        for href in hrefs:
            link = urljoin(self.start_articles_url,href)
            # self.random_delay()
            yield Request(url=link,callback=self.parse_article)

if __name__ == '__main__':
    cmdline.execute('scrapy crawl jianshu_sp '.split())
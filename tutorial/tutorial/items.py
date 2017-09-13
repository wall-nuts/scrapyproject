# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DingdianItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    word_count = scrapy.Field()
    update_date = scrapy.Field()
    status = scrapy.Field()
    tag = scrapy.Field()
    url = scrapy.Field()

class ChapterItem(scrapy.Item):
    noval_name = scrapy.Field()
    title = scrapy.Field()
    p = scrapy.Field()

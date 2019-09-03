# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PsleItem(scrapy.Item):
    url = scrapy.Field(title='a url')
    status = scrapy.Field()
    tables = scrapy.Field()
    region = scrapy.Field()
    district = scrapy.Field()
    school = scrapy.Field()
    is_error = scrapy.Field()

class AcseeItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    exam_center = scrapy.Field()
    is_error = scrapy.Field()
    errors = scrapy.Field()
    html = scrapy.Field()
    result_table = scrapy.Field() #header = 0
    rankings_table = scrapy.Field() #category, rank
    div_performance_table = scrapy.Field() #header = 0
    subject_performance_table = scrapy.Field() #header = 0
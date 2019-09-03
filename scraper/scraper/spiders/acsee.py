import time
import re
import os
import datetime as dt
from functools import partial
import scrapy
from ..items import AcseeItem

class Acsee(scrapy.Spider):
    name = 'acsee'
    custom_settings = {'DOWNLOAD_DELAY': 4,
                        'AUTOTHROTTLE_ENABLED': True,
                        'FEED_URI': None,
                        'FEED_FORMAT': 'jsonlines',
                        'ITEM_PIPELINES': {'scraper.pipelines.AcseeMakeDataFrame': 99,
                                            'scraper.pipelines.AcseeJsonWriter': 100},
                        'RETRY_TIMES': 5}
                        #TODO: Safe support for persistence. Seems crawling links is random, so might be safer
                        #to filter out links based on what has already been exported to jsonlines file.

    def __init__(self, start_urls, feed_uri, *args, **kwargs):
        super(Acsee, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.custom_settings['FEED_URI'] = feed_uri

    def parse(self, response):
        #Crawl all the non-index page links from that year's ACSEE main page
        if response.url in self.start_urls:
            for anchor in response.xpath('//a'): #all links on the first page of ACSEE results
                link = anchor.xpath('@href').get()
                text = anchor.xpath('text()').get().strip()
                new_callback = partial(self.parse_results_page, exam_center=text)
                if 'index' not in link:
                    yield response.follow(link, callback=new_callback, errback=self.errback)
                    
                    #hacky for particular urls
                    # if link[-9].lower() != 'p':
                    #     yield response.follow(link, callback=new_callback, errback=self.errback)
                    

    def parse_results_page(self, response, exam_center):
        #All the center results pages
        if response.url not in self.start_urls: #Don't try to crawl the start_url
            yield AcseeItem(url=response.url, status=response.status, html=response.text,
        exam_center=exam_center, is_error=False)
    
    def errback(self, error):
        time.sleep(120) #give the server some air
        yield {'is_error': True,
                'status': str(error.value)}        
import time
import re
import os
import datetime as dt
from functools import partial
import scrapy
from ..items import PsleItem

class Psle(scrapy.Spider):
    name = 'psle'
    custom_settings = {'DOWNLOAD_DELAY': 4,
                        'AUTOTHROTTLE_ENABLED': True,
                        'FEED_URI': None,
                        'FEED_FORMAT': 'jsonlines',
                        'ITEM_PIPELINES': {'scraper.pipelines.PsleMakeDataFrame': 99,
                                            'scraper.pipelines.PsleJsonWriter': 100}}
                        #TODO: Safe support for persistence. Seems crawling links is random, so might be safer
                        #to filter out links based on what has already been exported to jsonlines file.
    school_regex = re.compile('/(?!.*/)(.*ps\d+.+)')
    district_regex = re.compile('/(?!.*/)(.*dis.+)')
    region_regex = re.compile('/(?!.*/)(.*reg.+)')

    def __init__(self, start_urls, feed_uri, *args, **kwargs):
        super(Psle, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.custom_settings['FEED_URI'] = feed_uri

    def parse(self, response):
        #All the links from that year's PSLE main page
        if not self.school_regex.search(response.url)\
        and not self.district_regex.search(response.url)\
        and not self.region_regex.search(response.url):
            for anchor in response.xpath('//a'):
                link = anchor.xpath('@href').get()
                text = anchor.xpath('text()').get().strip()
                new_callback = partial(self.parse_region_page, region=text)
                yield response.follow(link, callback=new_callback, errback=self.errback)

    def parse_region_page(self, response, region):
        #All the links at this response.url are districts
        if self.region_regex.search(response.url): #if it is a region page
            for anchor in response.xpath('//a'):
                link = anchor.xpath('@href').get()
                text = anchor.xpath('text()').get().strip()
                new_callback = partial(self.parse_district_page, region=region, district=text)
                yield response.follow(link, callback=new_callback, errback=self.errback)
    
    def parse_district_page(self, response, region, district):
        #All the links at this response.url are to go to individual school data
        if self.district_regex.search(response.url):
            for anchor in response.xpath('//a'):
                link = anchor.xpath('@href').get()
                text = anchor.xpath('text()').get().strip()
                new_callback = partial(self.parse_school_page, region=region, district=district, school=text)
                yield response.follow(link, callback=new_callback, errback=self.errback)
    
    def parse_school_page(self, response, region, district, school):
        #All of these pages are static school pages with no links
        if self.school_regex.search(response.url):
            #https://stackoverflow.com/a/41862373 for more on XPATH usage of dot vs. text()
            yield PsleItem(url=response.url, status=response.status, tables=response.xpath('//table[contains(., "CAND. NO")]').getall(),
            region=region, district=district, school=school, is_error=False)
    
    def errback(self, error):
        time.sleep(120) #give the server some air
        yield {'is_error': True,
                'status': str(error.value)}        
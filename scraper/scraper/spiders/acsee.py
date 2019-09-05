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

    def __init__(self, start_urls, feed_uri, last_run_jl=None, *args, **kwargs):
        super(Acsee, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.custom_settings['FEED_URI'] = feed_uri
        if last_run_jl:
            self.last_run = list()
            import json
            with open(last_run_jl, 'r') as File:
                for line in File:
                    self.last_run.append((json.loads(line)))
                File.close()
            regex = re.compile('/(?!.*/)(.*)') #capturing text after the last slash /; could also .split('/')[-1]
            self.last_run_urls = [regex.search(i['url']).group()[1:] for i in self.last_run] #find the match and add to list, e.g. p0101.htm
        else:
            self.last_run = None

    def parse(self, response):
        #Crawl all page links from that year's ACSEE main page
        if response.url in self.start_urls:
            for anchor in response.xpath('//a'): #all links on the first page of ACSEE results
                link = anchor.xpath('@href').get()
                #import pdb; pdb.set_trace() for breakpoint interactive debugging
                text = anchor.xpath('text()').get().strip()
                new_callback = partial(self.parse_results_page, exam_center=text)
                if not self.last_run:
                    yield response.follow(link, callback=new_callback, errback=self.errback)
                else:
                    if link.lower().split('/')[-1] not in self.last_run_urls:
                        yield response.follow(link, callback=new_callback, errback=self.errback)
                    
                    #hacky for particular urls
                    # if link[-9].lower() != 'p':
                    #     yield response.follow(link, callback=new_callback, errback=self.errback)
                    

    def parse_results_page(self, response, exam_center):
        #All the center results pages
        if response.url not in self.start_urls and 'index' not in response.url: #Don't try to *scrape* the start_url
            yield AcseeItem(url=response.url, status=response.status, html=response.text,
        exam_center=exam_center, is_error=False)
    
    def errback(self, error):
        time.sleep(120) #give the server some air
        yield {'is_error': True,
                'status': str(error.value)}        
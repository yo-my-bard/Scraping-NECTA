from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('psle', ['https://necta.go.tz/results/2018/psle/psle.htm'],
            'file://C:/Users/Yusuph/Documents/GitHub/Scraping-NECTA/scraper/export/psle.jl')

process.start()
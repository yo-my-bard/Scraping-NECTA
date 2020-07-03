from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

FILE_SCHEME = "file://"
EXPORT_FILE = "/Users/Muse/Documents/GitHub/Scraping-NECTA/scraper/export/psle.jl"
os.makedirs(os.path.dirname(EXPORT_FILE), exist_ok=True)
 
process = CrawlerProcess(get_project_settings())

process.crawl('psle', ['https://onlinesys.necta.go.tz/results/2019/psle/psle.htm'],
            FILE_SCHEME+EXPORT_FILE)

process.start()
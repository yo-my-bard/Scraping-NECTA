"""
The initial stage. Sequentially, this process must come first. The rest of the modules
depend on the URLs that this web crawler finds. Most importantly, if saved to a data
storage location (MySQL, etc.) then you can refer to that instead of having to recrawl
the server. This was more or less a crawler from scratch (Udacity intro course helped!),
so may be worth looking into if other crawling packages (BeautifulSoup, etc.) can do better.
Submit a pull request!

"""
from lxml import html
import requests
from ratelimit import *
from sqlstore import storeinDB


"""

Because of how the URLs are, we need 3 ways of lengthening
the links for each depth. As well as short/long procedures.

"""


def short_urls(link):
    url = link
    page = requests.get(url)
    seed = html.fromstring(page.content)
    short_urls = seed.xpath('//a/@href')
    return short_urls

def full_url(list):
    complete_url = []
    for e in list:
        full = 'http://www.necta.go.tz/psle2013/'+e #Change this for the other years
        complete_url.append(full)
    return complete_url

def full_url2(list):
    complete_url = []
    for e in list:
        full = 'http://www.necta.go.tz/psle2013/results/'+e #Change this for the other years
        complete_url.append(full)
    return complete_url


def union(p,q):
    """
    Add future URLs to crawl, that haven't been crawled yet.
    :param p: crawled
    :param q: to be crawled
    :return: fully crawled list of URLs
    """
    for e in q:
        if e not in p:
            p.append(e)

#This is the entire program pieces put together to crawl
#everything

@rate_limited(1)
def crawl_web(seed):
    """
    Crawl NECTA HTML tables when starting at the year's region page.
    :param seed: NECTA page for the year e.g. http://www.necta.go.tz/psle2013/
    :return: URLs of every school's PSLE student-level data

    """
    tocrawl = [seed]
    crawled = []
    next_depth = []
    table_urls = []
    depth = 0
    while tocrawl and depth < 1:
        page = tocrawl.pop()
        if page not in crawled:
            union(next_depth, full_url(short_urls(page)))
            crawled.append(page)
        if not tocrawl:
            depth +=1
            tocrawl, next_depth = next_depth, []
    while tocrawl and depth < 2:
        page = tocrawl.pop()
        if page not in crawled:
            union(next_depth, full_url2(short_urls(page)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth += 1
    while tocrawl and depth < 3:
        page = tocrawl.pop()
        if page not in crawled:
            union(table_urls, full_url2(short_urls(page)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth +=1
    return table_urls


"""

Store all the table links in a database.
When first crawling, store the list in a database so you don't have to crawl again to get the tables.
Uncomment the code below to store in your database - be sure you configure storeinDB prior to using it.

"""

# page = 'http://www.necta.go.tz/psle2013/psle.htm'
# list_of_urls = crawl_web(page)
#
# print("About to put this pup in the database. Hold my beer.")
#
# storeinDB(list_of_urls)

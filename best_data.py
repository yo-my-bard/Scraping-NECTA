"""

If you opted to store your URLs in a database, use the provided SQL retrieval module and scrape some data.

"""

from pd_tablefetch import merge_all as merge
from pd_tablefetch import make_pretty as pretty
from sqlstore import fetchlist



table_urls = fetchlist()

print('List fetched....analyzing...')

#REMEMBER TO NAME A NEW CSV FILE in pd_tablefetch for subsequent iterations. The first run will likely fail because of
#Connection Refused, and other similar errors thrown by the server.

bigtable = merge(table_urls)

print("Merging complete...")

pretty(bigtable)

print("You've crawled 'em all!")

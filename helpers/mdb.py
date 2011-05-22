from minimongo import *

myDB = "sprocket_mdb"

class Listings(Model):
    class Meta:
        database = myDB
        collection = "listings"
        indeces = (Index("sku"), Index("author"), Index("title"))

import re
def getSearchQuery(attr, searchText):
# simply search or OR search for strings with spaces
    query = {}
    if searchText:
        words = searchText.split()
        query[attr] = re.compile('|'.join(words), re.IGNORECASE)
    return query

# Common constants used throughout the service

import symbolize, symbolscache, sys, urllib3

DOWNLOADS_URL_BASE = 'http://downloads.mongodb.org/'
LIST_BUILDS_URL_BASE = 'http://www.mongodb.org/dl/'

# Globally available services
gHttpService = urllib3.PoolManager()
gSymbolsCacheService = symbolscache.SymbolsCache(symbolize.LOCAL_CACHE_DIR)

# Global services initialization
symbolize.init_cache()

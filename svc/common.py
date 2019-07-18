# Common constants used throughout the service

import symbolscache, sys, urllib3

# Ensure that mongosymb is on the expected path
sys.path.append('triage-scripts/mongosymb')
import symbolize

DOWNLOADS_URL_BASE = 'http://downloads.mongodb.org/'
LIST_BUILDS_URL_BASE = 'http://www.mongodb.org/dl/'

# Globally available services
gHttpService = urllib3.PoolManager()
gSymbolsCacheService = symbolscache.SymbolsCache(symbolize.LOCAL_CACHE_DIR)

# Global services initialization
symbolize.init_cache()

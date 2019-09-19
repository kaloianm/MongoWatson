# Common constants and utilities used throughout the service

import keyring, symbolize, symbolscache, sys, urllib3

DOWNLOADS_URL_BASE = 'http://downloads.mongodb.org/'
LIST_BUILDS_URL_BASE = 'http://www.mongodb.org/dl/'
SERVICE_NAME = 'MongoWatson'

# Globally available services
gHttpService = urllib3.PoolManager()
gSymbolsCacheService = symbolscache.SymbolsCache(symbolize.LOCAL_CACHE_DIR)

# Global services initialization
symbolize.init_cache()


# Keyring utilities
def getPassword(user):
    return keyring.get_password(SERVICE_NAME, user)

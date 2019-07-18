import common, json, re, symbolize

from flask import jsonify
from werkzeug.exceptions import BadRequest

sourcePathRegex = r'/data/mci/(?P<buildId>\w+)/src/(?P<sourcePath>[\w\W]+):(?P<lineNum>\d+):(?P<colNum>\d+):\s+(?P<funcName>\S{1}[\S\s]+)'


def gitUrl(buildInfo, stackLine):
    match = re.match(sourcePathRegex, stackLine)
    if (match):
        return {
            'functionName':
                match['funcName'],
            'sourceFileUrl':
                'https://github.com/mongodb/mongo/tree/{}/{}#L{}'.format(buildInfo['githash'],
                                                                     match['sourcePath'],
                                                                     match['lineNum'])
        }
    else:
        return {'functionName': None}


class SymbolizeStackRequest:
    def __init__(self, request):
        self.stack = request['stack']


class SymbolizeStackResponse:
    def __init__(self, buildInfo, stackFrames):
        self.buildInfo = buildInfo
        self.stackFrames = stackFrames

    def tojson(self):
        return jsonify(buildInfo=self.buildInfo, stackFrames=self.stackFrames)


def symbolizeStackRequestImpl(request):
    if (not request.is_json):
        raise BadRequest('Invalid request content')

    ssRequest = SymbolizeStackRequest(request.get_json())

    buildInfo = json.loads(""" {
        "uname": {
            "sysname": "Linux",
            "release": "3.10.0-327.el7.x86_64",
            "version": "#1 SMP Thu Nov 19 22:10:57 UTC 2015",
            "machine": "x86_64"
        },
        "version": "3.2.9",
        "githash": "22ec9e93b40c85fc7cae7d56e7d6a02fd811088c",
        "edition": "community",
        "buildId": "6cc0db94b5f0b88048bd857b35f6d91747e14577"
    } """)

    stackFrames = """
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/mongo/util/stacktrace_posix.cpp:171:0: mongo::printStackTrace(std::ostream&)
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/mongo/util/signal_handlers_synchronous.cpp:180:0: mongo::(anonymous namespace)::printSignalAndBacktrace(int)
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/mongo/util/signal_handlers_synchronous.cpp:276:0: mongo::(anonymous namespace)::abruptQuitWithAddrSignal(int, siginfo_t*, void*)
        ??:0:0: ??
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/linked_list.h:75:0: SLL_PopRange
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/thread_cache.h:229:0: tcmalloc::ThreadCache::FreeList::PopRange(int, void**, void**)
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/thread_cache.cc:235:0: tcmalloc::ThreadCache::ReleaseToCentralCache(tcmalloc::ThreadCache::FreeList*, unsigned long, int)
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/thread_cache.cc:197:0: tcmalloc::ThreadCache::ListTooLong(tcmalloc::ThreadCache::FreeList*, unsigned long)
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/thread_cache.h:390:0: tcmalloc::ThreadCache::Deallocate(void*, unsigned long)
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/tcmalloc.cc:1227:0: do_free_helper
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/tcmalloc.cc:1257:0: do_free_with_callback
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/tcmalloc.cc:1266:0: do_free
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/gperftools-2.2/src/tcmalloc.cc:1617:0: free
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/btree/bt_discard.c:423:0: __free_update
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/btree/bt_discard.c:221:0: __free_page_modify
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/btree/bt_discard.c:115:0: __wt_page_out
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/evict/evict_page.c:276:0: __evict_page_dirty_update
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/evict/evict_page.c:124:0: __wt_evict
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/evict/evict_lru.c:1665:0: __evict_page
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/evict/evict_lru.c:916:0: __evict_lru_pages
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/evict/evict_lru.c:507:0: __evict_helper
        /data/mci/f12ef8ea00e4c7b69c83a1a5fbe9d0f8/src/src/third_party/wiredtiger/src/evict/evict_lru.c:220:0: __evict_thread_run
    """.strip().splitlines()

    ssResponse = SymbolizeStackResponse(
        buildInfo, list(map(lambda stackFrame: gitUrl(buildInfo, stackFrame.strip()), stackFrames)))

    return ssResponse.tojson()

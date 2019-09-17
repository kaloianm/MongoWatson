#!/usr/bin/env python

import common, json, re, symbolize

from flask import jsonify
from werkzeug.exceptions import BadRequest

sourcePathRegex = r'/data/mci/(?P<buildId>\w+)/src/(?P<sourcePath>[\w\W]+)'
kGithubUrl = 'https://github.com/mongodb/mongo/blob/{}/{}#L{}'


# Expects 'stackLine' to be json with the following fielts:
#   {
#       symbinfo: [ {
#           fn: 'mongo::function()',
#           file: '/data/mci/...',
#           column: 0,
#           line: 171
#       } ]
#   }
#
def gitUrl(githash, stackLine):
    symbol_info = stackLine['symbinfo'][0]
    match = re.match(sourcePathRegex, symbol_info['file'])

    return {
        'fn':
            symbol_info['fn'],
        'url':
            kGithubUrl.format(githash, match['sourcePath'], symbol_info['line']) if match else None
    }


class SymbolizeStackRequest:
    def __init__(self, request):
        if isinstance(request['stack'], str):
            self.stack = json.loads(request['stack'])
        else:
            self.stack = request['stack']


# Object which serializes itself to json with the following content:
#
# {
#  "buildInfo": {
#    "buildId": "6cc0db94b5f0b88048bd857b35f6d91747e14577",
#    "edition": "community",
#    "githash": "22ec9e93b40c85fc7cae7d56e7d6a02fd811088c",
#    "uname": {
#      "machine": "x86_64",
#      "release": "3.10.0-327.el7.x86_64",
#      "sysname": "Linux",
#      "version": "#1 SMP Thu Nov 19 22:10:57 UTC 2015"
#    },
#    "version": "3.2.9"
#  },
#  "stackFrames": [
#    {
#      "fn": "mongo::printStackTrace(std::ostream&)",
#      "url": "https://github.com/mongodb/mongo/tree/22ec9e93b40c85fc7cae7d56e7d6a02fd811088c/src/mongo/util/stacktrace_posix.cpp#L171"
#    },
#       ....
#    {
#      "fn": "??",
#      "url": null
#    }
#  ]
# }
class SymbolizeStackResponse:
    def __init__(self, buildInfo, stackFrames):
        self.buildInfo = buildInfo
        self.stackFrames = stackFrames

    def tojson(self):
        return jsonify(buildInfo=self.buildInfo, stackFrames=self.stackFrames)


def symbolizeStackRequestImpl(request):
    if request.is_json:
        ssRequest = SymbolizeStackRequest(request.get_json())
    else:
        raise BadRequest('Invalid request content')

    build_info, symbolized_stacktrace = symbolize.symbolize_backtrace_from_logs(
        json.dumps(ssRequest.stack), json_format=True)

    ssResponse = SymbolizeStackResponse(
        build_info,
        list(
            map(lambda stackFrame: gitUrl(build_info['githash'], stackFrame),
                json.loads(symbolized_stacktrace))))

    return ssResponse.tojson()

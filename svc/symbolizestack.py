#!/usr/bin/env python

import common, hashlib, hmac, json, re, symbolize, urllib

from bson import json_util
from flask import jsonify
from werkzeug.exceptions import BadRequest

kSourcePathRegex = r'/data/mci/(?P<buildId>\w+)/src/(?P<sourcePath>[\w\W]+)'
kGithubUrl = 'https://github.com/mongodb/mongo/blob/{}/{}#L{}'
kStatsServiceUrl = 'https://us-east-1.aws.webhooks.mongodb-stitch.com/api/client/v2.0/app/mongowatson-fvkop/service/https/incoming_webhook/{}'


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
    match = re.match(kSourcePathRegex, symbol_info['file'])

    return {
        'fn':
            symbol_info['fn'],
        'url':
            kGithubUrl.format(githash, match['sourcePath'], symbol_info['line']) if match else None
    }


# Object, which deserializes a request of json type with the following content:
#
# {
#   stack: (string or json)
# }
class SymbolizeStackRequest:
    def __init__(self, request):
        stack = request['stack']
        if isinstance(stack, str):
            self.stack = stack
        elif isinstance(stack, dict):
            self.stack = json.dumps(stack)
        else:
            raise BadRequest('The stack must be a string or json, but received {}'.format(
                type(stack)))


# Object, which serializes itself to json with the following content:
#
# {
#   buildInfo: {
#     buildId: "6cc0db94b5f0b88048bd857b35f6d91747e14577",
#     edition: "community",
#     githash: "22ec9e93b40c85fc7cae7d56e7d6a02fd811088c",
#     uname: {
#       machine: "x86_64",
#       release: "3.10.0-327.el7.x86_64",
#       sysname: "Linux",
#       version: "#1 SMP Thu Nov 19 22:10:57 UTC 2015"
#    },
#    version: "3.2.9"
#  },
#  stackFrames: [
#    {
#      fn: "mongo::printStackTrace(std::ostream&)",
#      url: "https://github.com/mongodb/mongo/tree/22ec9e93b40c85fc7cae7d56e7d6a02fd811088c/src/mongo/util/stacktrace_posix.cpp#L171"
#    },
#       ....
#    {
#      fn: "??",
#      url: null
#    }
#  ]
# }
class SymbolizeStackResponse:
    def __init__(self, buildInfo, stackFrames, occurrences):
        self.buildInfo = buildInfo
        self.stackFrames = stackFrames
        self.occurrences = occurrences

    def tojson(self):
        return jsonify(buildInfo=self.buildInfo, stackFrames=self.stackFrames,
                       occurrences=self.occurrences)


# Object, which serializes itself to the json format expected by the 'stats' service:
#
# {
#   stackFrames: [ (string function name), ... ],
#   rawinput: (string representation of the stack the customer pasted)
# }
class StatsServiceRequest:
    def __init__(self, stackFrames, rawinput):
        self.stackFrames = stackFrames
        self.rawinput = rawinput

    def tojson(self):
        return jsonify(stackFrames=self.stackFrames, rawinput=self.rawinput)


def symbolizeStackRequestImpl(request):
    if request.is_json:
        ssRequest = SymbolizeStackRequest(request.get_json())
    else:
        raise BadRequest('Invalid request content. Must be JSON, but received {}'.format(
            request.content_type))

    try:
        build_info, symbolized_stacktrace = symbolize.symbolize_backtrace_from_logs(
            ssRequest.stack, json_format=True)
    except symbolize.SymbolizerError as e:
        raise BadRequest('Unable to symbolize stack trace') from e

    stackFrames = list(
        map(lambda stackFrame: gitUrl(build_info['githash'], stackFrame),
            json.loads(symbolized_stacktrace)))

    # Call into the Stats service
    statsSvcRequest = StatsServiceRequest(stackFrames, json.dumps(ssRequest.stack))
    statsSvcRequestJson = statsSvcRequest.tojson()
    hash = hmac.new(
        common.getPassword('STATS_SVC_CREDENTIAL').encode('utf-8'), statsSvcRequestJson.data,
        hashlib.sha256)
    statsSvcResponse = common.gHttpService.urlopen(
        'POST', kStatsServiceUrl.format('getStackStats'), headers={
            'Content-Type': 'application/json',
            'X-Hook-Signature': 'sha256=' + hash.hexdigest(),
        }, body=statsSvcRequestJson.data)
    statsSvcResponseJson = json_util.loads(statsSvcResponse.data)

    # Construct the response
    ssResponse = SymbolizeStackResponse(build_info, stackFrames,
                                        statsSvcResponseJson['occurrences'])
    return ssResponse.tojson()
